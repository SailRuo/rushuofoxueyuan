#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成文章索引 - 从原始HTML文件提取元数据并生成新的文章文件
"""

import os
import json
import re
from html.parser import HTMLParser
from pathlib import Path

class ArticleParser(HTMLParser):
    """解析HTML文章,提取元数据和内容"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.author = ""
        self.summary = ""
        self.sections = []
        self.content_parts = []
        self.current_tag = ""
        self.current_attrs = {}
        self.in_title = False
        self.in_author = False
        self.in_summary = False
        self.in_section = False
        self.in_content = False
        self.summary_count = 0
        self.skip_nav = 0
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # 检测主内容表格
        if tag == 'table' and self.current_attrs.get('bgcolor') == '#FFFFFF':
            self.in_content = True
            return
        
        if not self.in_content:
            return
            
        # 检测标题 (H2标签)
        if tag == 'h2':
            self.in_title = True
            
        # 检测章节标题 (H4标签)
        if tag == 'h4':
            self.in_section = True
            self.content_parts.append(('section', ''))
            
        # 检测摘要 (红色楷体的段落)
        if tag == 'p' or tag == 'font':
            style = self.current_attrs.get('style', '')
            color = self.current_attrs.get('color', '')
            face = self.current_attrs.get('face', '')
            align = self.current_attrs.get('align', '')
            
            # 跳过导航
            if align == 'CENTER' and self.skip_nav < 3:
                self.skip_nav += 1
                return
            
            # 红色楷体通常是摘要
            if ('CC3300' in color or 'FF0000' in color) and ('楷体' in face or '楷体' in style):
                if self.summary_count < 3:
                    self.in_summary = True
                    self.content_parts.append(('summary', ''))
    
    def handle_endtag(self, tag):
        if tag == 'table' and self.in_content:
            self.in_content = False
            
        if tag == 'h2':
            self.in_title = False
        if tag == 'h4':
            self.in_section = False
        if tag == 'p' or tag == 'font':
            if self.in_summary:
                self.in_summary = False
                self.summary_count += 1
    
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        # 提取标题
        if self.in_title and not self.title:
            clean_title = re.sub(r'["\']', '', data)
            clean_title = re.sub(r'-如说修行.*', '', clean_title)
            self.title = clean_title.strip()
        
        # 提取章节
        if self.in_section:
            clean_section = re.sub(r'^\d+[、.]', '', data)
            clean_section = clean_section.strip()
            if clean_section and clean_section not in self.sections:
                self.sections.append(clean_section)
                if self.content_parts and self.content_parts[-1][0] == 'section':
                    self.content_parts[-1] = ('section', clean_section)
        
        # 提取摘要
        if self.in_summary and self.summary_count < 3:
            clean_summary = re.sub(r'["\']', '', data)
            clean_summary = clean_summary.strip()
            if clean_summary and len(clean_summary) > 10:
                if self.summary:
                    self.summary += " " + clean_summary
                else:
                    self.summary = clean_summary
                    
                if self.content_parts and self.content_parts[-1][0] == 'summary':
                    self.content_parts[-1] = ('summary', clean_summary)
        
        # 收集正文内容
        if self.in_content and not self.in_title and not self.skip_nav:
            if data and len(data) > 5:
                self.content_parts.append(('text', data))

def parse_html_file(file_path):
    """解析单个HTML文件"""
    try:
        encodings = ['gb2312', 'gbk', 'utf-8', 'gb18030']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if not content:
            print(f"⚠️  无法读取文件: {file_path}")
            return None
        
        parser = ArticleParser()
        parser.feed(content)
        
        return {
            'title': parser.title,
            'author': parser.author,
            'summary': parser.summary[:200] if parser.summary else "",
            'sections': parser.sections,
            'content_parts': parser.content_parts
        }
        
    except Exception as e:
        print(f"❌ 解析失败 {file_path}: {e}")
        return None

def generate_article_html(metadata, article_id):
    """生成新的文章HTML文件"""
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']} - 如说修行网上佛学院</title>
</head>
<body>
    <article>
        <h1>{metadata['title']}</h1>
