# 上传说明（给执行上传的人 / AI，自包含，无需其它上下文）

本目录 = 一个待发布到 GitHub 的完整项目包。
执行者只需照着本文件操作，**不要改动任何文件内容**。

---

## 0. 这个项目是什么

- 名字：**RustElytraClient — SLM 甲飞接管补丁版（非官方）**
- 内容：Minecraft 1.21.1 Fabric 模组 `RustElytraClient`（上游 GPL-3.0）的二进制补丁产物 + 补丁源码
- 作用：给该模组增加第 4 个任务模式「SLM 甲飞接管」，用 MagicBaritone + SlimefunHelper 的甲飞驱动飞行（不穿鞘翅、不掉耐久）
- 开源协议：**GPL-3.0**（因为上游是 GPL-3.0，衍生作品必须同协议发布，本目录已附 LICENSE 全文）
- 非官方声明：与模组原作者无关，不可声称获得原作者背书

## 1. 上传目标（新建仓库，不要 fork、不要往别人仓库 push）

| 项 | 建议值 |
| --- | --- |
| 仓库名 | `RustElytraClient-SLM` |
| 描述 | `RustElytraClient beta1.6 的非官方补丁：新增 SLM 甲飞接管模式（需 MagicBaritone + SlimefunHelper）` |
| 可见性 | Public |
| 初始化 | **不要**勾选 README / .gitignore / LICENSE（本目录已带，避免冲突） |
| License | GPL-3.0（GitHub 会自动识别根目录 LICENSE 文件） |
| Topics | `minecraft` `fabric` `baritone` `slimefunhelper` `elytra` `minecraft-mod` |
| 默认分支 | `main` |

## 2. 文件怎么放

**本目录（解压 zip 后的根目录）内的所有内容，原样放到仓库根目录。** 目录结构应为：

```
README.md                    # 项目说明（含「整个情况概述」）
UPLOAD.md                    # 本文件（可保留，也可删）
RELEASE_NOTES.md             # Release 正文模板
安装说明.md                   # 给用户的安装/使用说明
宣发文案.md                   # 视频宣发文案（可选，不想公开可删）
第三方声明与许可.md            # 许可证与合规说明（必须保留）
LICENSE                      # GPL-3.0 全文（必须保留）
CHECKSUMS.txt                # 全部文件校验和
release/
  RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar   # 本分支产物
  SHA256SUMS.txt
deps/                        # 必要依赖（第三方原版 jar，未修改）
  MagicBaritone-1.0.0-mc1.21.1-fabric.jar                  # LGPL-3.0
  SlimefunHelper-1.21.1-1.1.7.2.jar                        # CC0-1.0
  fabric-api-0.116.17+1.21.1.jar                           # Apache-2.0
config/                      # 推荐配置
  RSTConfig.json
baritone/settings.txt
slimefunhelper/runtime/*.yml # 13 个 SH 运行时配置
patches/src/                 # 补丁源码（GPL 合规所需）
  Patch2.java Patch4.java Patch6.java Patch7b.java Patch8.java T.java Verify.java
tools/
  build-release.ps1 repack3.py
licenses/
  MagicBaritone-LGPL-3.0.txt
docs/
  改动说明.md
  上游信息.md
```

> 说明：`deps/` 里是**第三方依赖的原版 jar**（未做任何修改），许可证分别是 LGPL-3.0 / CC0-1.0 / Apache-2.0，允许随包分发。
> 如果不想把第三方 jar 放仓库，也可以：仓库里只保留 `release/` + 源码 + 文档，把 `deps/` 三个 jar 作为 **Release 附件** 一起发布，并在 `安装说明.md` 里注明来源链接。

关键校验值（不要弄错版本）：

- jar：`RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`
- SHA-256：`1E96D83A298A03A150DACB566A62E0FC2B7F4E744DD89E24A022BC6C2E6B8D1A`

## 3. 上传方式（任选一种）

### 方式 A：网页上传（最简单，无需命令行/Token）

1. 打开 <https://github.com/new>，按第 1 节填好，创建空仓库
2. 进入仓库页面 → 点 **Add file → Upload files**
3. 把本目录**解压后**的全部文件/文件夹拖进去（保留目录结构）
4. 下方 Commit changes 填：`Initial release: SLM armor-fly takeover patch (GPL-3.0)`
5. 提交

