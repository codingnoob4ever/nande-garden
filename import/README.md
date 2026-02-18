# 楠得心灵花园 - 数据导入指南

## 🎯 导入功能概述

数据导入工具允许你将其他AI对话、笔记应用或其他来源的内容导入到楠得心灵花园的碎片存档系统。

## 📦 支持的格式

### 1. JSON格式

#### 简化格式

```json
[
    "内容1",
    "内容2",
    "内容3"
]
```

#### 完整格式

```json
{
    "date": "2026-01-21",
    "fragments": [
        {"time": "09:30", "content": "内容1"},
        {"time": "14:00", "content": "内容2"}
    ]
}
```

**导入命令**:

```bash
python import/import_data.py --json data.json --date 2026-01-21
```

### 2. Markdown格式

支持多种Markdown格式：

```markdown
# 我的想法

[09:30] 带时间戳的内容

- 列表项内容1
* 列表项内容2

纯文本内容
```

**导入命令**:

```bash
python import/import_data.py --markdown notes.md
```

### 3. 纯文本格式

每行一条碎片：

```
内容1
内容2
内容3
```

**导入命令**:

```bash
python import/import_data.py --text thoughts.txt --date 2026-01-20
```

### 4. CSV格式

#### 带时间

```csv
time,content
09:30,内容1
14:00,内容2
```

#### 不带时间

```csv
content
内容1
内容2
```

**导入命令**:

```bash
python import/import_data.py --csv data.csv
```

### 5. ChatGPT导出格式

支持ChatGPT标准导出JSON格式。

**导入命令**:

```bash
python import/import_data.py --chatgpt chat_export.json
```

## 🚀 快速开始

### 1. 准备数据文件

选择任一支持的格式创建数据文件，或从其他应用导出数据。

### 2. 运行导入命令

```bash
cd /path/to/nande-garden
python import/import_data.py --json your_data.json
```

### 3. 查看导入结果

导入的碎片会自动保存到：

```
fragments/YYYY/MM-MonthName/YYYY-MM-DD.md
```

## 📋 常见用途

### 从Claude/ChatGPT导入对话

1. 复制对话内容
2. 创建JSON或Markdown文件
3. 运行导入命令

```bash
# 示例：导入Claude对话
python import/import_data.py --markdown claude_chat.md --date 2026-01-21
```

### 从Obsidian导入笔记

```bash
python import/import_data.py --markdown obsidian_note.md
```

### 从Excel导入数据

1. 导出为CSV
2. 运行导入

```bash
python import/import_data.py --csv excel_export.csv
```

## ⚙️ 高级选项

### 指定日期

```bash
python import/import_data.py --json data.json --date 2026-01-15
```

### 指定基础路径

```bash
python import/import_data.py --json data.json --base-path /path/to/nande-garden
```

### 查看帮助

```bash
python import/import_data.py --help
```

## 🔧 自动化处理

### 时间戳自动生成

如果数据中没有时间戳，工具会自动生成：

- 从09:00开始
- 每15分钟一条
- 示例：09:00, 09:15, 09:30, ...

### 去重处理

导入时会自动去除重复内容（相同时间+相同内容）。

### 合并处理

如果目标日期已有碎片文件，新导入的内容会自动合并并排序。

## 📝 最佳实践

### 1. 日常导入

每天结束时，将其他AI对话中的精华内容导入：

```bash
# 创建today.json
# 运行导入
python import/import_data.py --json today.json
```

### 2. 批量导入

整理历史记录时，按日期批量导入：

```bash
python import/import_data.py --json 2026-01-20.json --date 2026-01-20
python import/import_data.py --json 2026-01-21.json --date 2026-01-21
```

### 3. 多源整合

从不同来源导入到同一天：

```bash
python import/import_data.py --json claude_chat.json --date 2026-01-21
python import/import_data.py --markdown obsidian_note.md --date 2026-01-21
python import/import_data.py --text quick_thoughts.txt --date 2026-01-21
```

## 🔐 隐私保护

- 所有数据仅在本地处理
- 不会上传到任何服务器
- 导入前可以手动审查内容

## 🆘 常见问题

### Q: 导入后碎片顺序混乱？

A: 工具会自动按时间排序，检查时间戳格式是否正确。

### Q: 支持中文吗？

A: 完全支持UTF-8编码的中文内容。

### Q: 可以撤销导入吗？

A: 建议导入前备份碎片文件，或手动编辑fragments/目录下的文件。

### Q: 导入大量数据会很慢吗？

A: Python脚本处理速度较快，通常几秒内完成。

## 🎨 自定义格式

如需支持其他格式，可以修改 `import_data.py` 中的导入方法，或联系开发者。

---

**提示**: 查看 `import/examples/` 目录获取更多示例文件。
