# 在3c3u中使用 RustElytraClient — SLM 甲飞接管扩展版（非官方）

给 **RustElytraClient beta1.6（baritone 版）** 加了第 4 个任务模式「SLM 甲飞接管」：
用 **MagicBaritone + SlimefunHelper 甲飞** 驱动飞行，**不用穿鞘翅、不掉鞘翅耐久**。

- 产物：`release/RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`
- SHA-256：`1E96D83A298A03A150DACB566A62E0FC2B7F4E744DD89E24A022BC6C2E6B8D1A`
- 上游基线：RustElytraClient `1.21.1` 分支 / `beta1.6`，提交 `e5ec472a`（2026-04-30）
- 游戏：Minecraft **1.21.1** + Fabric Loader，Java 21
- ⚠️ 非官方扩展，与原作者无关，基于 GPL-3.0 发布（见 [LICENSE](LICENSE)）
- 代码与文档：**未汐甜茶**（[@wxtc0219](https://github.com/wxtc0219)）与 **大肥鱼（DeepSeek）** 一并完成

---

演示视频【Slime甲飞+RustElytra 全自动不消耗鞘翅耐久跑图】 https://www.bilibili.com/video/BV1JwxR6DEun/?share_source=copy_web&vd_source=360c40ae2f77088d0831582c40221f78

> 文档都在 [`docs/`](docs/)：安装说明 · 参数说明 · 改动说明 · 上游信息 · 宣发文案 · Release Notes

## 装什么（4 个 jar，缺一不可）

| 组件 | 版本 | 上哪拿 |
| --- | --- | --- |
| 本扩展 | `RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar` | 本仓库 `release/` |
| MagicBaritone | `MagicBaritone-1.0.0-mc1.21.1-fabric.jar` | 见 [`deps/README.md`](deps/README.md) |
| SlimefunHelper | `1.1.7.2`（1.21.1 构建）| 见 [`deps/README.md`](deps/README.md) |
| Fabric API | `0.116.17+1.21.1` | 见 [`deps/README.md`](deps/README.md) |

**mods 里不能同时有原生 baritone**：`baritone-api-*.jar`、`baritone-helper-*.jar` 必须删掉。
本扩展不引用 SlimefunHelper 任何类，SH 1.1.7.x / 1.2.1.x 都能用（真正跟 SH 版本耦合的是 MagicBaritone）。

## 怎么装

1. 关游戏。
2. 删掉 mods 里所有 `baritone-api-*.jar`、`baritone-helper-*.jar`；原来的 `RustElytraClient-*.jar` 也移走。
3. 把上面 4 个 jar 放进 `.minecraft/mods/`。
4. `baritone/settings.txt` 里加一行 `slimePhysics false`（**UTF-8 无 BOM**；这是 MagicBaritone 独有设置，原生 baritone 会报 `No setting by that name`）。
5. 把仓库里的配置放好：`config/RSTConfig.json`、`baritone/settings.txt`、`slimefunhelper/runtime/*.yml`。
6. 进游戏确认模组列表是 **MagicBaritone**（不是 Baritone）。

**用**：按 `Z` 开 SH 的「鞘翅甲飞 + 简易鞘翅控制」→ 按 `]` 开 REC 填 X/Z → 点第 4 个按钮「开始飞行(SLM甲飞接管)」。

**起飞前**：背包里有胸甲（快捷栏）和鞘翅（甲飞只要求背包存在）、烟花够（默认 26 组）、**熟猪排 30 个以上**（`FoodIndex: 4`，不够会 `无可用熟猪排!` 直接中止）。

完整版细节见 [`安装说明.md`](docs/安装说明.md)。

## 本扩展改了什么

以官方 beta1.6 jar 为基线做 ASM 二进制补丁，**不改上游源码**；交付出去的产物是一个完整的 Fabric 模组（插件），装上就能用：

1. `TaskThread.TaskType` 加 `SLM_TAKEOVER` + 菜单第 4 个按钮
2. 两处 `$SwitchMap`（`RustElytraClient$1`、`RustSupplyTask$1`）指向 `INFINITY_ELYTRA` 分支
3. `RepairElytra` 仅 SLM 模式跳过，其余模式原样
4. 补给前置检查：SLM 模式只要求「背包有鞘翅」
5. 容器标题宽松匹配 + 等界面 20→120 tick

原版 3 个模式的行为完全没动。改法细节见 [`docs/改动说明.md`](docs/改动说明.md)。

## 已知问题

- 反作弊服务器（如 Grim）会周期性弹 `[AC] 反作弊回弹!`，属于服务器行为，压不下去。
- 烟花/食物不够会中止任务并自动退出（原作者设计）。
- 退出瞬间 REC 本身有个 NPE 老 bug，与本扩展无关。

## 授权与致谢

- 本扩展的代码与文档由 **未汐甜茶** 与 **大肥鱼（DeepSeek）** 一并完成。

- 上游：[RSTminecraft/RustElytraClient](https://github.com/RSTminecraft/RustElytraClient)（GPL-3.0），本仓库是其非官方衍生分支，同协议发布。
- 上游依赖演变：早期用 Meteor 构建的 baritone（`meteordevelopment:baritone`）+ `nether-pathfinder`；新版移除 baritone，改为作者自研 `dev.rstminecraft:RustClientCore`（内嵌）+ `nether-pathfinder`。本扩展基于仍然依赖 baritone 的 1.21.1 / beta1.6。
- [MagicBaritone](https://github.com/Alastorbaby/MagicBaritone)（LGPL-3.0，Baritone 1.11.2 分支，飞行物理换成 SH 甲飞）
- [SlimefunHelper](https://github.com/m1919810/SlimefunHelper)（CC0-1.0）
- [Baritone](https://github.com/cabaletta/baritone)（LGPL-3.0，上游）

第三方许可全文见 [`第三方声明与许可.md`](docs/第三方声明与许可.md) 与 [`licenses/`](licenses/)。

## 免责（务必看）

- 这是**非官方民间扩展，可能有 bug**：飞歪、卡段、补给失败、任务中途中断，极端情况下掉装备/掉鞘翅/掉图腾。
- 只在**你自己能承担损失的号**上用。别拿贵重号去试。
- 在服务器上使用可能违反服务器规则、被判作弊封号，**后果自负**。
- 出问题带 `.minecraft/logs/latest.log` 来提 issue；上游原作者不负责这个分支。
