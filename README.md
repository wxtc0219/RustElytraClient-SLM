# RustElytraClient — SLM 甲飞接管补丁版（非官方，多版本）

> 给 **RustElytraClient beta1.6（baritone 版）** 增加第 4 个任务模式 **「SLM 甲飞接管」**，
> 用 **MagicBaritone + SlimefunHelper 甲飞** 驱动 baritone 的鞘翅寻路，**不需要穿戴鞘翅、不消耗鞘翅耐久**。
>
> 支持 **Minecraft 1.21.1 / 1.21.4 / 1.21.11** 三个主流版本。
>
> ⚠️ 非官方补丁，与模组原作者无关。基于 GPL-3.0 发布，见 [LICENSE](LICENSE)。
>
> 🎬 演示视频【Slime甲飞+RustElytra 全自动不消耗鞘翅耐久跑图】 https://www.bilibili.com/video/BV1JwxR6DEun/

---

## 产物一览

### 补丁本体（三选一，按你的 MC 版本选）

| 文件 | 适用 MC | 说明 |
| --- | --- | --- |
| `release/RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar` | **1.21.1** | 基于 REC `1.21.1` 分支 beta1.6 源码重编译 |
| `release/RustElytraClient-1.21.4-beta1.6-slm-takeover-1.0.0.jar` | **1.21.4** | 基于 REC `1.21.4` 分支 beta1.6 源码重编译 |
| `release/RustElytraClient-1.21.11-beta1.6-slm-takeover-1.0.0.jar` | **1.21.11** | 基于 REC `1.21.8` 分支 beta1.6 源码移植到 1.21.11 |

### 飞行物理依赖（必须，按 MC 版本选）

| 文件 | 适用 MC | 来源 |
| --- | --- | --- |
| `deps/MagicBaritone-1.0.0-mc1.21.1-fabric.jar` | **1.21.1** | Alastorbaby 官方发布版（原版） |
| `deps/MagicBaritone-1.0.0-mc1.21.4-fabric.jar` | **1.21.4** | 本分支自行移植（baritone 1.21.4 + 甲飞补丁，未混淆版） |
| `deps/MagicBaritone-1.0.0-mc1.21.11-fabric.jar` | **1.21.11** | 本分支自行移植（baritone 1.21.11 + 甲飞补丁，未混淆版，内嵌 nether-pathfinder） |

> 1.21.4 / 1.21.11 的 MagicBaritone 是**未做 proguard 混淆**的移植版（类名可读），
> 这样才能让 REC 的 mixin 正确挂到 `baritone.behavior.LookBehavior` 等类上；
> 代价是体积比官方 1.21.1 版大一些（属正常）。

> MagicBaritone 是 baritone 的分支，**不能和原版 baritone 同时安装**（`baritone-*.jar` 全部移走）。

### 其它依赖（`deps/` 内也已附带）

| 组件 | 1.21.1 | 1.21.4 | 1.21.11 |
| --- | --- | --- | --- |
| Fabric API | `fabric-api-0.116.17+1.21.1.jar` | `fabric-api-0.110.0+1.21.4.jar` | `fabric-api-0.140.0+1.21.11.jar` |
| SlimefunHelper | `1.1.7.2`（推荐） | `1.1.7.1`（该版本唯一 1.1.7.x） | `1.1.7.2`（推荐）/ `1.2.1.3` 也可 |
| Java | 21+ | 21+ | 21+ |

> **同一时间只能放一个 SlimefunHelper 版本**。

---

## 0. 整个情况概述（先读这段）

**背景**：RustElytraClient（简称 REC）是一个 baritone 鞘翅自动飞行模组（自动飞向坐标 + 自动补给）。
原作者在 beta1.6 之后的新版本中**移除了 baritone 依赖**，改为自研寻路（1.21.11 的新版就是这种）。
而我们的需求是「**穿护甲飞、不穿鞘翅、不掉鞘翅耐久**」——这必须依靠 baritone 分支
**MagicBaritone** 把飞行物理替换为 SlimefunHelper 的甲飞（模拟 WASD/空格输入），
所以只能基于 **beta1.6（baritone 版）** 做分支。

**三个版本的实现方式**：

