# SlimefunHelper（SLM）甲飞参数全表

> 来源：本仓库 `slimefunhelper/runtime/mov.yml`（原样导出，未改动任何值）、`baritone/settings.txt`、`config/RSTConfig.json`。
> 想直接在游戏里改：`!!config` 面板，或导入 `slimefunhelper/config/` 下的快照。

## flight

| 参数 | 值 |
| --- | --- |
| `toggle-flying` | `hotkey:` |
| `flight-enable` | `false` |
| `flight-enable-hotkey` | `hotkey:` |
| `flight-mode` | `enum:flight_mode:CREATIVE` |
| `flight-mode-switch-hotkey` | `hotkey:` |
| `antikick` | `true` |
| `antikick-period` | `60` |
| `onground-when-mine` | `false` |

## no-fall

| 参数 | 值 |
| --- | --- |
| `toggle` | `false` |
| `hotkey` | `hotkey:` |
| `bypass-mode` | `enum:no_fall_bypass_mode:LAZY_MODE` |
| `safe-distance-modify` | `0` |
| `equipment-id-bypass-nofall` | `nbt:regex:"^(SLIME.*_BOOTS)$"` |
| `disable-when-allow-flying` | `true` |

## no-ground

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `mode` | `enum:no_ground_mode:NONE` |
| `反作弊回弹! tp号` | `{teleportId}, 位置: {position}"}` |

## anti-chunk-lag

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `predict-velocity` | `48` |
| `freeze-when-lag` | `false` |
| `log-to-player` | `false` |

## anti-liquid

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `mode` | `enum:anti_liquid_anti_liquid_mode:NONE` |
| `water-expand-check` | `0.2` |
| `enable-not-fly` | `false` |
| `enable-fly` | `false` |
| `auto-armor-fly-control` | `false` |
| `auto-armor-fly-switch-gt` | `5` |
| `leave-water-expand-check` | `2.0` |

## no-slowdown

| 参数 | 值 |
| --- | --- |
| `when-sneak` | `false` |
| `when-use-item` | `false` |
| `when-with-block` | `false` |
| `when-on-block` | `false` |
| `when-in-block` | `false` |
| `when-special-block` | `false` |
| `fake-sneak` | `false` |
| `fake-sneak-hotkey` | `hotkey:` |
| `use-item-bypass` | `enum:use_item_noslow_bypass:NO_BYPASS` |
| `use-item-swap-item-delay` | `1` |
| `use-item-swap-no-sprint` | `false` |
| `block-in-bypass` | `enum:no_web_slow_bypass:NO_BYPASS` |
| `block-in-keep-y` | `false` |
| `block-in-mine-when-jump` | `false` |
| `fake-sneak-mode` | `enum:bypass_mode:NO_BYPASS` |
| `fake-sneak-status-mode` | `enum:packet_sneak_bypass_mode:BAD_PACKET` |

## sprint

| 参数 | 值 |
| --- | --- |
| `legal-auto-sprint` | `false` |
| `legal-auto-sprint-hotkey` | `hotkey:` |
| `log-auto-sprint` | `false` |
| `fake-sprint` | `false` |
| `fake-sprint-mode` | `enum:bypass_mode:NO_BYPASS` |
| `all-direction-sprint` | `false` |
| `bypass-mode` | `enum:bypass_mode:NO_BYPASS` |

## swim-control

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `mode` | `enum:swim_control_mode:GRIM` |

## timer

| 参数 | 值 |
| --- | --- |
| `timer-enable` | `false` |
| `timer-enable-hotkey` | `hotkey:` |
| `multiply` | `0` |

## elytra-tweaks

| 参数 | 值 |
| --- | --- |
| `no-kinetic-mode` | `nbt:optionalprimitive:{present:0b,value:"wrapenum\|enum:bypass_mode:BYPASS_GRIM"}` |
| `mace-hit-fix-mode` | `nbt:optionalprimitive:{present:1b,value:"wrapenum\|enum:bypass_mode:BYPASS_GRIM"}` |
| `no-fall-when-landing` | `true` |
| `no-fall-disable-no-fall-module` | `false` |
| `auto-switch` | `false` |
| `auto-take-off` | `hotkey:` |
| `auto-take-off-fireworks-from-ground` | `false` |
| `auto-take-off-retry-ticks` | `3` |
| `auto-start-fly-join-server` | `true` |
| `firwork-speed-limit-web` | `false` |
| `firework-liquid-fly` | `false` |
| `manually-switch` | `hotkey:` |

