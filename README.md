# AI 视频剧本 Skills

这个仓库是所有剧本技能的唯一维护源。Codex 实际使用的是指向仓库内各个技能目录的软链接，因此不会复制出多套代码；仓库更新后，本机技能同步更新。

同事可以让支持本地文件和终端操作的 ChatGPT/Codex 客户端阅读 [同事安装使用说明.md](同事安装使用说明.md)，并按文档自动安装、自检和使用。普通网页聊天不能直接安装本地 Skills。

## 在新电脑首次部署

前提：已经安装 Codex、Git，并且这台电脑能够访问 GitHub 私有仓库。

```bash
mkdir -p "$HOME/.codex/skill-repos"
git clone git@github.com:thyong/aivideo-juben-skill.git "$HOME/.codex/skill-repos/aivideo-juben-skill"
"$HOME/.codex/skill-repos/aivideo-juben-skill/install.sh"
"$HOME/.codex/skill-repos/aivideo-juben-skill/doctor.sh"
```

看到 `Skill deployment check passed.` 即表示部署成功。之后新建一个 Codex 任务，让技能列表刷新。

## 日常升级

在任意目录执行：

```bash
"$HOME/.codex/skill-repos/aivideo-juben-skill/update.sh"
```

该命令会依次拉取 GitHub 最新版本、安装新增技能并运行部署自检。已有技能通过软链接使用，不需要重复复制。

## 查看已经部署的技能

```bash
"$HOME/.codex/skill-repos/aivideo-juben-skill/doctor.sh"
```

技能索引和中文命令见 [skills-index.yaml](skills-index.yaml)。

当前中文命令包括：

- `开始`：打开 AI 视频剧本助手的功能菜单。
- `技能清单`：按可生产、实验中和规划中查看全部能力。
- `原创剧本`：生成适配独立图生视频与硬切生产的一分钟原创动物人剧本。
- `剧本多版本`：保持剧情与核心内容不变，通过调整非核心视觉元素生成矩阵号差异版本，解决素材去重。
- `海洋风转换`：把现有剧本转换为固定海洋高端视觉系统。
- `剧本二创`：通过角色、道具或部分事件调整改编现有故事；确认方向和逐镜计划后再生成正式文件。
- `动物人转换`：保留原剧情和每个分镜的事件状态，用户确认角色映射后，仅将现有角色体系转换为动物人角色。

也可以不经过菜单，直接描述任务。例如“将这个文件转换为海洋系”；当输入完整时，助手会直接调用对应技能，只有缺少必要内容时才会询问。

## 常见问题

### GitHub 提示权限错误

先确认当前电脑已经配置 GitHub SSH：

```bash
ssh -T git@github.com
```

如果尚未配置，先在这台电脑登录 GitHub 或添加 SSH 公钥，再重新执行克隆命令。

### 提示目标技能已经存在

安装脚本不会覆盖真实目录，避免误删其他技能。如果目标只是旧软链接，可执行：

```bash
"$HOME/.codex/skill-repos/aivideo-juben-skill/install.sh" --repair
```

`--repair` 只替换软链接，不删除真实技能目录。

### 仓库放在了其他位置

没有关系。`install.sh` 会自动识别仓库所在位置并建立正确链接；`update.sh` 和 `doctor.sh` 也都从自身位置运行。