- **1.21.1 / 1.21.4**：REC 官方 beta1.6 源码分支本身就用 baritone，直接加第 4 模式、重编译。
- **1.21.11**：官方 REC 新版已经不用 baritone 了，本分支把 **REC 1.21.8 分支（baritone 版）的源码**
  移植到 1.21.11 API 上，再套用同一套「SLM 甲飞接管」改动。
  代价：**1.21.11 版的轨迹预览渲染已停用**（新渲染 API 大改，且只影响可视预览，不影响飞行/补给）。

**MagicBaritone 1.21.4 / 1.21.11**：Alastorbaby 只发布了 1.21.1 的 MagicBaritone。
本分支把它的「甲飞接管物理补丁」移植到了
[baritone 官方 1.21.4 / 1.21.11 分支](https://github.com/cabaletta/baritone) 上重新编译，
补丁源码见 `patches/magicbaritone/`。

**性质**：非官方分支，GPL-3.0，与原作者无关。

---

## 1. 这是什么

原版 REC 靠 baritone 的鞘翅寻路自动飞向目的地，但它的任务体系里有大量
“必须穿戴耐久3/经验修补鞘翅”的检查。

本补丁给 REC 增加了第 4 个独立任务类型 `SLM_TAKEOVER`（界面里叫「开始飞行(SLM甲飞接管)」），
它的飞行物理来自 **MagicBaritone（魔改男中音）**：把 baritone 原本的“真实滑翔物理”替换成
“写假朝向 + 模拟 WASD/空格/Shift 按键”，由 **SlimefunHelper（SLM）的鞘翅甲飞 + 简易鞘翅控制** 实际执行运动。

因此：

| 模式 | 飞行物理 | 需要穿戴鞘翅？ | 掉鞘翅耐久？ |
| --- | --- | --- | --- |
| 原版 3 个按钮（鞘翅 / XP / 无尽鞘翅） | 原版真实滑翔 | **是**（且需耐久3+/经验修补） | 是（XP/无尽模式用附魔之瓶等方式维护） |
| **第 4 个：SLM甲飞接管** | SLM 甲飞（模拟输入） | **否**，背包里有鞘翅即可 | **否**（穿的是护甲） |

原版 3 个模式的行为**完全没有改动**。

---

## 2. 安装步骤（三版本通用）

1. **关闭游戏**。
2. 备份并删除 `mods/` 下所有 `baritone-api-*.jar`、`baritone-helper-*.jar`（原版 baritone 不能与 MagicBaritone 共存）。
3. 按你的 MC 版本放入对应文件：
   - `release/RustElytraClient-<MC版本>-beta1.6-slm-takeover-1.0.0.jar`
   - `deps/MagicBaritone-1.0.0-mc<MC版本>-fabric.jar`
   - `deps/SlimefunHelper-<MC版本>-<版本>.jar`（只能放一个）
   - `deps/fabric-api-<对应版本>.jar`
   - 若原来有 `RustElytraClient-*.jar` 先移走（只能有一个 REC）。
4. 复制配置：
   - `config/RSTConfig.json` → `.minecraft/config/RSTConfig.json`
   - `baritone/settings.txt` → `.minecraft/baritone/settings.txt`
   - `slimefunhelper/runtime/` 下的 yml → `.minecraft/slimefunhelper/runtime/`
   - `slimefunhelper/config/*.nbt` → `.minecraft/slimefunhelper/config/`（MagicBaritone 推荐参数快照）
5. 启动游戏，确认模组列表里是 **MagicBaritone** 而不是 Baritone。
6. 按 **Z** 打开「鞘翅甲飞 + 简易鞘翅控制」（SlimefunHelper 模块，本包推荐热键为 Z）。
7. 按 **`]`** 打开 REC 界面 → 填目的地 X / Z → 点第 4 个按钮 **「开始飞行(SLM甲飞接管)」**。

> `baritone/settings.txt` 里必须有一行 `slimePhysics false`（UTF-8 无 BOM），
> 这是 MagicBaritone 的甲飞接管开关；本包已附带，直接覆盖即可。

### 起飞前检查

- 背包里有**胸甲**（最好放快捷栏）与**鞘翅**（放快捷栏或副手；甲飞要求背包里存在鞘翅）
- 烟花充足（甲飞模式按 26 组准备）
- 挂机点在安全位置（避免落地/掉岩浆）

---

## 3. 本补丁改了什么

### 3.1 第 4 模式（三版本一致，源码级改动）

1. `TaskThread.TaskType` 新增 `SLM_TAKEOVER` + 菜单第 4 个按钮
2. 补给逻辑：`SLM_TAKEOVER` 走「无尽鞘翅」那套（烟花目标 1664 = 26 组、不要求鞘翅耐久）
3. 补给前置检查：SLM 模式不再强制“穿戴耐久3经验修补鞘翅”
4. `RustElytraTask.RepairElytra`：SLM 模式跳过（甲飞不修鞘翅）
5. 起飞逻辑：SLM 模式单独实现（双击空格起跳 + 连续失败改烟花起飞），并修复了原版
   `jumpingCounter` 滑动窗口导致「起飞失败要卡 5 分钟才重试」的问题
6. 容器标题宽松匹配（去 `§`、双向包含）+ 等待容器界面 20→120 tick

### 3.2 本次顺带修好的老问题

- **`无可用熟猪排!` 直接整段失败** → 末影箱里没有食物时只警告，用身上现有食物继续
- **`挖掘异常？取消挖掘`（挖补给盒 2 秒超时）** → 先关闭容器界面，超时放宽到 30 秒，
  再不行直接用手挖兜底
- **容器标题匹配失败** → 宽松匹配（兼容服务器给容器名加前后缀）

### 3.3 MagicBaritone 1.21.4 / 1.21.11

在 baritone 官方分支上重新应用 MagicBaritone 的“甲飞接管物理”补丁：
`Settings` 4 个 `slime*` 设置、`#slime` 命令、`ElytraBehavior` 甲飞驾驶逻辑、
3 个 mixin（按键接管 / 假朝向还原 / 视角还原）。

---

## 4. 已知问题 / 限制

- **1.21.11 版没有轨迹预览渲染**（只影响可视轨迹线，不影响飞行和补给）
- 1.21.4 / 1.21.11 的 MagicBaritone 为**未混淆移植版**（类名可读），体积比 1.21.1 官方版大，属正常现象
- 1.21.4 / 1.21.11 的 MagicBaritone 是**本分支移植版**，未必 100% 等价于作者 1.21.1 版的行为；
  遇到问题请记录日志反馈
- 1.21.11 的 REC 是**1.21.8 分支源码移植**，界面/提示与官方 1.21.11 新版（beta1.9.x）不同
- Grim 等反作弊服务器有周期性 `[AC] 反作弊回弹!`（服务器行为，参数只能降低频率，无法根除）
- 任务失败会触发 REC 原版自动退出；退出瞬间 REC 自身存在 NPE 崩溃的老 bug（与本补丁无关）
- **补给需要 30 个以上熟猪排**（`FoodIndex: 4`）；末影箱里没有时会警告并继续

---

## 5. 目录结构

```
RustElytraClient-SLM/
├── release/            # 三个版本的补丁 jar
├── deps/               # MagicBaritone / SlimefunHelper / Fabric API
├── config/             # REC 配置
├── baritone/           # baritone settings.txt（slimePhysics false）
├── slimefunhelper/     # SH runtime yml + 推荐参数 nbt
├── patches/            # 源码级改动（REC 三版本 + MagicBaritone 移植）
├── docs/验证记录.md     # 发布前的静态/运行时检查记录
├── licenses/           # 第三方许可证
├── docs/               # 安装说明 · 史莱姆参数说明 · 宣发文案 · 第三方声明与许可 · Release Notes
├── README.md
└── LICENSE             # GPL-3.0
```

---

## 6. 许可证与致谢

- 本项目是 **RustElytraClient** 的衍生作品，原项目：
  <https://github.com/RSTminecraft/RustElytraClient>，许可证 **GPL-3.0**（完整 LICENSE 见根目录）。
- MagicBaritone 为 **LGPL-3.0**：<https://github.com/Alastorbaby/MagicBaritone>；
  1.21.4 / 1.21.11 版本由本项目从 <https://github.com/cabaletta/baritone>（LGPL-3.0）
  对应分支移植甲飞补丁后重新编译，补丁见 `patches/magicbaritone/`。
- SlimefunHelper（CC0-1.0）与 Fabric API 为独立依赖，仅原样附带。
- 致谢：RSTminecraft（RustElytraClient）、cabaletta（Baritone）、Alastorbaby 与 大肥鱼（MagicBaritone）、SlimefunHelper 作者。
