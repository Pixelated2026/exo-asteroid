use fs2::FileExt;
use pyo3::exceptions::{PyException, PyRuntimeError};
use pyo3::prelude::{PyModule, PyModuleMethods};
use pyo3::{Bound, PyErr, PyResult, Python, pyclass, pymethods};
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::PathBuf;

#[gen_stub_pyclass]
#[pyclass(frozen, extends=PyException, name="PidfileError")]
pub struct PyPidfileError(String);

impl PyPidfileError {
    fn into_pyerr(self, py: Python<'_>) -> PyErr {
        match Bound::new(py, self) {
            Ok(err) => PyErr::from_value(err.into_any()),
            Err(err) => err,
        }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyPidfileError {
    fn __repr__(&self) -> String {
        format!("PidfileError({:?})", self.0)
    }

    fn __str__(&self) -> String {
        self.0.clone()
    }
}

/// A Windows PID file protected by a persistent sidecar lock file.
struct LockedPidfile {
    path: PathBuf,
    lock_file: File,
}

impl Drop for LockedPidfile {
    fn drop(&mut self) {
        // Delete the PID while still holding the sidecar lock. The lock file itself
        // remains in place so waiters always coordinate on the same Windows file.
        let _ = fs::remove_file(&self.path);
        let _ = FileExt::unlock(&self.lock_file);
    }
}

#[gen_stub_pyclass]
#[pyclass(name = "Pidfile")]
pub struct PyPidfile(Option<LockedPidfile>);

impl PyPidfile {
    fn get_mut(&mut self) -> PyResult<&mut LockedPidfile> {
        self.0
            .as_mut()
            .ok_or_else(|| PyRuntimeError::new_err("cannot use resource after exiting context"))
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyPidfile {
    /// Creates and locks a PID file. The sidecar lock file is retained on disk.
    #[new]
    fn py_new(py: Python<'_>, path: PathBuf, _mode: u32) -> PyResult<Self> {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|error| {
                PyPidfileError(format!("Unable to create PID file directory: {error}"))
                    .into_pyerr(py)
            })?;
        }

        let mut lock_path = path.as_os_str().to_os_string();
        lock_path.push(".lock");
        let lock_path = PathBuf::from(lock_path);
        let lock_file = OpenOptions::new()
            .create(true)
            .read(true)
            .write(true)
            .open(&lock_path)
            .map_err(|error| {
                PyPidfileError(format!("Unable to open PID lock file: {error}"))
                    .into_pyerr(py)
            })?;

        if let Err(error) = FileExt::try_lock_exclusive(&lock_file) {
            let existing_pid = fs::read_to_string(&path).unwrap_or_default();
            let detail = if existing_pid.trim().is_empty() {
                String::new()
            } else {
                format!(" (PID {})", existing_pid.trim())
            };
            return Err(PyPidfileError(format!(
                "PID file {} is already locked{}: {}",
                path.display(),
                detail,
                error
            ))
            .into_pyerr(py));
        }

        Ok(Self(Some(LockedPidfile { path, lock_file })))
    }

    /// Writes the current process ID to the locked PID file.
    fn write(&mut self, py: Python<'_>) -> PyResult<()> {
        let pidfile = self.get_mut()?;
        let mut file = OpenOptions::new()
            .create(true)
            .write(true)
            .truncate(true)
            .open(&pidfile.path)
            .map_err(|error| {
                PyPidfileError(format!("Unable to open PID file: {error}")).into_pyerr(py)
            })?;
        write!(file, "{}", std::process::id()).map_err(|error| {
            PyPidfileError(format!("Unable to write PID file: {error}")).into_pyerr(py)
        })?;
        file.sync_all().map_err(|error| {
            PyPidfileError(format!("Unable to flush PID file: {error}")).into_pyerr(py)
        })
    }

    /// Raw POSIX file descriptors do not exist on Windows.
    fn as_raw_fd(&self) -> PyResult<i64> {
        Err(PyRuntimeError::new_err(
            "as_raw_fd() is unavailable on Windows; legacy daemonization is unsupported",
        ))
    }

    /// Closes the PID file and releases its inter-process lock.
    fn close(&mut self) {
        self.0 = None;
    }
}

pub fn pidfile_submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyPidfileError>()?;
    m.add_class::<PyPidfile>()?;
    Ok(())
}
