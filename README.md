# AI 视频剧本 Skills

这个仓库是所有剧本技能的唯一维护源。Codex 实际使用的是指向仓库内各个技能目录的软链接，因此不会复制出多套代码；仓库更新后，本机技能同步更新。

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