"""
    
    if metadata['summary']:
        html += f"""        <div class="summary">{metadata['summary']}</div>\n"""
    
    if metadata['sections']:
        html += """        <nav class="toc">\n            <h2>目录</h2>\n            <ul>\n"""
        for i, section in enumerate(metadata['sections']):
            html += f"""                <li><a href="#section-{i}">{section}</a></li>\n"""
        html += """            </ul>\n        </nav>\n"""
    
    html += """        <div class="content">\n"""
    
    section_index = 0
    for part_type, part_content in metadata['content_parts']:
        if part_type == 'section':
            html += f"""            <h2 id="section-{section_index}">{part_content}</h2>\n"""
            section_index += 1
        elif part_type == 'summary':
            html += f"""            <p class="highlight">{part_content}</p>\n"""
        elif part_type == 'text':
            html += f"""            <p>{part_content}</p>\n"""
    
    html += """        </div>
    </article>
</body>
</html>
"""
    
    return html

def determine_category(filename):
    """根据文件名或路径判断分类"""
    if 'chan' in filename or '禅' in filename:
        return '禅修院'
    elif 'jingtu' in filename or '净土' in filename:
        return '净修院'
    else:
        return '修学园地'

def extract_tags(title, summary, sections):
    """从标题、摘要、章节中提取标签"""
    tags = []
    
    keywords = {
        '念佛': ['念佛', '持名', '净土'],
        '禅修': ['禅', '参禅', '打坐', '禅定'],
        '般若': ['般若', '智慧', '空性'],
        '戒律': ['戒', '持戒', '律'],
        '因果': ['因果', '业力', '轮回'],
        '菩提心': ['菩提心', '发心', '愿'],
        '经典': ['经', '论', '疏']
    }
    
    text = f"{title} {summary} {' '.join(sections)}"
    
    for tag, words in keywords.items():
        if any(word in text for word in words):
            tags.append(tag)
    
    return tags[:5]

def generate_index():
    """生成文章索引并创建新的文章文件"""
    
    source_dir = Path('rushuofoxueyuan/My Web Sites/xiuxueyd')
    output_dir = Path('webapp/articles')
    
    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html_files = sorted(source_dir.glob('*.html'))
    
    print(f"📚 找到 {len(html_files)} 个HTML文件")
    print("=" * 60)
    
    articles = []
    
    for i, file_path in enumerate(html_files, 1):
        filename = file_path.name
        
        if filename in ['index.htm', 'index.html', 'frame.html']:
            continue
        
        print(f"[{i}/{len(html_files)}] 解析: {filename}")
        
        metadata = parse_html_file(file_path)
        
        if not metadata or not metadata['title']:
            print(f"  ⚠️  跳过(无标题)")
            continue
        
        file_id = re.match(r'(\d+)', filename)
        article_id = file_id.group(1) if file_id else filename.replace('.html', '')
        
        # 生成新的文章HTML
        new_html = generate_article_html(metadata, article_id)
        new_file = output_dir / f"{article_id}.html"
        
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        article = {
            'id': article_id,
            'title': metadata['title'],
            'file': f"articles/{article_id}.html",
            'category': determine_category(filename),
            'tags': extract_tags(metadata['title'], metadata['summary'], metadata['sections']),
            'author': metadata['author'] or '',
            'summary': metadata['summary'],
            'sections': metadata['sections']
        }
        
        articles.append(article)
        
        print(f"  ✓ {article['title']}")
        if article['sections']:
            print(f"    章节: {', '.join(article['sections'][:3])}...")
    
    print("=" * 60)
    print(f"✅ 成功解析 {len(articles)} 篇文章")
    
    # 保存索引
    output_file = 'webapp/articles-index.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"💾 索引已保存到: {output_file}")
    
    categories = {}
    for article in articles:
        cat = article['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 统计信息:")
    print(f"  总文章数: {len(articles)}")
    for cat, count in categories.items():
        print(f"  {cat}: {count} 篇")
    
    size_kb = os.path.getsize(output_file) / 1024
    print(f"\n📦 索引文件大小: {size_kb:.2f} KB")
    
    return articles

if __name__ == '__main__':
    print("🚀 开始生成文章索引和新文章文件...\n")
    articles = generate_index()
    print("\n✨ 完成!")
