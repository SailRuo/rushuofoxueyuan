#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析HTML文章，生成结构化JSON文件
保留样式信息（颜色、字体等）
"""

import os
import json
import re
from html.parser import HTMLParser
from pathlib import Path

class StructuredArticleParser(HTMLParser):
    """解析HTML文章，生成结构化内容"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.author = ""
        self.summary = ""
        self.sections = []
        self.content = []  # 结构化内容
        
        self.current_tag = ""
        self.current_attrs = {}
        self.current_text = ""
        self.current_style = {}
        
        self.in_title = False
        self.in_section = False
        self.in_table = False
        self.in_content = True  # 默认开始收集内容
        self.skip_nav = False
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # 提取样式信息
        self.current_style = {
            'color': self.current_attrs.get('color', ''),
            'face': self.current_attrs.get('face', ''),
            'size': self.current_attrs.get('size', ''),
            'align': self.current_attrs.get('align', '')
        }
        
        # 检测标题 - H2标签
        if tag == 'h2':
            self.in_title = True
            self.current_text = ""
            
        # 检测章节 - H4标签
        if tag == 'h4':
            self.in_section = True
            self.current_text = ""
            
        # 检测表格
        if tag == 'table':
            self.in_table = True
            self.content.append({
                'type': 'table',
                'rows': []
            })
            
        # 检测表格行
        if tag == 'tr' and self.in_table:
            if self.content and self.content[-1]['type'] == 'table':
                self.content[-1]['rows'].append([])
                
        # 检测段落
        if tag == 'p':
            self.current_text = ""
            self.skip_nav = False
    
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.in_title = False
            if self.current_text.strip() and not self.title:
                # 清理标题
                title = self.current_text.strip()
                title = re.sub(r'-如说修行.*', '', title)
                title = re.sub(r'["\']', '', title)
                self.title = title
            self.current_text = ""
                
        if tag == 'h4':
            self.in_section = False
            if self.current_text.strip():
                # 清理章节标题（去掉序号）
                section_title = re.sub(r'^\d+[、.]', '', self.current_text).strip()
                section_title = re.sub(r'^[一二三四五六七八九十]+[、.]', '', section_title).strip()
                if section_title and len(section_title) > 1:
                    self.sections.append(section_title)
                    self.content.append({
                        'type': 'section',
                        'text': section_title
                    })
            self.current_text = ""
                
        if tag == 'table':
            self.in_table = False
            
        if tag == 'p':
            text = self.current_text.strip()
            if text and not self.skip_nav and len(text) > 1:
                # 判断内容类型
                content_type = 'paragraph'
                
                # 红色或深红色楷体 = 摘要/重要提示
                color = self.current_style.get('color', '').upper()
                font = self.current_style.get('face', '')
                
                if (('CC3300' in color or 'FF0000' in color or 'DC2626' in color) and 
                    ('楷体' in font or 'KaiTi' in font)):
                    content_type = 'highlight'
                    if not self.summary and len(text) > 10:
                        self.summary = text[:200]
                
                self.content.append({
                    'type': content_type,
                    'text': text,
                    'style': {
                        'color': self.current_style.get('color', ''),
                        'font': self.current_style.get('face', ''),
                        'align': self.current_style.get('align', '')
                    }
                })
            
            self.current_text = ""
            self.skip_nav = False
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        
        # 跳过导航文本
        if any(nav in data for nav in ['如说修行', '净修院', '禅修院', '修学园地', '网上佛学院']):
            self.skip_nav = True
            return
        
        # 跳过空白字符
        if data in ['　', ' ', '\n', '\r', '\t']:
            return
            
        # 收集文本
        if self.in_table:
            # 表格内容
            if self.content and self.content[-1]['type'] == 'table':
                if self.content[-1]['rows']:
                    self.content[-1]['rows'][-1].append(data)
        else:
            # 普通文本 - 累积到current_text
            if self.current_text:
                self.current_text += data
            else:
                self.current_text = data

def parse_and_generate(file_path):
    """解析HTML文件并生成结构化JSON"""
    try:
        # 尝试多种编码
        encodings = ['gb2312', 'gbk', 'utf-8', 'gb18030']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                used_encoding = encoding
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        if not content:
            print(f"  ⚠️  无法解码文件")
            return None
        
        # 解析
        parser = StructuredArticleParser()
        parser.feed(content)
        
        # 清理标题
        title = parser.title.strip()
        if not title:
            # 尝试从文件名提取标题
            filename = file_path.name
            # 去掉扩展名和数字前缀
            title = re.sub(r'^\d+', '', filename.replace('.html', ''))
            if not title or len(title) < 2:
                return None
        
        # 清理标题中的特殊字符和后缀
        title = re.sub(r'["\']', '', title)
        title = re.sub(r'-如说修行.*', '', title)
        title = re.sub(r'如说修行.*', '', title)
        title = title.strip()
        
        if not title or len(title) < 2:
            return None
        
        # 如果没有内容，跳过
        if not parser.content or len(parser.content) == 0:
            print(f"  ⚠️  无内容")
            return None
        
        return {
            'title': title,
            'author': parser.author,
            'summary': parser.summary,
            'sections': parser.sections,
            'content': parser.content
        }
        
    except Exception as e:
        print(f"  ❌ 解析失败: {e}")
        return None

