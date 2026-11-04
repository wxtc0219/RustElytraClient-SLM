# RustElytraClient — SLM 甲飞接管补丁版（非官方）

> 给 **RustElytraClient beta1.6（baritone 版）** 增加第 4 个任务模式 **「SLM 甲飞接管」**，
> 用 **MagicBaritone + SlimefunHelper 甲飞** 驱动 baritone 的鞘翅寻路，**不需要穿戴鞘翅、不消耗鞘翅耐久**。
>
> ⚠️ 非官方补丁，与模组原作者无关。基于 GPL-3.0 发布，见 [LICENSE](LICENSE)。

- **产物**：`release/RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`
- **SHA-256**：`1E96D83A298A03A150DACB566A62E0FC2B7F4E744DD89E24A022BC6C2E6B8D1A`
- **兼容性**：**不绑定 SlimefunHelper 版本**（1.1.7.1 / 1.1.7.2 / 1.2.1.3 均已验证）
- **上游基线**：RustElytraClient `beta1.6`（GitHub 提交 `b7f60332`，2026-04-30，`beta (develop) 1.6 test!!!!`）
- **目标游戏**：Minecraft 1.21.1 + Fabric Loader

---

## 0. 整个情况概述（先读这段）

**背景**：RustElytraClient（简称 REC）是一个 baritone 鞘翅自动飞行模组（自动飞向坐标 + 自动补给）。原作者在 beta1.6 之后的新版本中**移除了 baritone 依赖**，改为自研寻路。而我们的需求是「**穿护甲飞、不穿鞘翅、不掉鞘翅耐久**」——这必须依靠 baritone 分支 **MagicBaritone** 把飞行物理替换为 SlimefunHelper 的甲飞（模拟 WASD/空格输入），所以只能基于 **beta1.6（baritone 版）** 做分支。

**做法**：不改上游源码，以官方 beta1.6 jar 为基线做 **ASM 二进制补丁**：
1. `TaskThread.TaskType` 新增 `SLM_TAKEOVER`（第 4 个模式）+ 菜单第 4 个按钮
2. **两处** `$SwitchMap` 映射（`RustElytraClient$1` 与 `RustSupplyTask$1`）→ 走 `INFINITY_ELYTRA` 分支（烟花补给目标 1664、不要求鞘翅、不自动紧急降落）
3. `RustElytraTask.RepairElytra` 仅 SLM 模式跳过，其余模式保持原版
4. 补给前置检查：SLM 模式改为「背包有鞘翅即可」，其余模式保持原版
5. 容器标题宽松匹配（去 `§`、双向包含）+ 等待容器界面 20→120 tick

**踩过并已修复的坑**（对后续维护者很重要）：
- `$SwitchMap` 是**每个类各自一份合成类**：只补 `RustElytraClient$1` 会漏掉 `RustSupplyTask$1`，表现为「补给任务开始后 1 秒直接进入飞行、完全不取物资」
- ASM `InsnList.insert(location, ...)` 会插到 location **之后**，必须用 `insertBefore`，否则补丁变成 `return` 之后的死代码（症状：任务瞬间跳过某阶段）

**当前状态（v1.0.0）**：实测可自动起飞、按段飞行、自动补给（日志可见 `所需补给:26组烟花,0组附魔之瓶/鞘翅`、`所需的潜影盒槽位列表：[3, 9]`）。已知限制：
- Grim 等反作弊服务器有周期性 `[AC] 反作弊回弹!`（服务器行为，参数只能降低频率，无法根除）
- 补给需要 **30 个以上熟猪排**（`FoodIndex: 4`），否则抛 `无可用熟猪排!` → 补给失败 → 自动退出
- 任务失败会触发 REC 原版自动退出；退出瞬间 REC 自身存在 NPE 崩溃的老 bug（与本补丁无关）

**性质**：非官方分支，GPL-3.0，与原作者无关。

---

## 1. 这是什么

