#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 RustElytraClient（baritone 版，1.21.1 / 1.21.4 源码结构相同）加第 4 个任务模式「SLM 甲飞接管」，
并顺带修好补给任务里“挖补给盒超时”和容器标题匹配的老问题。

用法: python patch_rec_slm.py <REC 源码根目录>
"""
import os
import re
import sys

root = sys.argv[1]
J = os.path.join(root, 'src/main/java/dev/rstminecraft')


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)


def sub1(s, old, new, tag):
    assert old in s, '[MISS] ' + tag
    assert s.count(old) == 1, '[MULTI] ' + tag
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- TaskThread
p = os.path.join(J, 'TaskThread.java')
s = read(p)
s = sub1(s,
         '    public enum TaskType {\n'
         '        EXP_BOTTLE, ELYTRA, INFINITY_ELYTRA\n'
         '    }',
         '    public enum TaskType {\n'
         '        EXP_BOTTLE, ELYTRA, INFINITY_ELYTRA, SLM_TAKEOVER\n'
         '    }',
         'TaskType enum')

s = sub1(s,
         '    public static @Nullable TaskThread getModThread() {\n'
         '        return ModThread;\n'
         '    }',
         '    public static @Nullable TaskThread getModThread() {\n'
         '        return ModThread;\n'
         '    }\n'
         '\n'
         '    /** 当前任务是否为第 4 个模式「SLM 甲飞接管」 */\n'
         '    public static boolean isSlm() {\n'
         '        TaskThread t = ModThread;\n'
         '        return t != null && t.type == TaskType.SLM_TAKEOVER;\n'
         '    }',
         'isSlm helper')
write(p, s)

# ---------------------------------------------------------------- RSTScr GUI
p = os.path.join(J, 'RSTScr.java')
s = read(p)
s = sub1(s, 'private static final int ciButtonsRow = 5;',
         'private static final int ciButtonsRow = 6;', 'ciButtonsRow')

new_button = (
    ',\n'
    '                    new SrcButtonEntry("开始飞行(SLM甲飞接管)", "第4模式:用MagicBaritone把飞行物理替换为SlimefunHelper甲飞,不穿鞘翅、不掉鞘翅耐久(需安装MagicBaritone+SlimefunHelper)", () -> {\n'
    '                        int x1, z1;\n'
    '                        if (x == null || z == null) return;\n'
    '                        try {\n'
    '                            x1 = Integer.parseInt(x);\n'
    '                        } catch (NumberFormatException e) {\n'
    '                            return;\n'
    '                        }\n'
    '                        try {\n'
    '                            z1 = Integer.parseInt(z);\n'
    '                        } catch (NumberFormatException e) {\n'
    '                            return;\n'
    '                        }\n'
    '                        if (client == null || client.player == null) return;\n'
    '                        if (TaskThread.getModThread() != null) {\n'
    '                            if (TaskThread.getModThread().getState() == Thread.State.TERMINATED)\n'
    '                                MsgSender.SendMsg(client.player, "模组遇到线程状态错误，通常重启可解决！", MsgLevel.warning);\n'
    '                            return;\n'
    '                        }\n'
    '                        MsgSender.SendMsg(client.player, "任务开始！(SLM甲飞接管)", MsgLevel.warning);\n'
    '                        TaskThread.StartModThread(TaskThread.TaskType.SLM_TAKEOVER, getBoolean("isAutoLog", true), getBoolean("isAutoLogOnSeg1", false), x1, z1, client.player.getBlockPos());\n'
    '                        client.setScreen(null);\n'
    '                    })'
)
anchor = ('TaskThread.StartModThread(TaskThread.TaskType.INFINITY_ELYTRA, getBoolean("isAutoLog", true), '
          'getBoolean("isAutoLogOnSeg1", false), x1, z1, client.player.getBlockPos());\n'
          '                        client.setScreen(null);\n'
          '                    })')
s = sub1(s, anchor, anchor + new_button, 'SLM button')
write(p, s)

# ---------------------------------------------------------------- RustElytraClient HUD
p = os.path.join(J, 'RustElytraClient.java')
s = read(p)
s = sub1(s, '                case INFINITY_ELYTRA -> sb.append("无尽鞘翅模式");',
         '                case INFINITY_ELYTRA -> sb.append("无尽鞘翅模式");\n'
         '                case SLM_TAKEOVER -> sb.append("SLM甲飞接管");', 'HUD status')
write(p, s)

# ---------------------------------------------------------------- RustElytraTask
p = os.path.join(J, 'RustElytraTask.java')
s = read(p)

GLIDING = 'isFallFlying' if 'isFallFlying()' in s else 'isGliding'

s = sub1(s, '    private static boolean noElytra = false;',
         '    private static boolean noElytra = false;\n'
         '    /** ★SLM 甲飞接管：起飞失败计数（连续失败 3 次就改用烟花起飞） */\n'
         '    private static int slmTakeoffFails = 0;', 'slmTakeoffFails field')

s = sub1(s, '        jumpingCounter.clear();',
         '        jumpingCounter.clear();\n'
         '        slmTakeoffFails = 0;', 'resetStatus slm')

s = sub1(s, 'if (type == INFINITY_ELYTRA) BaritoneAPI.getSettings().elytraAllowEmergencyLand.value = false;',
         'if (type == INFINITY_ELYTRA || type == SLM_TAKEOVER) BaritoneAPI.getSettings().elytraAllowEmergencyLand.value = false;',
         'allowEmergencyLand')

old_takeoff = (
    '    private static void elytraTakeoff(@NotNull MinecraftClient client) {\n'
    '        if (client.player == null) throw new TaskException("null");\n'
)
assert old_takeoff in s, '[MISS] elytraTakeoff head'
s = s.replace(old_takeoff,
              old_takeoff +
              '        if (isSlm()) {\n'
              '            slmElytraTakeoff(client);\n'
              '            return;\n'
              '        }\n', 1)

slm_takeoff = (
    '\n'
    '    /**\n'
    '     * ★SLM 甲飞接管模式起飞：按住空格起跳，再在空中补按一次，让 SlimefunHelper 甲飞/滑翔生效；\n'
    '     * 多试几次，因为服务器卡顿/反作弊回弹可能吃掉其中一次按键。\n'
    '     */\n'
    '    private static void slmElytraTakeoff(@NotNull MinecraftClient client) {\n'
    '        if (client.player == null) throw new TaskException("null");\n'
    '        client.player.setPitch(-20);\n'
    '        for (int attempt = 0; attempt < 3; attempt++) {\n'
    '            client.options.jumpKey.setPressed(true);\n'
    '            delay(2);\n'
    '            if (client.player == null) return;\n'
    '            client.options.jumpKey.setPressed(false);\n'
    '            delay(1);\n'
    '            client.options.jumpKey.setPressed(true);\n'
    '            delay(1);\n'
    '            client.options.jumpKey.setPressed(false);\n'
    '            for (int i = 0; i < 6; i++) {\n'
    '                if (client.player == null || client.player.' + GLIDING + '()) return;\n'
    '                delay(1);\n'
    '            }\n'
    '        }\n'
    '    }\n'
)
anchor_takeoff_end = (
    '        client.options.jumpKey.setPressed(true);\n'
    '        delay(1);\n'
    '        client.options.jumpKey.setPressed(false);\n'
    '    }\n'
)
assert anchor_takeoff_end in s, '[MISS] elytraTakeoff end'
s = s.replace(anchor_takeoff_end, anchor_takeoff_end + slm_takeoff, 1)

old_jump = (
    '                    MsgSender.SendMsg(client.player, "自动起跳：" + jumpingCounter.getCount(), MsgLevel.warning);\n'
    '                    if (jumpingCounter.getCount() <= 3) {\n'
    '                        elytraTakeoff(client);\n'
    '                        for (int i = 0; i < 40; i++) {\n'
    '                            if (BaritoneControlChecker.isControlPlayer() || client.player.isOnGround()) break;\n'
    '                            delay(1);\n'
    '                        }\n'
    '\n'
    '                    } else {\n'
    '                        flyToOpen(client, x, z);\n'
    '                    }\n'
    '\n'
    '                    jumpingCounter.accumulate();\n'
)
new_jump = (
    '                    if (isSlm()) {\n'
    '                        // ★SLM 甲飞接管：原生 jumpingCounter 是 100 tick 滑动窗口，\n'
    '                        //   起飞失败时窗口会漏空，导致要卡 5 分钟才走烟花起飞。这里改成持久计数。\n'
    '                        MsgSender.SendMsg(client.player, "SLM自动起跳：" + slmTakeoffFails, MsgLevel.warning);\n'
    '                        if (slmTakeoffFails < 3) {\n'
    '                            elytraTakeoff(client);\n'
    '                            for (int i = 0; i < 40; i++) {\n'
    '                                if (BaritoneControlChecker.isControlPlayer() || !client.player.isOnGround()) break;\n'
    '                                delay(1);\n'
    '                            }\n'
    '                            if (client.player.' + GLIDING + '() || !client.player.isOnGround()) slmTakeoffFails = 0;\n'
    '                            else slmTakeoffFails++;\n'
    '                        } else {\n'
    '                            slmTakeoffFails = 0;\n'
    '                            flyToOpen(client, x, z);\n'
    '                        }\n'
    '                    } else {\n'
    '                        MsgSender.SendMsg(client.player, "自动起跳：" + jumpingCounter.getCount(), MsgLevel.warning);\n'
    '                        if (jumpingCounter.getCount() <= 3) {\n'
    '                            elytraTakeoff(client);\n'
    '                            for (int i = 0; i < 40; i++) {\n'
    '                                if (BaritoneControlChecker.isControlPlayer() || client.player.isOnGround()) break;\n'
    '                                delay(1);\n'
    '                            }\n'
    '\n'
    '                        } else {\n'
    '                            flyToOpen(client, x, z);\n'
    '                        }\n'
    '\n'
    '                        jumpingCounter.accumulate();\n'
    '                    }\n'
)
s = sub1(s, old_jump, new_jump, 'jump branch')
write(p, s)

# ---------------------------------------------------------------- RustSupplyTask
p = os.path.join(J, 'RustSupplyTask.java')
s = read(p)

s = sub1(s,
         '            if (!elytra) throw new TaskThread.TaskException("物资不足：需要穿戴 耐久3 经验修补的鞘翅！");',
         '            if (!elytra && !TaskThread.isSlm())\n'
         '                throw new TaskThread.TaskException("物资不足：需要穿戴 耐久3 经验修补的鞘翅！");',
         'supply elytra precheck')

s = sub1(s,
         '            case INFINITY_ELYTRA -> FireworkInNeed = (int) Math.floor(Math.max(26 * 64 - FireworkSupplyChecker(client), 0) / 64.0);',
         '            case INFINITY_ELYTRA -> FireworkInNeed = (int) Math.floor(Math.max(26 * 64 - FireworkSupplyChecker(client), 0) / 64.0);\n'
         '            case SLM_TAKEOVER -> FireworkInNeed = (int) Math.floor(Math.max(26 * 64 - FireworkSupplyChecker(client), 0) / 64.0);',
         'FireworkInNeed switch')

old_slot = (
    '                    case INFINITY_ELYTRA -> {\n'
    '                        if(m < 26){\n'
    '                            m++;\n'
    '                            continue;\n'
    '                        }\n'
    '                    }\n'
)
new_slot = old_slot + (
    '                    case SLM_TAKEOVER -> {\n'
    '                        if(m < 26){\n'
    '                            m++;\n'
    '                            continue;\n'
    '                        }\n'
    '                    }\n'
)
s = sub1(s, old_slot, new_slot, 'replaceSlot switch')

# 末影箱里没有食物时不要整段任务失败（用户实测：经常因此自动退出）
_NL = chr(10)
old_food = ('            if (slot2 == -1)' + _NL +
            '                throw new TaskThread.TaskException("无可用" + Food.getName().getString() + "!");' + _NL +
            '            else ShulkerList.add(slot2);' + _NL)
new_food = ('            if (slot2 == -1)' + _NL +
            '                MsgSender.SendMsg(client.player, "末影箱里没有" + Food.getName().getString() + "，先用身上现有的食物继续", MsgLevel.warning);' + _NL +
            '            else ShulkerList.add(slot2);' + _NL)
s = sub1(s, old_food, new_food, 'food shortage')

# 容器标题宽松匹配
s = sub1(s,
         '        // 不是目标容器\n'
         '        if (!ContainerName.equalsIgnoreCase(handled.getTitle().getString())) return null;',
         '        // 不是目标容器（★宽松匹配：去颜色符号/空格，双向包含）\n'
         '        if (!containerNameMatches(handled.getTitle().getString(), ContainerName)) return null;',
         'container title match')

helper = (
    '\n'
    '    /** ★容器标题宽松匹配：去掉 § 颜色符号和空格，双向包含（兼容服务器给容器名加前后缀） */\n'
    '    private static boolean containerNameMatches(@Nullable String title, @Nullable String want) {\n'
    '        String a = normalizeContainerName(title);\n'
    '        String b = normalizeContainerName(want);\n'
    '        if (a.isEmpty() || b.isEmpty()) return true;\n'
    '        return a.contains(b) || b.contains(a);\n'
    '    }\n'
    '\n'
    '    private static String normalizeContainerName(@Nullable String s) {\n'
    '        if (s == null) return "";\n'
    '        StringBuilder sb = new StringBuilder();\n'
    '        for (int i = 0; i < s.length(); i++) {\n'
    '            char c = s.charAt(i);\n'
    '            if (c == \'\\u00a7\') {\n'
    '                i++;\n'
    '                continue;\n'
    '            }\n'
    '            if (c < 32 || c == \' \') continue;\n'
    '            sb.append(Character.toLowerCase(c));\n'
    '        }\n'
    '        return sb.toString();\n'
    '    }\n'
)
anchor_screen = (
    '    private static @Nullable HandledScreen<?> ContainerScreenChecker(@NotNull MinecraftClient client, @NotNull String ContainerName) {'
)
assert anchor_screen in s, '[MISS] ContainerScreenChecker'
s = s.replace(anchor_screen, helper + '\n' + anchor_screen, 1)

# WaitForScreen 20 -> 120
s = sub1(s,
         '        for (int i = 0; i < 20; i++) {\n'
         '            HandledScreen<?> temp = ContainerScreenChecker(client, ScreenName);',
         '        for (int i = 0; i < 120; i++) {   // ★原版只等 20 tick，服务器卡顿时必失败\n'
         '            HandledScreen<?> temp = ContainerScreenChecker(client, ScreenName);',
         'WaitForScreen timeout')

# mineSupplyShulker 重写
start = s.index('    private static void mineSupplyShulker(@NotNull MinecraftClient client, BlockPos ShulkerPos) {')
end = s.index('    /**\n     * 挖掘末影箱', start)
new_mine = '''    private static void mineSupplyShulker(@NotNull MinecraftClient client, BlockPos ShulkerPos) {
        if (client.player == null) throw new TaskThread.TaskException("Player为null");
        PlayerInventory inventory = client.player.getInventory();
        int count = countShulkerInInventory(inventory);
        if (client.world == null) throw new TaskThread.TaskException("世界异常");
        final int targetCount = count + 1;
        final BlockPos pos = ShulkerPos;

        // ★先关掉潜影盒界面：界面开着时玩家无法攻击方块/移动，baritone 的挖掘会永远结束不了
        RunAsMainThread(() -> client.setScreen(null));
        TaskThread.delay(2);

        // 用 baritone 挖掉用过的补给盒
        RunAsMainThread(() -> {
            Block block = client.world.getBlockState(pos).getBlock();
            BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().mine(targetCount, block);
        });

        // 等待 baritone 挖掘（★原版只等 40 tick = 2 秒，服务器回弹/卡顿必炸，这里放宽到 30 秒）
        for (int i = 0; i < 600; i++) {
            if (isHittingFireball()) i = 0;
            if (!BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().isActive()) break;
            TaskThread.delay(1);
        }
        if (BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().isActive()) {
            RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().cancel());
        }

        // ★兜底：block 还在就自己动手挖（方块是自己放的，就在交互距离内）
        for (int i = 0; i < 200; i++) {
            if (client.world == null || client.player == null) throw new TaskThread.TaskException("世界异常");
            if (client.world.getBlockState(pos).isAir()) break;
            if (i == 199) throw new TaskThread.TaskException("挖掘补给箱超时");
            RunAsMainThread(() -> {
                if (client.interactionManager == null || client.player == null) return;
                Vec3d target = Vec3d.ofCenter(pos);
                Vec3d eye = client.player.getEyePos();
                Vec3d dir = target.subtract(eye);
                double horiz = Math.sqrt(dir.x * dir.x + dir.z * dir.z);
                float yaw = (float) (MathHelper.atan2(dir.z, dir.x) * 180.0 / Math.PI) - 90.0f;
                float pitch = (float) (-(MathHelper.atan2(dir.y, horiz) * 180.0 / Math.PI));
                client.player.setYaw(yaw);
                client.player.setPitch(pitch);
                Direction side = Direction.getFacing(eye.x - target.x, eye.y - target.y, eye.z - target.z);
                client.interactionManager.updateBlockBreakingProgress(pos, side);
                client.player.swingHand(Hand.MAIN_HAND);
            });
            TaskThread.delay(1);
        }

        // 等待捡起潜影盒
        for (int j = 0; j < 60; j++) {
            if (countShulkerInInventory(inventory) >= targetCount) break;
            if (j == 59) throw new TaskThread.TaskException("挖掘补给箱失败!");
            TaskThread.delay(1);
        }
    }

    /** 统计背包里的潜影盒数量（所有颜色都算） */
    private static int countShulkerInInventory(@NotNull PlayerInventory inventory) {
        int count = 0;
        for (int i = 0; i < inventory.main.size(); i++) {
            ItemStack stack = inventory.main.get(i);
            Item item = stack.getItem();
            if (item instanceof BlockItem && ((BlockItem) item).getBlock() instanceof ShulkerBoxBlock) {
                count += stack.getCount();
            }
        }
        return count;
    }

'''
s = s[:start] + new_mine + s[end:]

# MathHelper import
if 'import net.minecraft.util.math.MathHelper;' not in s:
    s = s.replace('import net.minecraft.util.math.BlockPos;',
                  'import net.minecraft.util.math.BlockPos;\nimport net.minecraft.util.math.MathHelper;', 1)
write(p, s)

print('PATCH OK ->', root)