def determine_category(filename):
    """根据文件名判断分类"""
    if 'chan' in filename or '禅' in filename:
        return '禅修院'
    elif 'jingtu' in filename or '净土' in filename:
        return '净修院'
    else:
        return '修学园地'

def extract_tags(title, summary, sections):
    """提取标签"""
    tags = []
    keywords = {
        '念佛': ['念佛', '持名', '净土'],
        '禅修': ['禅', '参禅', '打坐', '禅定'],
        '般若': ['般若', '智慧', '空性'],
        '戒律': ['戒', '持戒', '律'],
        '菩提心': ['菩提心', '发心', '愿'],
        '经典': ['经', '论', '疏']
    }
    
    text = f"{title} {summary} {' '.join(sections)}"
    
    for tag, words in keywords.items():
        if any(word in text for word in words):
            tags.append(tag)
    
    return tags[:5]

def main():
    """主函数"""
    print("🚀 开始生成结构化文章...\n")
    
    # 源目录和目标目录
    source_dir = Path('rushuofoxueyuan/My Web Sites/xiuxueyd')
    articles_dir = Path('webapp/articles')
    
    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return
    
    # 创建文章目录
    articles_dir.mkdir(exist_ok=True)
    
    # 获取所有HTML文件
    html_files = sorted(source_dir.glob('*.html'))
    
    print(f"📚 找到 {len(html_files)} 个HTML文件")
    print("=" * 60)
    
    articles_index = []
    success_count = 0
    
    for i, file_path in enumerate(html_files, 1):
        filename = file_path.name
        
        # 跳过索引页
        if filename in ['index.htm', 'index.html', 'frame.html']:
            continue
        
        print(f"[{i}/{len(html_files)}] 解析: {filename}")
        
        # 解析文件
        parsed = parse_and_generate(file_path)
        
        if not parsed or not parsed['title']:
            print(f"  ⚠️  跳过(无标题)")
            continue
        
        # 提取ID
        file_id = re.match(r'(\d+)', filename)
        article_id = file_id.group(1) if file_id else filename.replace('.html', '')
        
        # 构建完整文章数据
        article_data = {
            'id': article_id,
            'title': parsed['title'],
            'category': determine_category(filename),
            'tags': extract_tags(parsed['title'], parsed['summary'], parsed['sections']),
            'author': parsed['author'],
            'summary': parsed['summary'],
            'sections': parsed['sections'],
            'content': parsed['content']
        }
        
        # 保存文章JSON文件
        article_file = articles_dir / f"{article_id}.json"
        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        # 索引中只保留元数据
        articles_index.append({
            'id': article_data['id'],
            'title': article_data['title'],
            'category': article_data['category'],
            'tags': article_data['tags'],
            'author': article_data['author'],
            'summary': article_data['summary'],
            'sections': article_data['sections']
        })
        
        success_count += 1
        print(f"  ✓ {article_data['title']}")
        if article_data['sections']:
            print(f"    章节: {', '.join(article_data['sections'][:3])}...")
    
    print("=" * 60)
    print(f"✅ 成功生成 {success_count} 篇文章")
    
    # 保存索引
    index_file = 'webapp/articles-index.json'
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(articles_index, f, ensure_ascii=False, indent=2)
    
    print(f"💾 索引已保存到: {index_file}")
    print(f"💾 文章已保存到: {articles_dir}/")
    
    # 统计
    print("\n📊 统计信息:")
    print(f"  总文章数: {success_count}")
    
    categories = {}
    for article in articles_index:
        cat = article['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  {cat}: {count} 篇")
    
    # 文件大小
    index_size = os.path.getsize(index_file) / 1024
    total_size = sum(f.stat().st_size for f in articles_dir.glob('*.json')) / 1024
    
    print(f"\n📦 索引文件: {index_size:.2f} KB")
    print(f"📦 文章文件总计: {total_size:.2f} KB")
    
    print("\n✨ 完成!")

if __name__ == '__main__':
    main()
