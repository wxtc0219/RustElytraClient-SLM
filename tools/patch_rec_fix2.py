#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REC 补给/飞行检查稳健性修复（v1.0.0-r2）：
1. 食物检查放宽：不再只看快捷栏第 6 格 >18，改为统计整个快捷栏食物 >=8
2. 补给食物门槛 16 -> 8，避免“差一个金胡萝卜就整段失败”
3. 快速找放置点时优先半径 1，失败再半径 2（上方允许非空气）
4. 潜影盒放不下时：先挖掉末影箱腾位置，再重新放一个末影箱继续
5. 末影箱挖不动时：切镐子手动挖兜底
"""
import sys

SUPPLY = 'src/main/java/dev/rstminecraft/RustSupplyTask.java'
TASK = 'src/main/java/dev/rstminecraft/RustElytraTask.java'


def patch(root):
    p = root + '/' + SUPPLY
    s = open(p, encoding='utf-8').read()

    def rep(old, new, tag):
        nonlocal s
        assert old in s, f'{tag}: anchor not found'
        s = s.replace(old, new, 1)

    # ---------- 3. findPlaceTarget：半径 1 -> 半径 2 回退 ----------
    import re as _re
    _m = _re.search(r'    private static @Nullable BlockPos findPlaceTarget\(@NotNull ClientPlayerEntity player\) \{.*?\n    \}', s, _re.S)
    assert _m, 'findPlaceTarget: method not found'
    _old_block = _m.group(0)
    _world_getter = 'player.getEntityWorld()' if 'getEntityWorld()' in _old_block else 'player.getWorld()'
    _new_block = '''    private static @Nullable BlockPos findPlaceTarget(@NotNull ClientPlayerEntity player) {
        BlockPos origin = player.getBlockPos();
        World world = _WORLD_GETTER_;

        // 搜索范围：优先 3×3×3，放不下再扩到 5×5×5（挖矿洞、窄隧道里很常见）
        for (int radius = 1; radius <= 2; radius++) {
            boolean relaxed = radius > 1;
            for (int dx = -radius; dx <= radius; dx++) {
                for (int dy = -radius; dy <= radius; dy++) {
                    for (int dz = -radius; dz <= radius; dz++) {
                        // 不能与玩家重合
                        if (0 == dx && 0 == dz) continue;
                        BlockPos target = origin.add(dx, dy, dz);

                        // 目标必须是空气或可替换方块（如草）
                        if (!world.getBlockState(target).isAir() && !world.getBlockState(target).isReplaceable()) continue;

                        // 下方必须是实心方块
                        BlockPos below = target.down();
                        if (!world.getBlockState(below).isSolidBlock(world, below)) continue;
                        // 上方必须是空气（半径 2 时放宽为“空气或可替换”）
                        BlockPos up = target.up();
                        if (relaxed) {
                            if (!world.getBlockState(up).isAir() && !world.getBlockState(up).isReplaceable()) continue;
                        } else {
                            if (!world.getBlockState(up).isAir()) continue;
                        }

                        return target;
                    }
                }
            }
        }
        return null;
    }'''.replace('_WORLD_GETTER_', _world_getter)
    s = s.replace(_old_block, _new_block, 1)


    # ---------- 5. forceBreakBlock + mineEnderChest 兜底 ----------
    rep('''    private static void mineEnderChest(@NotNull MinecraftClient client, BlockPos EnderChestPos) {
        if (client.player == null || client.world == null) throw new TaskThread.TaskException("null");
        int enderCount = countItemInInventory(client.player, Items.ENDER_CHEST);
        int obsidianCount = countItemInInventory(client.player, Items.OBSIDIAN);
        RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().mine(obsidianCount + 1, client.world.getBlockState(EnderChestPos).getBlock()));

        // 等待baritone挖掘
        for (int i = 0; i < 100; i++) {
            if (isHittingFireball()) i = 0;
            if (!BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().isActive() || countItemInInventory(client.player, Items.ENDER_CHEST) > enderCount) {
                RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().cancel());
                break;
            }

            if (i == 99 || !client.player.getBlockPos().isWithinDistance(EnderChestPos, 5)) {
                RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().cancel());
                throw new TaskThread.TaskException("挖掘异常？取消挖掘!!");
            }
            TaskThread.delay(1);
        }
        MsgSender.SendMsg(client.player, "挖掘完毕", MsgLevel.tip);
    }''', '''    /**
     * ★切到镐子手动挖一个方块（baritone 找不到路 / 挖不动时兜底）
     */
    private static void forceBreakBlock(@NotNull MinecraftClient client, @NotNull BlockPos pos) {
        if (client.player == null || client.world == null || client.interactionManager == null)
            throw new TaskThread.TaskException("null");
        int oldSlot = client.player.getInventory().selectedSlot;
        int pick = findItemInHotBar(client.player, Items.NETHERITE_PICKAXE);
        if (pick == -1) pick = findItemInHotBar(client.player, Items.DIAMOND_PICKAXE);
        final int finalPick = pick;
        if (pick != -1) {
            RunAsMainThread(() -> {
                client.player.getInventory().selectedSlot = finalPick;
                if (client.getNetworkHandler() != null)
                    client.getNetworkHandler().sendPacket(new UpdateSelectedSlotC2SPacket(finalPick));
            });
            TaskThread.delay(2);
        }
        try {
            for (int i = 0; i < 200; i++) {
                if (client.world == null || client.player == null || client.interactionManager == null)
                    throw new TaskThread.TaskException("null");
                if (client.world.getBlockState(pos).isAir()) break;
                if (i == 199) throw new TaskThread.TaskException("手动挖掘补给方块超时");
                RunAsMainThread(() -> {
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
        } finally {
            RunAsMainThread(() -> {
                if (client.player == null) return;
                client.player.getInventory().selectedSlot = oldSlot;
                if (client.getNetworkHandler() != null)
                    client.getNetworkHandler().sendPacket(new UpdateSelectedSlotC2SPacket(oldSlot));
            });
        }
    }

    private static void mineEnderChest(@NotNull MinecraftClient client, BlockPos EnderChestPos) {
        if (client.player == null || client.world == null) throw new TaskThread.TaskException("null");
        int enderCount = countItemInInventory(client.player, Items.ENDER_CHEST);
        int obsidianCount = countItemInInventory(client.player, Items.OBSIDIAN);
        RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().mine(obsidianCount + 1, client.world.getBlockState(EnderChestPos).getBlock()));

        // 等待baritone挖掘（★超时不再直接失败，留给下面的手动兜底）
        for (int i = 0; i < 100; i++) {
            if (isHittingFireball()) i = 0;
            if (!BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().isActive() || countItemInInventory(client.player, Items.ENDER_CHEST) > enderCount) {
                RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().cancel());
                break;
            }

            if (i == 99 || !client.player.getBlockPos().isWithinDistance(EnderChestPos, 5)) {
                RunAsMainThread(() -> BaritoneAPI.getProvider().getPrimaryBaritone().getMineProcess().cancel());
                break;
            }
            TaskThread.delay(1);
        }

        // ★兜底：方块还在就切镐子自己挖
        if (client.world != null && !client.world.getBlockState(EnderChestPos).isAir()) {
            MsgSender.SendMsg(client.player, "baritone挖不动末影箱，手动挖掘", MsgLevel.warning);
            forceBreakBlock(client, EnderChestPos);
        }

        // 等待捡起末影箱
        for (int j = 0; j < 60; j++) {
            if (countItemInInventory(client.player, Items.ENDER_CHEST) > enderCount) break;
            if (j == 59) throw new TaskThread.TaskException("挖掘末影箱失败!");
            TaskThread.delay(1);
        }
        MsgSender.SendMsg(client.player, "挖掘完毕", MsgLevel.tip);
    }''', 'mineEnderChest')

    # ---------- 1a. SupplyTask 提前返回的 hasFood ----------
    rep('''        boolean hasTotem = client.player.getInventory().getStack(3).getItem() == Items.TOTEM_OF_UNDYING || client.player.getInventory().getStack(4).getItem() != Items.TOTEM_OF_UNDYING;
        boolean hasFood = client.player.getInventory().getStack(5).getItem() == Food && client.player.getInventory().getStack(5).getCount() > 18;''',
        '''        boolean hasTotem = client.player.getInventory().getStack(3).getItem() == Items.TOTEM_OF_UNDYING || client.player.getInventory().getStack(4).getItem() != Items.TOTEM_OF_UNDYING;
        int hotbarFood0 = 0;
        for (int i = 0; i < 9; i++) {
            ItemStack fs = client.player.getInventory().getStack(i);
            if (fs.getItem() == Food) hotbarFood0 += fs.getCount();
        }
        boolean hasFood = hotbarFood0 >= 8;''', 'SupplyTask hasFood')

    # ---------- 2. 食物门槛 16 -> 8 ----------
    rep('''            if (FoodCount <= 15)
                throw new TaskThread.TaskException("物资不足：需要至少16个" + Food.getName().getString() + "!");''',
        '''            if (FoodCount <= 7)
                throw new TaskThread.TaskException("物资不足：需要至少8个" + Food.getName().getString() + "!");''', 'FoodCount threshold')

    # ---------- 1b. 快捷栏食物统计（决定要不要从末影箱取食物） ----------
    rep('''        if (client.player.getInventory().getStack(findItemInHotBar(client.player, Food)).getCount() < 30) {''',
        '''        int hotbarFoodCount = 0;
        for (int i = 0; i < 9; i++) {
            ItemStack fs = client.player.getInventory().getStack(i);
            if (fs.getItem() == Food) hotbarFoodCount += fs.getCount();
        }
        if (hotbarFoodCount < 30) {''', 'hotbarFoodCount')

    # ---------- 4a. 状态变量 + 潜影盒放置兜底 ----------
    rep('''        TaskThread.delay(1);
        for (int SupplySlot : ShulkerList) {''',
        '''        TaskThread.delay(1);
        final BlockPos[] enderChestPos = {EnderChestTargetPos};
        boolean enderChestBroken = false;
        for (int SupplySlot : ShulkerList) {''', 'enderChest state')

    rep('''            // 找空位放置潜影盒
            BlockPos ShulkerTargetPos = findPlaceTarget(player);
            if (ShulkerTargetPos == null) throw new TaskThread.TaskException("附近没有合适的位置放置潜影盒");''',
        '''            // 找空位放置潜影盒
            BlockPos ShulkerTargetPos = findPlaceTarget(player);
            if (ShulkerTargetPos == null) {
                // ★兜底：末影箱很可能占了唯一能放的位置，先把它挖了腾地方
                MsgSender.SendMsg(client.player, "附近没有位置放潜影盒，先挖掉末影箱腾位置", MsgLevel.warning);
                mineEnderChest(client, enderChestPos[0]);
                enderChestBroken = true;
                TaskThread.delay(3);
                ShulkerTargetPos = findPlaceTarget(player);
            }
            if (ShulkerTargetPos == null) throw new TaskThread.TaskException("附近没有合适的位置放置潜影盒");''', 'shulker place fallback')

    # ---------- 4b. 重新打开末影箱（必要时重新放一个） ----------
    rep('''            // 重新打开末影箱
            RunAsMainThread(() -> lookAt(client.player, Vec3d.ofCenter(EnderChestTargetPos)));
            TaskThread.delay(2);
            OpenContainer(client, EnderChestTargetPos);''',
        '''            // 重新打开末影箱（兜底挖掉过的话，就用背包里的末影箱重新放一个）
            if (enderChestBroken) {
                int ecSlot = findItemInHotBar(client.player, Items.ENDER_CHEST);
                if (ecSlot == -1) throw new TaskThread.TaskException("无末影箱可重新放置");
                BlockPos newEnderChestPos = findPlaceTarget(client.player);
                if (newEnderChestPos == null) throw new TaskThread.TaskException("附近没有合适的位置放置末影箱");
                PlaceAndOpenContainer(client, newEnderChestPos, ecSlot);
                enderChestPos[0] = newEnderChestPos;
                enderChestBroken = false;
            } else {
                RunAsMainThread(() -> lookAt(client.player, Vec3d.ofCenter(enderChestPos[0])));
                TaskThread.delay(2);
                OpenContainer(client, enderChestPos[0]);
            }''', 'reopen ender chest')

    # ---------- 4c. 收尾挖末影箱用最新位置 ----------
    rep('''        // 挖掘末影箱
        mineEnderChest(client, EnderChestTargetPos);''',
        '''        // 挖掘末影箱
        mineEnderChest(client, enderChestPos[0]);''', 'final mineEnderChest')

    open(p, 'w', encoding='utf-8', newline='\n').write(s)

    # ---------- 1c. RustElytraTask.FireworkChecker hasFood ----------
    p2 = root + '/' + TASK
    t = open(p2, encoding='utf-8').read()
    old = '''            boolean hasTotem = client.player.getInventory().getStack(3).getItem() == Items.TOTEM_OF_UNDYING || client.player.getInventory().getStack(4).getItem() != Items.TOTEM_OF_UNDYING;
            boolean hasFood = client.player.getInventory().getStack(5).getItem() == Food && client.player.getInventory().getStack(5).getCount() > 18;'''
    new = '''            boolean hasTotem = client.player.getInventory().getStack(3).getItem() == Items.TOTEM_OF_UNDYING || client.player.getInventory().getStack(4).getItem() != Items.TOTEM_OF_UNDYING;
            int hotbarFood = 0;
            for (int i = 0; i < 9; i++) {
                ItemStack fs = client.player.getInventory().getStack(i);
                if (fs.getItem() == Food) hotbarFood += fs.getCount();
            }
            boolean hasFood = hotbarFood >= 8;'''
    assert old in t, 'FireworkChecker hasFood anchor not found'
    t = t.replace(old, new, 1)
    open(p2, 'w', encoding='utf-8', newline='\n').write(t)
    print('patched', root)


if __name__ == '__main__':
    for r in sys.argv[1:]:
        patch(r)
