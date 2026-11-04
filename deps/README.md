# 依赖下载（本仓库不放第三方 jar）

三个第三方 jar 不在仓库里，自己下，和 `release/` 的补丁 jar 一起放进 `.minecraft/mods/`，四个缺一不可。

| 文件 | 版本要对上 | 下载 | 许可证 |
| --- | --- | --- | --- |
| `MagicBaritone-1.0.0-mc1.21.1-fabric.jar` | MC 1.21.1 / Fabric（mod 内部版本 `baritone 1.11.2`）| <https://github.com/Alastorbaby/MagicBaritone/releases> | LGPL-3.0 |
| `SlimefunHelper-1.21.1-1.1.7.2.jar` | MC 1.21.1（`slimefunhelper 1.1.7.2`，别拿 1.21.11 的）| <https://github.com/m1919810/SlimefunHelper/releases> | CC0-1.0 |
| `fabric-api-0.116.17+1.21.1.jar` | `0.116.17+1.21.1` | <https://modrinth.com/mod/fabric-api/versions?g=1.21.1> | Apache-2.0 |

补丁产物在 `release/`：`RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`（校验见 `release/SHA256SUMS.txt`）。

装完的样子：

```
.minecraft/mods/  ← 上面 4 个 jar
.minecraft/config/RSTConfig.json          ← 仓库 config/
.minecraft/baritone/settings.txt          ← 仓库 baritone/（UTF-8 无 BOM，含 slimePhysics false）
.minecraft/slimefunhelper/runtime/*.yml   ← 仓库 slimefunhelper/runtime/
```

要 Minecraft **1.21.1**、Fabric Loader ≥ 0.16、Java **21**；mods 里不能留原生 `baritone-api-*.jar`。
详细步骤看 [`安装说明.md`](../安装说明.md)。
