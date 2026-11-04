# v1.0.0 — SLM 甲飞接管补丁（非官方，多版本）

> 非官方补丁，基于 [RustElytraClient](https://github.com/RSTminecraft/RustElytraClient) **beta1.6**（baritone 分支），GPL-3.0。
> 与模组原作者无关。

## 这是什么

给 RustElytraClient 增加第 4 个任务模式 **「开始飞行(SLM甲飞接管)」**：
用 **MagicBaritone**（甲飞驱动的 baritone 分支）接管 baritone 的鞘翅寻路，实际运动由 **SlimefunHelper** 的鞘翅甲飞 + 简易鞘翅控制执行。

- ❌ 不需要穿戴鞘翅（背包里有鞘翅即可）
- ❌ 不消耗鞘翅耐久（飞行时穿的是护甲）
- ✅ 保留原版 3 个模式（鞘翅 / XP / 无尽鞘翅）的原始行为不变
- ✅ 自动补给：按段检查烟花，不足时自动开末影箱取物资
- ✅ **一次发布，三个 MC 版本**：1.21.1 / 1.21.4 / 1.21.11

## 本版改动（相对官方 beta1.6）

### 第 4 模式

1. 新增枚举 `TaskThread.TaskType.SLM_TAKEOVER`（第 4 个模式，界面第 4 个按钮）
2. 补给/替换槽位分支：SLM 模式走 `INFINITY_ELYTRA` 那套
   - 补给目标：烟花 1664（= 26 组，不要求鞘翅）
   - 关闭自动紧急降落
3. `RustElytraTask.RepairElytra`：SLM 模式跳过（甲飞不修鞘翅）
4. `RustSupplyTask` 补给前置检查：SLM 模式不再强制“穿戴耐久3经验修补鞘翅”
5. 容器标题宽松匹配（去 `§` 颜色码、双向包含）+ 等待容器界面 20→120 tick

### 起飞 / 补给稳定性修复（原版老 bug）

6. **SLM 模式专用起飞**：双击空格起跳；连续失败 3 次改用烟花起飞。
   修掉了原版 `jumpingCounter` 是 100 tick 滑动窗口、起飞失败时窗口会漏空，
   导致**要卡 5 分钟才重试**的问题。
7. **`挖掘异常？取消挖掘` 修复**：挖补给盒前先关闭容器界面，超时 2 秒 → 30 秒，
   再不行直接用手挖兜底。
8. **`无可用熟猪排!` 修复**：末影箱里没有食物时只警告，用身上现有食物继续，不再整段任务失败。

### 多版本支持

9. **1.21.1 / 1.21.4**：基于官方 beta1.6 对应分支源码重新编译（源码级补丁，不是字节码补丁）。
10. **1.21.11**：官方新版已移除 baritone，因此把 **beta1.6 的 1.21.8 分支源码移植到 1.21.11**
    再套用同一套改动；**该版本轨迹预览渲染停用**。
11. **MagicBaritone 1.21.4 / 1.21.11**：把 Alastorbaby 的甲飞补丁移植到
    [cabaletta/baritone](https://github.com/cabaletta/baritone) 对应分支重新编译，
    补丁见 `patches/magicbaritone/`；移植版为**未混淆**构建（类名可读，保证 REC mixin 能挂上），体积略大。

## 依赖

| 组件 | 1.21.1 | 1.21.4 | 1.21.11 |
| --- | --- | --- | --- |
| Minecraft | 1.21.1 + Fabric | 1.21.4 + Fabric | 1.21.11 + Fabric |
| **MagicBaritone** | `mc1.21.1` 官方版 | `mc1.21.4` 本分支移植 | `mc1.21.11` 本分支移植 |
| **SlimefunHelper** | 1.1.7.2（推荐） | 1.1.7.1 | 1.1.7.2 / 1.2.1.3 |
| 原生 baritone | **删除**（不可与 MagicBaritone 共存） | 同左 | 同左 |
| Fabric API | 0.116.17+1.21.1 | 0.110.0+1.21.4 | 0.140.0+1.21.11 |
| Java | 21+ | 21+ | 21+ |

## 安装要点

1. 关闭游戏，删除原生 baritone
2. `mods/` 放入对应版本的 MagicBaritone + REC 补丁 + SlimefunHelper + Fabric API（**4 个 jar**）
3. `baritone/settings.txt` 加一行 `slimePhysics false`（UTF-8 无 BOM）
4. 按 Z 打开甲飞模块 → 按 `]` 打开 REC 菜单 → 填坐标 → 第 4 个按钮

## 已知问题

- 1.21.11 版轨迹预览渲染停用
- 1.21.4 / 1.21.11 的 MagicBaritone 为本分支移植版，行为未必 100% 等价于 1.21.1 官方版
- Grim 服有周期性 `[AC] 反作弊回弹!`（服务器行为）
- 任务失败会触发 REC 原版自动退出；退出瞬间 REC 自身有 NPE 崩溃老 bug（与本补丁无关）
- 补给需要 30 个以上熟猪排；末影箱没有时只警告继续

## 兼容性

| 组合 | 结果 |
| --- | --- |
| MC 1.21.1 + MB 1.21.1 + SH 1.1.7.2 | ✅ 实测 |
| MC 1.21.4 + MB 1.21.4(本移植) + SH 1.21.4-1.1.7.1 | 🧪 待实测 |
| MC 1.21.11 + MB 1.21.11(本移植) + SH 1.21.11-1.1.7.2 / 1.2.1.3 | 🧪 待实测 |

## 许可证

GPL-3.0（上游 RustElytraClient 同许可证）。MagicBaritone 为 LGPL-3.0，SlimefunHelper 为 CC0-1.0。
