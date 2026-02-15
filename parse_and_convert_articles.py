#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能解析旧版HTML文章,生成结构化的新版文章
"""

import os
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict

class SmartArticleParser(HTMLParser):
    """智能HTML解析器 - 识别文章结构"""
    
    def __init__(self):
        super().__init__()
        self.reset_state()
        
    def reset_state(self):
        """重置解析状态"""
        # 文章元数据
        self.title = ""
        self.author = ""
        
        # 文章结构
        self.summary = []          # 摘要(红色楷体段落)
        self.toc = []              # 目录(带锚点的链接)
        self.sections = []         # 章节
        self.references = []       # 参考阅读
        
        # 当前状态
        self.current_section = None
        self.current_tag = ""
        self.current_attrs = {}
        self.in_main_content = False
        self.in_title = False
        self.in_toc_area = False
        self.in_reference_area = False
        self.skip_navigation = True  # 跳过顶部导航
        self.nav_count = 0
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        
        # 检测主内容区域(白色背景的表格)
        if tag == 'table':
            bgcolor = self.current_attrs.get('bgcolor', '').upper()
            if bgcolor == '#FFFFFF':
                self.in_main_content = True
        
        # 检测标题 (H2, 红色, 大字)
        if tag == 'h2' and self.in_main_content:
            self.in_title = True
            
        # 检测章节标题 (H4)
        if tag == 'h4' and self.in_main_content:
            self.current_section = {
                'id': f'section-{len(self.sections)}',
                'title': '',
                'content': []
            }
            
        # 检测目录链接
        if tag == 'a' and self.in_main_content:
            href = self.current_attrs.get('href', '')
            if href.startswith('#') and not self.in_reference_area:
                self.in_toc_area = True
    
    def handle_endtag(self, tag):
        if tag == 'h2':
            self.in_title = False
            self.skip_navigation = False  # 标题后开始正式内容
            
        if tag == 'h4' and self.current_section:
            if self.current_section['title']:
                self.sections.append(self.current_section)
            self.current_section = None
            
        if tag == 'table':
            bgcolor = self.current_attrs.get('bgcolor', '').upper()
            if bgcolor == '#FFFFFF':
                self.in_main_content = False
    
    def handle_data(self, data):
        data = data.strip()
        if not data or not self.in_main_content:
            return
        
        # 跳过顶部导航
        if self.skip_navigation:
            if '净修院' in data or '禅修院' in data or '修学园地' in data:
                self.nav_count += 1
                return
            if self.nav_count > 0 and self.nav_count < 3:
                return
        
        # 提取标题
        if self.in_title and not self.title:
            clean_title = re.sub(r'-如说修行.*', '', data)
            clean_title = re.sub(r'["\']', '', clean_title)
            self.title = clean_title.strip()
            return
        
        # 检测作者(标题后的短段落)
        if not self.author and self.title and len(data) < 20:
            if not any(char in data for char in ['、', '。', '，', '：']):
                self.author = data
                return
        
        # 检测摘要(红色楷体)
        if self.is_summary_style():
            if len(data) > 10 and len(self.summary) < 5:
                self.summary.append(data)
                return
        
        # 检测目录
        if self.in_toc_area:
            if len(data) > 3 and len(data) < 50:
                # 清理目录项
                clean_toc = re.sub(r'^\d+[、.]', '', data)
                clean_toc = clean_toc.strip()
                if clean_toc and clean_toc not in self.toc:
                    self.toc.append(clean_toc)
            return
        
        # 检测参考阅读
        if '参考阅读' in data or '相关阅读' in data:
            self.in_reference_area = True
            return
        
        if self.in_reference_area and self.current_tag == 'a':
            if len(data) > 3:
                self.references.append(data)
            return
        
        # 检测章节标题
        if self.current_section and not self.current_section['title']:
            # 清理章节标题
            clean_section = re.sub(r'^\d+[、.]', '', data)
            clean_section = clean_section.strip()
            if clean_section:
                self.current_section['title'] = clean_section
            return
        
        # 添加到当前章节内容
        if self.current_section and len(data) > 10:
            self.current_section['content'].append({
                'type': 'paragraph',
                'text': data,
                'tag': self.current_tag,
                'style': self.get_text_style()
            })
    
    def is_summary_style(self):
        """判断是否是摘要样式(红色楷体)"""
        color = self.current_attrs.get('color', '').upper()
        face = self.current_attrs.get('face', '')
        
        # 红色系
        red_colors = ['CC3300', 'FF0000', 'CC0000', '009999']
        is_red = any(c in color for c in red_colors)
        
        # 楷体
        is_kaiti = '楷体' in face
        
        return is_red and is_kaiti
    
    def get_text_style(self):
        """获取文本样式"""
        style = {}
        
        color = self.current_attrs.get('color', '')
        if color:
            style['color'] = color
            
        face = self.current_attrs.get('face', '')
        if face:
            style['font'] = face
            
        size = self.current_attrs.get('size', '')
        if size:
            style['size'] = size
        
        # 检测加粗
        if self.current_tag == 'b' or self.current_tag == 'strong':
            style['bold'] = True
        
        return style if style else None

def parse_article_file(file_path):
    """解析单个文章文件"""
    try:
        # 尝试多种编码
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
            return None
        
        # 解析HTML
        parser = SmartArticleParser()
        parser.feed(content)
        
        # 构建文章结构
        article = {
            'title': parser.title,
            'author': parser.author,
            'summary': ' '.join(parser.summary),
            'toc': parser.toc,
            'sections': parser.sections,
            'references': parser.references
        }
        
        return article
        
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return None

def convert_to_markdown(article, filename):
    """将文章转换为Markdown格式"""
    md = []
    
    # 标题
    md.append(f"# {article['title']}\n")
    
    # 作者
    if article['author']:
        md.append(f"**作者**: {article['author']}\n")
    
    # 摘要
    if article['summary']:
        md.append(f"> {article['summary']}\n")
    
    # 目录
    if article['toc']:
        md.append("## 目录\n")
        for i, item in enumerate(article['toc'], 1):
            md.append(f"{i}. [{item}](#section-{i-1})")
        md.append("")
    
    # 章节
    for section in article['sections']:
        md.append(f"## {section['title']}\n")
        md.append(f'<a name="section-{section["id"]}"></a>\n')
        
        for para in section['content']:
            text = para['text']
            
            # 应用样式
            if para.get('style'):
                style = para['style']
                if style.get('bold'):
                    text = f"**{text}**"
                if style.get('color') and '009999' in style['color']:
                    text = f"*{text}*"  # 绿色文字用斜体
            
            md.append(f"{text}\n")
        
        md.append("")
    
    # 参考阅读
    if article['references']:
        md.append("## 参考阅读\n")
        for ref in article['references']:
            md.append(f"- {ref}")
        md.append("")
    
    return '\n'.join(md)

def convert_to_json(article, filename):
    """将文章转换为JSON格式"""
    # 提取文章ID
    file_id = re.match(r'(\d+)', filename)
    article_id = file_id.group(1) if file_id else filename.replace('.html', '')
    
    # 提取标签
    tags = extract_tags(article)
    
    # 判断分类
    category = determine_category(article['title'], article['summary'])
    
    return {
        'id': article_id,
        'title': article['title'],
        'author': article['author'],
        'category': category,
        'tags': tags,
        'summary': article['summary'][:200] if article['summary'] else '',
        'toc': article['toc'],
        'sections': article['sections'],
        'references': article['references']
    }

def extract_tags(article):
    """从文章中提取标签"""
    tags = []
    
    text = f"{article['title']} {article['summary']} {' '.join(article['toc'])}"
    
    keywords = {
        '念佛': ['念佛', '持名', '净土', '往生', '极乐'],
        '禅修': ['禅', '参禅', '打坐', '禅定', '参究'],
        '般若': ['般若', '智慧', '空性', '金刚经', '心经'],
        '戒律': ['戒', '持戒', '律', '十善'],
        '因果': ['因果', '业力', '轮回', '感应'],
        '菩提心': ['菩提心', '发心', '愿', '慈悲'],
        '明心见性': ['明心', '见性', '开悟', '觉悟']
    }
    
    for tag, words in keywords.items():
        if any(word in text for word in words):
            tags.append(tag)
    
    return tags[:5]

def determine_category(title, summary):
    """判断文章分类"""
    text = f"{title} {summary}"
    
    if any(word in text for word in ['禅', '参禅', '打坐', '禅定', '虚云', '憨山']):
        return '禅修院'
    elif any(word in text for word in ['净土', '念佛', '往生', '极乐', '阿弥陀']):
        return '净修院'
    else:
        return '修学园地'

def main():
    """主函数"""
    print("🚀 开始解析和转换文章...\n")
    
    # 源目录
    source_dir = Path('rushuofoxueyuan/My Web Sites/xiuxueyd')
    
    # 输出目录
    output_dir = Path('webapp/articles')
    output_dir.mkdir(exist_ok=True)
    
    # 获取所有HTML文件
    html_files = sorted(source_dir.glob('*.html'))
    
    print(f"📚 找到 {len(html_files)} 个HTML文件")
    print("=" * 60)
    
    articles_data = []
    success_count = 0
    
    for i, file_path in enumerate(html_files, 1):
        filename = file_path.name
        
        # 跳过索引页
        if filename in ['index.htm', 'index.html', 'frame.html']:
            continue
        
        print(f"[{i}/{len(html_files)}] 解析: {filename}")
        
        # 解析文章
        article = parse_article_file(file_path)
        
        if not article or not article['title']:
            print(f"  ⚠️  跳过(无法解析)")
            continue
        
        print(f"  ✓ {article['title']}")
        
        # 显示结构信息
        if article['toc']:
            print(f"    目录: {len(article['toc'])} 项")
        if article['sections']:
            print(f"    章节: {len(article['sections'])} 个")
        
        # 转换为JSON
        article_json = convert_to_json(article, filename)
        articles_data.append(article_json)
        
        # 保存为JSON文件
        output_file = output_dir / filename.replace('.html', '.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(article_json, f, ensure_ascii=False, indent=2)
        
        # 可选: 也保存为Markdown
        # md_content = convert_to_markdown(article, filename)
        # md_file = output_dir / filename.replace('.html', '.md')
        # with open(md_file, 'w', encoding='utf-8') as f:
        #     f.write(md_content)
        
        success_count += 1
    
    print("=" * 60)
    print(f"✅ 成功转换 {success_count} 篇文章")
    
    # 生成索引
    index_file = Path('webapp/articles-index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 索引已保存到: {index_file}")
    
    # 统计信息
    print("\n📊 统计信息:")
    print(f"  总文章数: {len(articles_data)}")
    
    categories = defaultdict(int)
    for article in articles_data:
        categories[article['category']] += 1
    
    for cat, count in categories.items():
        print(f"  {cat}: {count} 篇")
    
    # 文件大小
    index_size = os.path.getsize(index_file) / 1024
    print(f"\n📦 索引文件大小: {index_size:.2f} KB")
    
    print("\n✨ 完成!")

if __name__ == '__main__':
    main()
