# 构建说明（如何从源码重建三个版本的产物）

本目录 `release/` 里的三个 REC jar 与 `deps/` 里的 MagicBaritone 1.21.4 / 1.21.11
都可以从上游源码 + 本目录补丁重新构建。

## 环境

- JDK 21（带 javac）
- Gradle 8.14.x（REC / MagicBaritone 1.21.4）或 Gradle 9.6.x（REC 1.21.11 / baritone 1.21.11，需要 loom 1.17）
- 网络可访问：Mojang 版本元数据、Fabric Maven、Meteor Maven（REC 依赖 baritone snapshot）

## 1. REC 补丁 jar

```bash
# 取上游源码（按版本选分支）
git clone -b 1.21.1 https://github.com/RSTminecraft/RustElytraClient.git rec1211
git clone -b 1.21.4 https://github.com/RSTminecraft/RustElytraClient.git rec1214
git clone -b 1.21.8 https://github.com/RSTminecraft/RustElytraClient.git rec1218   # 1.21.11 版用

# 打第 4 模式补丁（本目录 tools/patch_rec_slm.py）
python tools/patch_rec_slm.py rec1211
python tools/patch_rec_slm.py rec1214
python tools/patch_rec_slm.py rec1218

# 1.21.11 额外：把 rec1218 的 gradle.properties/build.gradle 改成
#   minecraft_version=1.21.11
#   yarn mappings 1.21.11+build.6
#   loader_version=0.18.0
#   loom_version=1.17-SNAPSHOT
#   fabric_version=0.140.0+1.21.11
#   modCompileOnly meteordevelopment:baritone:1.21.11-SNAPSHOT
# 并按 patches/rec/1.21.11-slm-takeover.diff 里的 API 适配部分修正（getEntityPos / KeyBinding.Category /
# PlayerInventory.getStack / TrajectoryRenderer 空实现）

cd rec1211 && ./gradlew build -x test
# 产物：build/libs/1.21.1/RustElytraClient-1.21.1-beta1.6-<时间戳>.jar
```

## 2. MagicBaritone 1.21.4 / 1.21.11

```bash
# 取 baritone 官方对应分支
git clone -b 1.21.4 https://github.com/cabaletta/baritone.git baritone-1.21.4
git clone -b 1.21.11 https://github.com/cabaletta/baritone.git baritone-1.21.11

# 应用甲飞补丁
cd baritone-1.21.4 && git apply ../patches/magicbaritone/1.21.4-slime.diff
cd baritone-1.21.11 && git apply ../patches/magicbaritone/1.21.11-slime.diff

# gradle.properties 里改：available_loaders=fabric、mod_version=1.0.0
./gradlew :fabric:build
# 产物：fabric/build/libs/baritone-fabric-1.0.0.jar
```

> 产物重命名为 `MagicBaritone-1.0.0-mc<MC版本>-fabric.jar` 即为 `deps/` 中的移植版。

## 3. 版本信息

| 产物 | 上游 | 许可证 |
| --- | --- | --- |
| `release/RustElytraClient-*-slm-takeover-1.0.0.jar` | RSTminecraft/RustElytraClient（GPL-3.0） | GPL-3.0 |
| `deps/MagicBaritone-1.0.0-mc1.21.1-fabric.jar` | Alastorbaby/MagicBaritone 官方发布（LGPL-3.0） | LGPL-3.0 |
| `deps/MagicBaritone-1.0.0-mc1.21.4-fabric.jar` | cabaletta/baritone 1.21.4 + 甲飞补丁（LGPL-3.0） | LGPL-3.0 |
| `deps/MagicBaritone-1.0.0-mc1.21.11-fabric.jar` | cabaletta/baritone 1.21.11 + 甲飞补丁（LGPL-3.0） | LGPL-3.0 |