原版 RustElytraClient（简称 REC）靠 baritone 的鞘翅寻路自动飞向目的地，但它的任务体系里有大量“必须穿戴耐久3/经验修补鞘翅”的检查。

本补丁给 REC 增加了第 4 个独立任务类型 `SLM_TAKEOVER`（界面里叫「开始飞行(SLM甲飞接管)」），它的飞行物理来自 **MagicBaritone（魔改男中音）**：把 baritone 原本的“真实滑翔物理”替换成“写假朝向 + 模拟 WASD/空格/Shift 按键”，由 **SlimefunHelper（SLM）的鞘翅甲飞 + 简易鞘翅控制** 实际执行运动。

因此：

| 模式 | 飞行物理 | 需要穿戴鞘翅？ | 掉鞘翅耐久？ |
| --- | --- | --- | --- |
| 原版 3 个按钮（鞘翅 / XP / 无尽鞘翅） | 原版真实滑翔 | **是**（且需耐久3+/经验修补） | 是（XP/无尽模式用附魔之瓶等方式维护） |
| **第 4 个：SLM甲飞接管** | SLM 甲飞（模拟输入） | **否**，背包里有鞘翅即可 | **否**（穿的是护甲） |

原版 3 个模式的行为**完全没有改动**（`RepairElytra`、补给前置检查都保留原作者逻辑）。

---

## 2. 依赖（缺一不可）

| 组件 | 版本要求 | 说明 |
| --- | --- | --- |
| Minecraft | **1.21.1** | Fabric |
| Fabric Loader | 0.20.x 可用 | 开发时使用 0.20.1 |
| **MagicBaritone** | `MagicBaritone-1.0.0-mc1.21.1-fabric.jar` | 提供甲飞驱动的 baritone 分支 |
| **SlimefunHelper** | **任意版本**（1.1.7.1 / 1.1.7.2 / 1.2.1.3 均验证可用） | 本补丁不引用 SH 任何类；MagicBaritone 作者推荐 1.1.7.2 |
| 原生 baritone | **必须移除** | `baritone-api-*.jar`、`baritone-helper-*.jar` 不能与 MagicBaritone 共存 |
| RustElytraClient | **本补丁版** | 覆盖原版 beta1.6 |

服务端环境：任意（甲飞对反作弊是否友好取决于服务器，见“已知问题”）。

### 兼容性说明（为什么是“全兼容”）

本补丁 jar 的 `fabric.mod.json` 只声明依赖 `fabricloader / minecraft ~1.21.1 / java >=21 / fabric-api`，
代码里**不引用 SlimefunHelper 的任何类**（只有按钮文案里出现 “SlimefunHelper” 字符串），
因此它天然不绑定 SlimefunHelper 版本——只要你的客户端装有 SLM 且甲飞功能可用，就能用。

真正和 SH 版本有耦合的是 **MagicBaritone**（飞行物理来源），经实测：

| SlimefunHelper | 结果 | 备注 |
| --- | --- | --- |
| 1.1.7.1 | ✅ 可用 | MB 作者最低要求附近 |
| 1.1.7.2 | ✅ 可用 | **MagicBaritone 作者官方推荐** |
| 1.2.1.3 | ✅ 可用 | 1.2.1 重构了 GUI/配置，但甲飞相关键位全部保留（23/23） |

甲飞相关配置键在 1.1.7.x 与 1.2.1.x 的差异（已逐键核对）：

- `elytra.armor-fly.*`：22 键 → 22 键（完全一致）
- `elytra.simple-flight-control.*`：33 → 34（+`auto-pull-up-mode-when-press-blank-only`）
- `elytra.custom-fireworks.*`：35 → 39（+`firework-max-delay-multiply-vanilla` 等）
- `elytra.unbreakable-elytra.*`：6 → 6
- 1.2.1 改名：`disabler.*` → `disablers.*`（9 → 20 键）
- 1.2.1 删除 37 个键，与飞行相关的仅 `travelling-control.pitch-40-*`、`render.no-world-bob-view`

---

