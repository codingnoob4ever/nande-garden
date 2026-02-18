#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楠得心灵花园 - 数据导入工具
Data Import Tool for NanDe Garden

支持从多种格式导入对话内容到碎片存档系统
"""

import json
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class FragmentImporter:
    """碎片导入器"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.fragments_dir = self.base_path / "fragments"
        
    def import_from_json(self, json_file: str, date: Optional[str] = None) -> int:
        """
        从JSON文件导入
        
        JSON格式示例:
        {
            "date": "2026-01-21",
            "fragments": [
                {"time": "09:30", "content": "内容1"},
                {"time": "10:15", "content": "内容2"}
            ]
        }
        
        或简化格式:
        [
            "内容1",
            "内容2"
        ]
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 支持两种格式
        if isinstance(data, dict):
            target_date = data.get('date', date or self._get_today())
            fragments = data.get('fragments', [])
        elif isinstance(data, list):
            target_date = date or self._get_today()
            # 简化格式，自动分配时间
            fragments = [{"time": self._generate_time(i), "content": item} 
                        for i, item in enumerate(data)]
        else:
            raise ValueError("不支持的JSON格式")
        
        return self._write_fragments(target_date, fragments)
    
    def import_from_markdown(self, md_file: str, date: Optional[str] = None) -> int:
        """
        从Markdown文件导入
        
        支持格式:
        1. 带时间戳: [HH:mm] 内容
        2. 列表形式: - 内容 或 * 内容
        3. 纯文本: 每行一条
        """
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        target_date = date or self._get_today()
        fragments = []
        
        # 解析不同格式
        lines = content.strip().split('\n')
        time_pattern = re.compile(r'^\[(\d{2}:\d{2})\]\s*(.+)$')
        list_pattern = re.compile(r'^[\-\*]\s+(.+)$')
        
        counter = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 格式1: [HH:mm] 内容
            match = time_pattern.match(line)
            if match:
                fragments.append({
                    "time": match.group(1),
                    "content": match.group(2)
                })
                continue
            
            # 格式2: - 内容
            match = list_pattern.match(line)
            if match:
                fragments.append({
                    "time": self._generate_time(counter),
                    "content": match.group(1)
                })
                counter += 1
                continue
            
            # 格式3: 纯文本
            if line:
                fragments.append({
                    "time": self._generate_time(counter),
                    "content": line
                })
                counter += 1
        
        return self._write_fragments(target_date, fragments)
    
    def import_from_text(self, text_file: str, date: Optional[str] = None, 
                        separator: str = '\n') -> int:
        """
        从纯文本文件导入
        
        参数:
            text_file: 文本文件路径
            date: 目标日期 (YYYY-MM-DD)
            separator: 分隔符，默认换行
        """
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        target_date = date or self._get_today()
        
        # 按分隔符分割
        items = [item.strip() for item in content.split(separator) if item.strip()]
        
        fragments = [
            {"time": self._generate_time(i), "content": item}
            for i, item in enumerate(items)
        ]
        
        return self._write_fragments(target_date, fragments)
    
    def import_from_csv(self, csv_file: str, date: Optional[str] = None) -> int:
        """
        从CSV文件导入
        
        CSV格式:
        time,content
        09:30,内容1
        10:15,内容2
        
        或无时间:
        content
        内容1
        内容2
        """
        fragments = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # 检查是否有time列
            has_time = 'time' in reader.fieldnames
            
            for i, row in enumerate(reader):
                if has_time:
                    fragments.append({
                        "time": row['time'],
                        "content": row['content']
                    })
                else:
                    # 只有content列
                    fragments.append({
                        "time": self._generate_time(i),
                        "content": row['content']
                    })
        
        target_date = date or self._get_today()
        return self._write_fragments(target_date, fragments)
    
    def import_from_chatgpt_export(self, json_file: str, date: Optional[str] = None) -> int:
        """
        从ChatGPT导出的JSON导入
        
        ChatGPT导出格式通常为:
        {
            "title": "对话标题",
            "mapping": {
                "id1": {
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["内容"]}
                    }
                }
            }
        }
        """
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        target_date = date or self._get_today()
        fragments = []
        
        # 解析ChatGPT格式
        mapping = data.get('mapping', {})
        counter = 0
        
        for node_id, node in mapping.items():
            message = node.get('message')
            if not message:
                continue
            
            author = message.get('author', {})
            role = author.get('role', '')
            
            # 只提取用户消息
            if role == 'user':
                content_obj = message.get('content', {})
                parts = content_obj.get('parts', [])
                
                for part in parts:
                    if isinstance(part, str) and part.strip():
                        fragments.append({
                            "time": self._generate_time(counter),
                            "content": part.strip()
                        })
                        counter += 1
        
        return self._write_fragments(target_date, fragments)
    
    def _write_fragments(self, date: str, fragments: List[Dict]) -> int:
        """写入碎片到文件"""
        # 解析日期
        dt = datetime.strptime(date, '%Y-%m-%d')
        year = dt.strftime('%Y')
        month = dt.strftime('%m-%B')
        filename = f"{date}.md"
        
        # 创建目录
        target_dir = self.fragments_dir / year / month
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 准备文件内容
        file_path = target_dir / filename
        
        # 读取现有内容（如果存在）
        existing_fragments = []
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取现有碎片
                pattern = re.compile(r'^\[(\d{2}:\d{2})\]\s*(.+)$', re.MULTILINE)
                existing_fragments = [
                    {"time": m.group(1), "content": m.group(2)}
                    for m in pattern.finditer(content)
                ]
        
        # 合并新旧碎片并去重
        all_fragments = existing_fragments + fragments
        unique_fragments = self._deduplicate_fragments(all_fragments)
        
        # 排序
        unique_fragments.sort(key=lambda x: x['time'])
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 碎片记录 - {date}\n\n")
            f.write(f"> 本文件记录{dt.year}年{dt.month}月{dt.day}日的所有原始输入碎片\n\n")
            f.write("---\n\n")
            f.write("## 📝 碎片流水\n\n")
            
            for frag in unique_fragments:
                f.write(f"[{frag['time']}] {frag['content']}\n\n")
            
            f.write("---\n\n")
            f.write("## 📊 统计信息\n\n")
            f.write(f"- **碎片数量**: {len(unique_fragments)}条\n")
            if unique_fragments:
                f.write(f"- **记录时段**: {unique_fragments[0]['time']} - {unique_fragments[-1]['time']}\n")
            f.write(f"- **导入时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        return len(fragments)
    
    def _deduplicate_fragments(self, fragments: List[Dict]) -> List[Dict]:
        """去重碎片"""
        seen = set()
        unique = []
        
        for frag in fragments:
            key = (frag['time'], frag['content'])
            if key not in seen:
                seen.add(key)
                unique.append(frag)
        
        return unique
    
    def _generate_time(self, index: int, start_hour: int = 9) -> str:
        """生成时间戳"""
        # 从9点开始，每15分钟一条
        total_minutes = start_hour * 60 + index * 15
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    
    def _get_today(self) -> str:
        """获取今天的日期"""
        return datetime.now().strftime('%Y-%m-%d')


def main():
    parser = argparse.ArgumentParser(
        description='楠得心灵花园 - 数据导入工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 从JSON导入
  python import_data.py --json conversations.json --date 2026-01-21
  
  # 从Markdown导入
  python import_data.py --markdown notes.md
  
  # 从文本导入
  python import_data.py --text thoughts.txt --date 2026-01-20
  
  # 从CSV导入
  python import_data.py --csv data.csv
  
  # 从ChatGPT导出导入
  python import_data.py --chatgpt chat_export.json
        """
    )
    
    parser.add_argument('--json', help='JSON文件路径')
    parser.add_argument('--markdown', '--md', help='Markdown文件路径')
    parser.add_argument('--text', '--txt', help='纯文本文件路径')
    parser.add_argument('--csv', help='CSV文件路径')
    parser.add_argument('--chatgpt', help='ChatGPT导出JSON文件路径')
    parser.add_argument('--date', help='目标日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--base-path', default='.', help='楠得花园根目录路径')
    
    args = parser.parse_args()
    
    importer = FragmentImporter(args.base_path)
    
    try:
        count = 0
        if args.json:
            count = importer.import_from_json(args.json, args.date)
            print(f"✅ 成功从JSON导入 {count} 条碎片")
        elif args.markdown:
            count = importer.import_from_markdown(args.markdown, args.date)
            print(f"✅ 成功从Markdown导入 {count} 条碎片")
        elif args.text:
            count = importer.import_from_text(args.text, args.date)
            print(f"✅ 成功从文本导入 {count} 条碎片")
        elif args.csv:
            count = importer.import_from_csv(args.csv, args.date)
            print(f"✅ 成功从CSV导入 {count} 条碎片")
        elif args.chatgpt:
            count = importer.import_from_chatgpt_export(args.chatgpt, args.date)
            print(f"✅ 成功从ChatGPT导出导入 {count} 条碎片")
        else:
            parser.print_help()
            return 1
        
        print(f"📁 碎片已保存到 fragments/")
        return 0
        
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return 1


if __name__ == '__main__':
    exit(main())
