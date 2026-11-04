package dev.rstminecraft;

public class T {
    public static boolean eq(String name, String title) {
        String a = clean(name);
        String b = clean(title);
        if (a.isEmpty() || b.isEmpty()) {
            return true;
        }
        return b.contains(a) || a.contains(b);
    }

    /** 当前任务是否是第 4 个 SLM 甲飞接管模式 */
    public static boolean isSlm() {
        try {
            Class<?> tt = Class.forName("dev.rstminecraft.TaskThread");
            Object thread = tt.getMethod("getModThread").invoke(null);
            if (thread == null) {
                return false;
            }
            Object type = thread.getClass().getField("type").get(thread);
            return type != null && "SLM_TAKEOVER".equals(String.valueOf(type));
        } catch (Throwable t) {
            return false;
        }
    }

    /** 背包里是否还有鞘翅（不要求穿戴） */
    public static boolean hasElytra() {
        try {
            Object inv = inventory();
            if (inv == null) {
                return false;
            }
            Object elytra = elytraItem();
            java.lang.reflect.Method getStack = inv.getClass().getMethod("method_5438", int.class);
            for (int i = 0; i < 41; i++) {
                Object stack;
                try {
                    stack = getStack.invoke(inv, i);
                } catch (Throwable ignored) {
                    continue;
                }
                if (stack == null) {
                    continue;
                }
                Object item = stack.getClass().getMethod("method_7909").invoke(stack);
                if (item == elytra) {
                    return true;
                }
            }
        } catch (Throwable ignored) {
        }
        return false;
    }

    /** 补给前置检查：原版要求穿戴附魔鞘翅；SLM 模式只要背包里有鞘翅 */
    public static boolean elytraOk(boolean wornOk) {
        if (wornOk) {
            return true;
        }
        return isSlm() && hasElytra();
    }

    /** RepairElytra 里的守卫：原版要求身上是鞘翅；SLM 模式直接放行 */
    public static boolean repairGuard(Object chestStack) {
        try {
            Object elytra = elytraItem();
            if (chestStack != null) {
                Object item = chestStack.getClass().getMethod("method_7909").invoke(chestStack);
                if (item == elytra) {
                    return true;
                }
            }
        } catch (Throwable ignored) {
        }
        return isSlm();
    }

    private static Object inventory() throws Exception {
        Class<?> mcCls = Class.forName("net.minecraft.class_310");
        Object mc = mcCls.getMethod("method_1551").invoke(null);
        if (mc == null) {
            return null;
        }
        Object player = mcCls.getField("field_1724").get(mc);
        if (player == null) {
            return null;
        }
        return player.getClass().getMethod("method_31548").invoke(player);
    }

    private static Object elytraItem() throws Exception {
        return Class.forName("net.minecraft.class_1802").getField("field_8833").get(null);
    }

    private static String clean(String s) {
        if (s == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\u00a7') {
                i++;
                continue;
            }
            if (c < 32) {
                continue;
            }
            sb.append(Character.toLowerCase(c));
        }
        return sb.toString().trim();
    }
}
