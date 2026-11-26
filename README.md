<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="/docs/imgs/exo-logo-black-bg.jpg">
  <img alt="exo logo" src="/docs/imgs/exo-logo-transparent.png" width="50%" height="50%">
</picture>

exo: Run frontier AI locally. Maintained by [exo labs](https://x.com/exolabs).

<p align="center">
  <a href="https://discord.gg/TJ4P57arEm" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Discord-Join%20Server-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://x.com/exolabs" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/twitter/follow/exolabs?style=social" alt="X"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0.html" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/License-Apache2.0-blue.svg" alt="License: Apache-2.0"></a>
</p>

</div>

---

exo connects all your devices into an AI cluster. Not only does exo enable running models larger than would fit on a single device, but with [day-0 support for RDMA over Thunderbolt](https://x.com/exolabs/status/2001817749744476256?s=20), makes models run faster as you add more devices.

## Features

- **Automatic Device Discovery**: Devices running exo automatically discover each other - no manual configuration.
- **RDMA over Thunderbolt**: exo ships with [day-0 support for RDMA over Thunderbolt 5](https://x.com/exolabs/status/2001817749744476256?s=20), enabling 99% reduction in latency between devices.
- **Topology-Aware Auto Parallel**: exo figures out the best way to split your model across all available devices based on a real-time view of your device topology. It takes into account device resources and network latency/bandwidth between each link.
- **Tensor Parallelism**: exo supports sharding models, for up to 1.8x speedup on 2 devices and 3.2x speedup on 4 devices.
- **MLX Support**: exo uses [MLX](https://github.com/ml-explore/mlx) as an inference backend and [MLX distributed](https://ml-explore.github.io/mlx/build/html/usage/distributed.html) for distributed communication.
- **Multiple API Compatibility**: Compatible with OpenAI Chat Completions API, Claude Messages API, OpenAI Responses API, and Ollama API - use your existing tools and clients.
- **Custom Model Support**: Load custom models from HuggingFace hub to expand the range of available models.

## Dashboard

exo includes a built-in dashboard for managing your cluster and chatting with models.

<p align="center">
  <img src="docs/imgs/dashboard-cluster-view.png" alt="exo dashboard - cluster view showing 4 x M3 Ultra Mac Studio with DeepSeek v3.1 and Kimi-K2-Thinking loaded" width="80%" />
</p>
<p align="center"><em>4 × 512GB M3 Ultra Mac Studio running DeepSeek v3.1 (8-bit) and Kimi-K2-Thinking (4-bit)</em></p>

## Benchmarks

<details>
  <summary>Qwen3-235B (8-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA</summary>
  <img src="docs/benchmarks/jeffgeerling/mac-studio-cluster-ai-full-1-qwen3-235b.jpeg" alt="Benchmark - Qwen3-235B (8-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA" width="80%" />
  <p>
    <strong>Source:</strong> <a href="https://www.jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5">Jeff Geerling: 15 TB VRAM on Mac Studio – RDMA over Thunderbolt 5</a>
  </p>
</details>

<details>
  <summary>DeepSeek v3.1 671B (8-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA</summary>
  <img src="docs/benchmarks/jeffgeerling/mac-studio-cluster-ai-full-2-deepseek-3.1-671b.jpeg" alt="Benchmark - DeepSeek v3.1 671B (8-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA" width="80%" />
  <p>
    <strong>Source:</strong> <a href="https://www.jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5">Jeff Geerling: 15 TB VRAM on Mac Studio – RDMA over Thunderbolt 5</a>
  </p>
</details>

<details>
  <summary>Kimi K2 Thinking (native 4-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA</summary>
  <img src="docs/benchmarks/jeffgeerling/mac-studio-cluster-ai-full-3-kimi-k2-thinking.jpeg" alt="Benchmark - Kimi K2 Thinking (native 4-bit) on 4 × M3 Ultra Mac Studio with Tensor Parallel RDMA" width="80%" />
  <p>
    <strong>Source:</strong> <a href="https://www.jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5">Jeff Geerling: 15 TB VRAM on Mac Studio – RDMA over Thunderbolt 5</a>
  </p>
</details>

---

## Quick Start

Devices running exo find each other automatically, without any manual configuration, when they are on the same network and run the same version of exo (see [Adding another Mac](#adding-another-mac)). Each device provides an API and a dashboard for interacting with your cluster (runs at `http://localhost:52415`).

You can run exo with the macOS app, the easiest way on a Mac, or from source on macOS or Linux.

### macOS App

exo ships a macOS app that runs in the background, in your Mac's menu bar.

<img src="docs/imgs/macos-app-one-macbook.png" alt="exo macOS App - running on a MacBook" width="35%" />

The app needs a Mac with Apple silicon and macOS Sequoia 15.1 or later. [RDMA over Thunderbolt](#enabling-rdma-on-macos) needs macOS Tahoe 26.2 or later.

Download the latest version: [EXO-latest.dmg](https://assets.exolabs.net/EXO-latest.dmg). Open it, drag EXO to your Applications folder, and open EXO from there. The first time, macOS asks whether you want to open an app downloaded from the internet: click **Open**.

You can also install it with Homebrew:

```bash
brew install --cask exo
```

#### What EXO asks for, and why

- **Local Network access.** macOS asks whether EXO may find devices on your local network. EXO needs this to find your other devices running exo and share the work with them. If you said no, turn EXO on in System Settings → Privacy & Security → Local Network, then quit and reopen EXO.
- **Thunderbolt network setup (optional, needs your administrator password).** EXO offers to set up networking for Thunderbolt in its menu when Macs are connected with Thunderbolt cables; you can also do it in Settings › Cluster. Macs that share a Wi-Fi or Ethernet network don't need it. If you agree, EXO installs a small system service (`io.exo.networksetup`) that:
  - creates a network location called `exo` and switches this Mac to it;
  - gives each Thunderbolt port its own network service, which gets an address automatically;
  - turns off Thunderbolt Bridge, which can flood the network with packets when three or more Macs are cabled in a loop.

  The service runs when your Mac starts and about every 30 minutes, to keep these settings in place. The `exo` location starts with default settings, so anything you changed in your usual location (such as a fixed IP address, DNS servers or proxies) doesn't apply while it's in use. To undo the setup, [uninstall EXO](#uninstalling-the-macos-app). To undo it but keep EXO, run the uninstall script described there: it restores your network settings and keeps your downloaded models, and EXO asks again before it sets up the network.
- **Opening at login.** EXO's welcome window has **Open EXO at login** ticked, so your Mac is ready to work with the others after a restart. Untick it there, or change it later in EXO's Settings › General or in System Settings → General → Login Items & Extensions.
- **Notifications.** EXO doesn't ask at launch. When an update is ready to install, it leaves a quiet notification in Notification Center; you can turn these off in System Settings → Notifications. You can always check for updates in EXO's menu or Settings.

#### Adding another Mac

1. Install EXO on the other Mac and open it.
2. Put both Macs on the same local network (Wi-Fi or Ethernet), or connect them with a Thunderbolt cable.
3. Make sure both Macs run the same version of exo. Devices running different versions don't join each other.

The new Mac shows up in the dashboard within a few seconds.

To see which version a Mac runs:

- in the app: choose **About EXO** from the menu bar icon, or open **Settings** › **General**;
- from source: run `uv run exo --version`.

The app and a source checkout number their versions differently. The app uses its release number (such as 1.0.71), while a source checkout uses the version in `pyproject.toml` (such as 0.3.70). Because the default [cluster name](#cluster-name) is the version, an app and a source checkout don't join each other by default. To mix them, give every device the same cluster name.

If a Mac doesn't show up:

- check that both Macs run the same version of exo;
- check that EXO is turned on in System Settings → Privacy & Security → Local Network on both Macs;
- guest Wi-Fi and some office networks stop devices from seeing each other: try Ethernet or a Thunderbolt cable instead;
- when exo sees another device that can't join (a different version or cluster name), it notes this in its log, `~/.exo/exo_log/exo.log`.

#### Updating

EXO checks for updates by itself and tells you when one is ready. You can also use **Check for Updates** in EXO's menu or Settings. A Homebrew installation updates itself the same way.

**Update every Mac in your cluster.** Devices running different versions of exo don't join each other, so a Mac you haven't updated yet drops out of the cluster until you update it too; the dashboard then shows "DEVICE ON ANOTHER EXO VERSION". Mixing versions in one cluster isn't supported.

From source, pull the latest code, rebuild the dashboard and run `uv sync` again, on every device.

#### Cluster name

Devices join each other only when they use the same cluster name (in the CLI, the "namespace") and run the same build of exo (see below). By default the cluster name is `exo`, in the app and from source, the same for every version of exo, so a device can say that another one runs a different version instead of not seeing it.

To run separate clusters on one network, for example a test cluster next to your main one, give each cluster its own name:

- in the app: open **Settings** › **Cluster** from the menu bar icon and fill in **Cluster name** (leave it on Automatic for the default);
- from source: run `uv run exo --namespace my-cluster`, or set `EXO_ZENOH_NAMESPACE=my-cluster`.

Devices also need the same *wire version*, a number exo bumps whenever what devices send each other changes, and the same *build*: the same app release, or for source builds the same exo package version and the same MLX and mlx-lm versions. Source builds of one package version are assumed to run the same exo code, so developers can run one checkout on several machines. A custom name doesn't override either, so devices with the same custom name but different versions of exo don't connect; before, they connected and then could stop making progress. A device that sees one under its cluster name logs "a device at … runs another version of exo" (or "another build") and lists it at `GET /v1/devices-on-other-versions`. The cluster name, wire version and build in use are logged at startup ("Discovery namespace: …"). A Mac and a Linux machine don't join each other, even on the same commit, because they run different builds of MLX. A Mac running exo from source and the Mac app at the same release don't join either, because the app names its own build.

#### Uninstalling the macOS app

The easiest way is in the app: click the EXO icon in the menu bar, open **Settings** › **General**, and click **Uninstall EXO…**. Enter your administrator password when asked. EXO then:

- removes its network setup service and the `exo` network location, switches your Mac back to the Automatic location and turns Thunderbolt Bridge back on;
- removes its login item;
- deletes its data folder, `~/.exo`, but keeps downloaded models in `~/.exo/models` unless you untick **Keep downloaded models**;
- moves EXO.app to the Trash.

If you've already deleted EXO.app, or removed it with Homebrew, run the uninstall script. You don't need a copy of this repository:

```bash
