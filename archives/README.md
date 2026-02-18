# 楠得心灵花园 - 存档系统

## 📂 存档结构说明

这个目录用于自动存储所有复盘内容，按时间维度分层管理。

## 📁 目录层次

```
archives/
├── daily/          # 日报存档（每日6模块完整复盘）
│   └── YYYY/
│       └── MM-MonthName/
│           └── YYYY-MM-DD.md
│
├── weekly/         # 周报存档（7天趋势与模式分析）
│   └── YYYY/
│       └── WXX_YYYY-MM-DD_to_YYYY-MM-DD.md
│
├── monthly/        # 月报存档（30天战略复盘）
│   └── YYYY/
│       └── YYYY-MM-MonthName.md
│
└── quarterly/      # 季报存档（90天人生校准）
    └── YYYY/
        └── YYYY-QX.md
```

## 🔄 自动化流程

### 日报存档

- **触发**: 每次"召唤卡片"生成日报后自动保存
- **路径**: `daily/YYYY/MM-MonthName/YYYY-MM-DD.md`
- **示例**: `daily/2026/01-January/2026-01-21.md`

### 周报存档

- **触发**: 每次"召唤周报"后自动保存
- **路径**: `weekly/YYYY/WXX_StartDate_to_EndDate.md`
- **示例**: `weekly/2026/W03_2026-01-13_to_2026-01-19.md`

### 月报存档

- **触发**: 每次"召唤月报"后自动保存
- **路径**: `monthly/YYYY/YYYY-MM-MonthName.md`
- **示例**: `monthly/2026/2026-01-January.md`

### 季报存档

- **触发**: 每次"召唤季报"后自动保存
- **路径**: `quarterly/YYYY/YYYY-QX.md`
- **示例**: `quarterly/2026/2026-Q1.md`

## 📊 存档文件格式

所有存档文件均为Markdown格式，包含：

- 完整的复盘内容
- 生成时间戳
- 元数据（关键词、标签等）

## 🔍 查阅建议

- **每日回顾**: 浏览daily目录，重温某一天的细节
- **每周总结**: 查看weekly目录，识别行为模式
- **每月战略**: 翻阅monthly目录，调整目标方向
- **每季校准**: 研究quarterly目录，进行人生复盘

## ⚠️ 注意事项

- 所有文件自动生成，无需手动创建
- 文件名遵循严格的时间格式，便于检索
- 建议定期备份整个archives目录
- 可通过关键词搜索快速定位历史内容
