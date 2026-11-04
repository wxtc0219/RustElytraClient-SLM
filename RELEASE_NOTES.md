# v1.0.0 — SLM 甲飞接管补丁（非官方）

> 非官方补丁，基于 [RustElytraClient](https://github.com/RSTminecraft/RustElytraClient) **beta1.6**（提交 `b7f60332`），GPL-3.0。
> 与模组原作者无关。

## 这是什么

给 RustElytraClient 增加第 4 个任务模式 **「开始飞行(SLM甲飞接管)」**：
用 **MagicBaritone**（甲飞驱动的 baritone 分支）接管 baritone 的鞘翅寻路，实际运动由 **SlimefunHelper** 的鞘翅甲飞 + 简易鞘翅控制执行。

- ❌ 不需要穿戴鞘翅（背包里有鞘翅即可）
- ❌ 不消耗鞘翅耐久（飞行时穿的是护甲）
- ✅ 保留原版 3 个模式（鞘翅 / XP / 无尽鞘翅）的原始行为不变
- ✅ 自动补给：按段检查烟花，不足时自动开末影箱取物资

## 本版改动（相对官方 beta1.6）

1. 新增枚举 `TaskThread.TaskType.SLM_TAKEOVER`（第 4 个模式，界面第 4 个按钮）
2. `$SwitchMap` 映射（`RustElytraClient$1` 与 `RustSupplyTask$1` **两处**）→ 走 `INFINITY_ELYTRA` 分支：
   - 补给目标：烟花 1664（不要求鞘翅）
   - 关闭自动紧急降落
3. `RustElytraTask.RepairElytra`：仅当当前为 SLM 模式时跳过（其余模式保留原版修鞘翅逻辑）
4. `RustSupplyTask` 补给前置检查：SLM 模式改为「背包中有鞘翅即可」，其余模式保持原版
5. 容器标题宽松匹配（去 `§` 颜色码、包含匹配）+ 等待容器界面 20→120 tick（提升服务端/插件改名兼容性）
6. 新增辅助类 `dev.rstminecraft.T`（`eq` / `isSlm` / `hasElytra` / `elytraOk`）

## 依赖

| 组件 | 要求 |
| --- | --- |
| Minecraft | **1.21.1** + Fabric（Loader 0.16+，Fabric API） |
| **MagicBaritone** | `MagicBaritone-1.0.0-mc1.21.1-fabric.jar`（必需；原生 baritone 必须移除） |
| **SlimefunHelper** | 任意版本（1.1.7.1 / 1.1.7.2 / 1.2.1.3 均验证可用；MB 官方推荐 1.1.7.2） |
| 原生 baritone | **删除**（`baritone-api-*.jar` / `baritone-helper-*.jar` 不可与 MB 共存） |

## 安装要点

1. 关闭游戏，删除原生 baritone
2. `mods/` 放入 MagicBaritone + 本 jar
3. `baritone/settings.txt` 加一行 `slimePhysics false`（UTF-8 无 BOM）
4. 游戏内按 **Z** 开启「鞘翅甲飞 + 简易鞘翅控制」
5. 按 **`]`** 打开界面 → 填目的 X/Z → 点第 4 个按钮

详细步骤见仓库 README。

## 已知问题

- **服务器反作弊回弹**：Grim 等严格反作弊服务器上，甲飞期间会周期出现 `[AC] 反作弊回弹!`，观感有轻微顿挫。属服务器行为，参数只能降低频率、无法根除。
- 上游作者新版已移除 baritone，本补丁**仅适用于 beta1.6**。
- MagicBaritone 已停止维护（as-is）。
- 需要末影箱内含足够烟花，否则补给会因物资不足失败并触发自动退出。

## 校验

```
SHA-256 (RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar)
= 1E96D83A298A03A150DACB566A62E0FC2B7F4E744DD89E24A022BC6C2E6B8D1A
```

## 授权

GPL-3.0（衍生自 RustElytraClient，上游同协议）。
致谢：RSTminecraft（RustElytraClient）、cabaletta（Baritone）、Alastorbaby / 大肥鱼（MagicBaritone）、SlimefunHelper 作者。

仅供技术研究与学习使用；在服务器上使用可能违反该服务器规则，后果自负。