## unbreakable-elytra

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `period` | `16` |
| `reset-vanilla` | `false` |

## armor-fly

| 参数 | 值 |
| --- | --- |
| `enable` | `true` |
| `enable-hotkey` | `hotkey:Z` |
| `armor-mode` | `enum:armorflymode:TICK` |
| `force-no-elytra` | `true` |
| `enable-liquid-fly` | `false` |
| `liquid-fly-only-fireworks` | `false` |
| `on-ground-fly-only-fireworks` | `true` |
| `land-auto-close` | `false` |
| `land-auto-sneak` | `false` |
| `close-continue-fly` | `nbt:optionalprimitive:{present:1b,value:"int\|20"}` |
| `armor-fly-fix-grim-bad-packets-1` | `true` |
| `pose-fix` | `true` |
| `render-fix` | `true` |
| `enable-manually-swap` | `false` |
| `anti-kick` | `true` |
| `max-delay-ticks` | `nbt:optionalprimitive:{present:1b,value:"int\|7"}` |

## custom-fireworks

| 参数 | 值 |
| --- | --- |
| `firework-item-id` | `nbt:regex:"^(.*?_MULTI_TOOL\|STAFF_ELEMENTAL_WIND)$"` |
| `firework-delay-multiply-vanilla` | `40` |
| `firework-auto-use-vanilla` | `true` |
| `rocket-extra-effect-ticks` | `1` |
| `auto-rescale-firework-box` | `true` |
| `auto-rescale-firework-amount` | `1.6` |
| `firework-speed-limit-up` | `nbt:optionalprimitive:{present:1b,value:"double\|5.0"}` |
| `firework-speed-limit-down` | `nbt:optionalprimitive:{present:1b,value:"double\|5.0"}` |
| `auto-rescale-firework-al` | `enum:elytra_extra_fireworks_al_type:V1` |
| `auto-rescale-firework-anti-lag-threshold` | `0.002` |
| `switch-auto-rescale-firework-al-key` | `hotkey:` |
| `auto-rescale-axis-zero-point-three` | `0.02` |
| `firework-boost-enable` | `false` |
| `firework-boost-hotkey` | `hotkey:` |
| `firework-boost-speed` | `1.7` |
| `baritone-use-rocket-boost` | `false` |
| `firework-boost-use-rescale` | `true` |
| `fly-rocket-on-first-off` | `false` |
| `fly-rocket-on-first-off-hotkey` | `hotkey:` |
| `click-firework-use` | `hotkey:` |
| `log-no-fireworks` | `false` |
| `fireworks-lag-delay` | `true` |
| `firework-lag-delay-hotkey` | `hotkey:` |
| `fireworks-delay-ms` | `500` |
| `motion-amount` | `1.7` |
| `firework-max-delay-multiply-vanilla` | `20.0` |

## simple-flight-control

| 参数 | 值 |
| --- | --- |
| `enable-control` | `true` |
| `enable-control-hotkey` | `hotkey:Z` |
| `motion-mode` | `enum:motionmode:FIRE_WORKS` |
| `firework-rotation-last-ticks` | `3` |
| `rotate-when-void-motion` | `true` |
| `flight-mode` | `enum:elytramode:CONTROL` |
| `flight-toggle` | `hotkey:` |
| `use-floating-utils` | `true` |
| `horizontal-no-gravity` | `true` |
| `pause-when-accelerate` | `true` |
| `land-auto-close` | `false` |
| `hold-jump-takeoff-ticks` | `nbt:optionalprimitive:{present:0b,value:"int\|10"}` |
| `motion-lerp-argument` | `1.0` |
| `motion-lerp-starting` | `true` |
| `use-auto-rescale` | `true` |
| `override-pullup-angle` | `nbt:optionalprimitive:{present:0b,value:"double\|45.0"}` |
| `override-downward-angle` | `nbt:optionalprimitive:{present:0b,value:"double\|45.0"}` |
| `override-horizontal-fly-angle` | `nbt:optionalprimitive:{present:0b,value:"double\|0.1"}` |
| `use-auto-rescale-best-climbing-speed` | `false` |
| `auto-fly` | `false` |
| `auto-fly-hotkey` | `hotkey:` |
| `auto-fly-auto-jump-off` | `false` |
| `auto-fly-land-auto-close` | `true` |