## 3. 安装步骤

1. 关闭游戏。
2. 备份并删除 `mods/` 下所有 `baritone-api-*.jar`、`baritone-helper-*.jar`。
3. 放入 `MagicBaritone-1.0.0-mc1.21.1-fabric.jar`。
4. 放入本补丁 `RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`（若原来有 `RustElytraClient-*.jar` 先移走）。
5. 编辑 `baritone/settings.txt`（没有就新建），加入一行：

   ```
   slimePhysics false
   ```

   注意：文件必须是 **UTF-8 无 BOM**。这一行是 MagicBaritone 专属设置，原生 baritone 会因为不认识这行而在启动时报 `No setting by that name`。
6. 启动游戏，确认模组列表里是 **MagicBaritone** 而不是 Baritone。
7. 按 **Z** 打开「鞘翅甲飞 + 简易鞘翅控制」（SlimefunHelper 的 `elytra.armor-fly` 与 `elytra.simple-flight-control`，本包推荐热键为 Z，可在 SH 配置里改）。
8. 按 **`]`** 打开 REC 界面 → 填目的地 X / Z → 点第 4 个按钮 **「开始飞行(SLM甲飞接管)」**。

### 起飞前检查

- 背包里有**胸甲**（最好放快捷栏）与**鞘翅**（放快捷栏或副手；甲飞要求背包里存在鞘翅）
- 烟花充足（默认按 1 组烟花 / 5 组附魔之瓶的准备量）
- 挂机点在安全位置（避免落地/掉岩浆）

---

## 4. 本补丁改了什么（6 处字节码修改）

> 全部通过 ASM 写入，构建后使用 `Verify` 工具（ASM `BasicVerifier`）做栈一致性校验，全部 `OK`。

| # | 目标类 | 修改 | 作用 |
| --- | --- | --- | --- |
| 1 | `TaskThread$TaskType` | 新增枚举常量 `SLM_TAKEOVER`（`$values()` 扩容到 4、`<clinit>` 补构造） | 第 4 个任务类型 |
| 2 | `RustElytraClient$1` | `$SwitchMap$TaskType` 把 `SLM_TAKEOVER` 映射到 ELYTRA 分支 | 复用原版任务流程（补给/分段/寻路） |
| 3 | `RSTScr$ciScr` | 菜单由 5 项扩到 6 项，新增第 4 个按钮「开始飞行(SLM甲飞接管)」，lambda 捕获 `this` | 界面入口 |
| 4 | `RustElytraTask.RepairElytra` | 方法开头插入 `if (T.isSlm()) return;`，其它模式保持原版 | SLM 模式跳过“修鞘翅/必须穿鞘翅”流程 |
| 5 | `RustSupplyTask.SortAndCheckInv`（含 lambda） | 补给前置守卫改调 `T.elytraOk(wornOk)`：其它模式 = 原版；SLM = 背包里有鞘翅即可 | 不再强制穿戴附魔鞘翅 |
| 6 | `dev/rstminecraft/T`（新增辅助类） | `eq()` 容器标题宽松匹配、`isSlm()`、`hasElytra()`、`elytraOk()`、`repairGuard()` | 运行时判定 |

辅助类 `T.hasElytra()` 用**反射**遍历玩家背包 0–40 格查找 `Items.ELYTRA`（intermediary 名：`class_310` / `class_1802.field_8833` / `method_31548` / `method_5438`），因此不依赖编译期 Minecraft 类。

补丁源码见 [`patches/src`](patches/src)，构建脚本见 [`tools/build-release.ps1`](tools/build-release.ps1)。

---

## 5. 如何自己构建（可选，GPL 合规所需）

需要：JDK 21、ASM 9.10.1、官方 `RustElytraClient-1.21.1-beta1.6-*.jar`、Python 3。