### 方式 B：git 命令行（可选，需要 GitHub 账号凭据）

```bash
cd <本目录>
git init -b main
git config user.name  "<你的GitHub用户名>"
git config user.email "<你的GitHub邮箱>"
git add -A
git commit -m "Initial release: SLM armor-fly takeover patch (GPL-3.0)"
git remote add origin https://github.com/<用户名>/RustElytraClient-SLM.git
git push -u origin main
```

> 推送需要账号凭据：GitHub 密码不可用，需 Personal Access Token（classic 勾 `repo`；或 fine-grained 对目标仓库给 Contents: Read and write）。
> 命令示例：`git remote set-url origin https://<用户名>:<TOKEN>@github.com/<用户名>/RustElytraClient-SLM.git`

### 方式 C：gh CLI（如果目标机器装了）

```bash
gh repo create <用户名>/RustElytraClient-SLM --public \
  --description "RustElytraClient beta1.6 的非官方补丁：新增 SLM 甲飞接管模式（需 MagicBaritone + SlimefunHelper）"
git push -u origin main
```

## 4. 创建 Release（仓库建好之后必做）

| 项 | 值 |
| --- | --- |
| Tag | `v1.0.0` |
| Title | `v1.0.0 — SLM 甲飞接管补丁` |
| 正文 | 直接复制同目录 `RELEASE_NOTES.md` 的内容 |
| 附件 | `release/RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`、`release/SHA256SUMS.txt` |

网页操作：仓库右侧 **Releases → Draft a new release** → 填 Tag/Title/正文 → 拖入两个附件 → Publish release。

命令行（可选）：

```bash
gh release create v1.0.0 \
  release/RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar \
  release/SHA256SUMS.txt \
  --title "v1.0.0 — SLM 甲飞接管补丁" \
  --notes-file RELEASE_NOTES.md
```

## 5. 绝对不要做的事

1. **不要修改** `LICENSE`、`README.md` 里的上游链接与致谢、`docs/上游信息.md` 的版权信息
2. **不要把 MagicBaritone 或 SlimefunHelper 的 jar 放进仓库**（它们是独立许可证的第三方依赖，只写进依赖说明）
3. **不要更换许可证**（必须保持 GPL-3.0）
4. **不要 force push 到上游仓库**（`RSTminecraft/RustElytraClient`），只能推到自己新建的仓库
5. 不要声称这是官方版本、不要删掉“非官方补丁”说明

## 6. 上传完成后自检

- [ ] 仓库根目录能看到 `README.md`、`LICENSE`、`release/`、`patches/`、`docs/`、`tools/`
- [ ] GitHub 右侧显示 **GPL-3.0 license**
- [ ] Releases 里有 `v1.0.0`，且 jar 可下载
- [ ] 下载 jar 后校验 SHA-256 与 `1E96D83A...6B8D1A` 一致：
  - Windows：`Get-FileHash .\RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar -Algorithm SHA256`
  - Linux/macOS：`sha256sum RustElytraClient-1.21.1-beta1.6-slm-takeover-1.0.0.jar`
- [ ] README 中「非官方」「GPL-3.0」「依赖 MagicBaritone + SlimefunHelper」三段都在

## 7. 合规要点（GPL-3.0）

- 上游：<https://github.com/RSTminecraft/RustElytraClient>（GPL-3.0，对应 beta1.6 提交 `b7f60332`）
- 本仓库必须：
  - 保留 GPL-3.0 全文（`LICENSE`）
  - 提供对应源码：本包以 `patches/src/`（补丁源码）+ `tools/`（构建脚本）+ `release/` 产物 形式提供
  - 保留原作者版权声明与致谢（README 已写）
- 建议在仓库 About 里注明：`Unofficial patch for RustElytraClient (GPL-3.0)`

## 8. 备注

- 本项目涉及游戏自动化/作弊功能补丁，公开传播可能违反部分服务器规则，README 已附免责声明，**不要删除该段**
- 如果上传过程报 “filename too long / 乱码”：确认文件名保持 UTF-8；本包文件名都是 ASCII，只有目录内文档内容含中文
- 如需要改仓库名，README 里没有硬编码仓库地址，可自由改名
