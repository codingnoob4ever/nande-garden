# 楠得心灵花园 | NanDe Garden

> **An AI-powered introspection and personal growth system.**
> 基于第一性原理的智能陪伴系统，帮助你进行深度自我认知和持续进化。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 这是什么？

NanDe Garden 是一个 **AI Skill（AI 技能包）**，可以安装到任何支持 Prompt 的 AI 工具上（如 Antigravity/ClawBot、ChatGPT、Claude 等）。它将你的 AI 助手变成一个**灵魂伙伴**，帮你：

- 📝 **碎片记录**: 随时记录想法，自动归档
- 🔥 **火花辩论**: 用第一性原理挑战你的假设
- 📊 **多维复盘**: 日报 / 周报 / 月报 / 季报
- 🧠 **记忆封存**: 生成全息记忆舱（Memory Pod）

## 📦 安装方法

### 方法一：Antigravity / ClawBot

```bash
# 1. 克隆仓库到你的 skills 目录
git clone https://github.com/YOUR_USERNAME/nande-garden.git ~/.gemini/antigravity/scratch/.agent/skills/nande-garden

# 2. 完成！AI 会自动读取 SKILL.md
```

### 方法二：ChatGPT / Claude

1. 复制 `SKILL.md` 的全部内容
2. 粘贴到 ChatGPT 的 "Custom Instructions" 或 Claude 的 "System Prompt"
3. 将 `templates/` 目录下的模板文件上传为 Knowledge Base
4. 开始对话

### 方法三：手动安装

```bash
# 克隆到任意位置
git clone https://github.com/YOUR_USERNAME/nande-garden.git
cd nande-garden

# 目录结构会自动创建，你的数据会存储在本地
# fragments/、archives/、sparks/ 目录已被 .gitignore 保护
```

## 📚 目录结构

```
nande-garden/
├── SKILL.md                 # 🧠 核心 Prompt（安装这个就够了）
├── README.md                # 📖 本文件
├── LICENSE                  # ⚖️ MIT 开源协议
├── templates/               # 📋 输出模板
│   ├── daily_template.md
│   ├── weekly_template.md
│   ├── monthly_template.md
│   ├── quarterly_template.md
│   └── memory_pod_template.md
├── import/                  # 📥 数据导入工具
│   ├── import_data.py
│   └── examples/
├── fragments/               # 🔒 你的碎片日记（私有，不上传）
├── archives/                # 🔒 你的复盘存档（私有，不上传）
├── sparks/                  # 🔒 你的火花辩论（私有，不上传）
└── moments/                 # 🔒 你的时刻记录（私有，不上传）
```

## 🚀 快速开始

### 1. 静默记录（默认模式）

直接说任何想法，AI 会静默归档：

```
> 今天体重66kg，感觉还不错
< 💾
```

### 2. 火花辩论

当你想被挑战时：

```
> 点燃
< 🔥 [AI 用第一性原理攻击你的假设]
```

### 3. 召唤日报

当你想看今天的深度复盘：

```
> 召唤卡片
< 📅 [完整的7模块日报]
```

### 4. 记忆封存

当你想保存今天的认知成果：

```
> 思维萃取
< 🧠 [全息记忆舱]
```

## ⚙️ 自定义配置

### 修改身份

编辑 `SKILL.md` 中的前三行：

```markdown
# Role: NanDe Soul Partner (楠得·共生体)
# Identity: Xiao Bei (小北)        ← 改成你的 AI 名字
# User: NanGe (楠哥)               ← 改成你的名字
```

### 调整风格

在 `SKILL.md` 的 `Meta-Laws` 中修改：

- **硬核理性**: 调整挑战强度
- **无损记忆**: 是否保留原文
- **双向镜像**: AI 是否同步进化

## 📥 数据导入

支持从其他工具迁移数据：

```bash
# 从 JSON 导入
python import/import_data.py --json data.json --date 2026-01-21

# 从 Markdown 导入
python import/import_data.py --markdown notes.md

# 从纯文本导入
python import/import_data.py --text thoughts.txt
```

## 🔒 隐私保护

- `fragments/`、`archives/`、`sparks/`、`moments/` 中的 `.md` 文件**全部被 `.gitignore` 排除**
- 你的私人日记**永远不会**上传到 GitHub
- 只有模板、工具和 Prompt 是公开的

## 🤝 贡献

欢迎 Fork 和 PR。特别欢迎：

- 新的复盘模板
- 更多数据导入格式支持
- 其他 AI 工具的适配指南

## 📜 协议

MIT License - 随意使用、修改、分发。