```powershell
# 1. 编译补丁工具（需要 asm / asm-tree / asm-analysis 9.10.1 在 classpath）
javac -encoding UTF-8 -cp "asm-9.10.1.jar;asm-tree-9.10.1.jar;asm-analysis-9.10.1.jar" -d out patches/src/*.java
# 2. 用官方 beta1.6 jar 作为 base，按 tools/build-release.ps1 的流程依次打补丁
# 3. 产物 SHA-256 应为 1E96D83A...6B8D1A
```

---

## 6. 已知问题

1. **服务器反作弊回弹**：在 GrimAC 等严格反作弊的服务器上，甲飞期间会周期性出现 `[AC] 反作弊回弹!`（位置被拉回一点点，观感顿挫）。这是服务器对“护甲滑翔”的移动预测不信任导致的，**参数只能降低频率，不能根除**。追求完全平滑请使用原版 3 个模式 + 真实鞘翅。
2. **MagicBaritone 已停止维护**（作者原话：as-is，不给支持）。其 README 推荐 **SlimefunHelper 1.1.7.2**；实测 1.1.7.1 / 1.2.1.3 也能用，但参数行为可能有细微差异。
3. 上游作者的新版本已移除 baritone 依赖，本补丁**只针对 beta1.6**，不能用于新版 REC。
4. 需要末影箱内物资（烟花/附魔之瓶/鞘翅）满足补给计算，否则任务会以“末影箱中物资不足”失败并触发自动退出。
5. 与替代版 baritone（如 Meteor 内置）不兼容。

---

## 7. 授权与致谢

- 本项目是 **RustElytraClient** 的衍生作品，原项目：<https://github.com/RSTminecraft/RustElytraClient>，许可证 **GPL-3.0**（完整 LICENSE 见本仓库根目录）。
- 原项目声明部分核心代码来自 **Baritone (meteor)**，同样受 GPLv3 保护。
- 本补丁不包含、不修改 MagicBaritone 的代码；MagicBaritone 为 **LGPL-3.0**：<https://github.com/Alastorbaby/MagicBaritone>
- 致谢：RSTminecraft（RustElytraClient）、cabaletta（Baritone）、Alastorbaby 与 大肥鱼（MagicBaritone）、SlimefunHelper 作者。

**免责声明**：仅供技术研究与学习使用。在任何服务器上使用本补丁可能违反该服务器规则并导致封禁，后果由使用者自负。

---

## 8. 文件清单

```
LICENSE                                  GPL-3.0 全文（上游仓库原文件）
README.md                                本说明（含「整个情况概述」）
UPLOAD.md                                上传到 GitHub 的完整操作说明（给执行上传的人/AI）
RELEASE_NOTES.md                         Release 正文模板（可直接粘贴）
安装说明.md                               安装/使用/物资准备/排查（给用户）
宣发文案.md                               视频标题、简介、演示流程、标签
第三方声明与许可.md                        各组件许可证与 GPL 合规说明
CHECKSUMS.txt                            全部文件 SHA-256
release/
  RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar   补丁产物
  SHA256SUMS.txt
deps/                                    必要依赖（3 个 jar，可随 Release 一起发）
  MagicBaritone-1.0.0-mc1.21.1-fabric.jar
  SlimefunHelper-1.21.1-1.1.7.2.jar
  fabric-api-0.116.17+1.21.1.jar
config/                                  推荐配置
  RSTConfig.json                         （FoodIndex 4 = 熟猪排、elytraFireworkSpeed 1.2 等）
baritone/settings.txt                    巴里通配置（含 slimePhysics false）
slimefunhelper/runtime/*.yml             SlimefunHelper 1.1.7.2 运行时配置（13 个，含 Z 热键/甲飞参数）
patches/src/*.java                       全部补丁源码（ASM 树 API，GPL 合规所需）
tools/build-release.ps1                  完整构建流程
tools/repack3.py                         jar 内多文件替换打包脚本
licenses/                                MagicBaritone LGPL-3.0 原文（GPL-3.0 在根目录 LICENSE）
docs/改动说明.md                          每处修改的技术细节
docs/上游信息.md                          上游仓库/许可证/提交信息
```