## elytra-flight-legit

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `set-back-mode` | `enum:setback_trigger_type:CRASH_PACKETS` |
| `max-accelerate-velocity` | `6.0` |
| `fix-old-version-velocity-shit` | `true` |
| `fix-kick-from-lag` | `true` |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `pitch` | `80.0` |
| `sneak` | `false` |
| `ground-height` | `3.0` |
| `axis-strict` | `false` |
| `auto-mine-obstacles` | `false` |
| `auto-avoid-obstacles` | `false` |
| `avoid-obstacles-yaw-range` | `50` |
| `avoid-obstacles-predict-ticks` | `80` |
| `avoid-holes` | `false` |
| `queue-packets` | `true` |

## antikb

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `horizontal-threshold` | `0.0` |
| `vertical-threshold` | `0.0` |
| `mode` | `enum:velocity_bypass_mode:NONE` |
| `bypass-explosions` | `false` |
| `grim-freeze-if-walk` | `false` |
| `grim-reset-kb-tick` | `3` |
| `pause-when-wasd` | `false` |
| `freeze-time` | `5.0` |
| `on-ground-only` | `false` |
| `not-in-water` | `false` |
| `execute-during-fireworks` | `true` |
| `execute-in-wall` | `true` |
| `no-entity-push` | `false` |
| `no-liquid-flow-push` | `false` |
| `no-climbing` | `false` |
| `no-block-push` | `false` |
| `no-entity-push` | `false` |
| `no-liquid-flow-push` | `false` |
| `no-climbing` | `false` |

## floating-utils

| 参数 | 值 |
| --- | --- |
| `enable` | `false` |
| `hotkey` | `hotkey:` |
| `on-ground-float` | `false` |
| `use-snap-packet` | `false` |
| `freeze-void` | `nbt:optionalprimitive:{present:0b,value:"double\|-2.0"}` |
| `freeze-absolute-y` | `nbt:optionalprimitive:{present:0b,value:"double\|256.0"}` |
| `enable` | `false` |
| `hotkey` | `hotkey:` |

## baritone/settings.txt

| 参数 | 值 |
| --- | --- |
| `allowInventory` | `true` |
| `allowWaterBucketFall` | `false` |
| `allowVines` | `true` |
| `allowParkour` | `true` |
| `blockReachDistance` | `4.5` |
| `pathRenderLineWidthPixels` | `5.0` |
| `antiCheatCompatibility` | `false` |
| `colorCurrentPath` | `255,0,0` |
| `colorNextPath` | `255,0,255` |
| `colorMostRecentConsidered` | `255,0,0` |
| `colorGoalBox` | `0,255,0` |
| `elytraFireworkSpeed` | `0.7` |
| `elytraNetherSeed` | `-7346913998703726680` |
| `elytraTermsAccepted` | `true` |
| `slimePhysics` | `false` |

## config/RSTConfig.json

```json
{
  "FirstUse": false,
  "isAutoLog": true,
  "isAutoLogOnSeg1": false,
  "DisplayDebug": false,
  "inspectArmor": false,
  "verboseDisplayDebug": false,
  "FoodIndex": 4,
  "autoLogEnabled": true,
  "HudX": 0,
  "HudY": 0,
  "enableHud": true,
  "elytraPredictTerrain": true,
  "netherSeed": -7346913998703726680,
  "elytraFireworkSpeed": 1.2
}
```

## 其它 runtime yml

`chat / combat / interact / inv / mine / misc / models / render / slimefun / survival / test / toggles` —— 与甲飞无关，
需要哪一项再单独看对应文件即可。
