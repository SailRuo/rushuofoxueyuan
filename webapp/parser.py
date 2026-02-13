#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML内容解析器 - 解析现有佛学网站的HTML文件
提取文章标题、内容、颜色样式等信息
"""
import os
import re
import json
from bs4 import BeautifulSoup
from pathlib import Path

class ArticleParser:
    def __init__(self, base_dir="My Web Sites"):
        self.base_dir = Path(base_dir)
        self.articles = []
    
    def parse_html_file(self, file_path):
        """解析单个HTML文件"""
        try:
            with open(file_path, 'r', encoding='gb2312', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取标题
            title = soup.find('title')
            title_text = title.get_text() if title else file_path.stem
            
            # 提取主要内容（带颜色的段落）
            paragraphs = []
            for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4']):
                text = p.get_text(strip=True)
                if not text or text == '　':
                    continue
                
                # 提取颜色信息
                color = self._extract_color(p)
                font_size = self._extract_font_size(p)
                
                paragraphs.append({
                    'text': text,
                    'color': color,
                    'size': font_size,
                    'tag': p.name
                })
            
            return {
                'title': title_text,
                'file': str(file_path.relative_to(self.base_dir)),
                'paragraphs': paragraphs
            }
        
        except Exception as e:
            print(f"解析文件失败 {file_path}: {e}")
            return None
    
    def _extract_color(self, element):
        """提取元素的颜色"""
        # 检查style属性
        style = element.get('style', '')
        color_match = re.search(r'color:\s*([^;]+)', style)
        if color_match:
            return color_match.group(1).strip()
        
        # 检查color属性
        if element.get('color'):
            return element.get('color')
        
        # 检查font标签
        font = element.find('font')
        if font and font.get('color'):
            return font.get('color')
        
        return None
    
    def _extract_font_size(self, element):
        """提取字体大小"""
        font = element.find('font')
        if font and font.get('size'):
            return font.get('size')
        return None
    
    def scan_directory(self):
        """扫描目录下所有HTML文件"""
        html_files = list(self.base_dir.rglob('*.html')) + list(self.base_dir.rglob('*.htm'))
        
        print(f"找到 {len(html_files)} 个HTML文件")
        
        for file_path in html_files:
            article = self.parse_html_file(file_path)
            if article and article['paragraphs']:
                self.articles.append(article)
        
        print(f"成功解析 {len(self.articles)} 篇文章")
        return self.articles
    
    def save_to_json(self, output_file="articles.json"):
        """保存为JSON格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
        print(f"已保存到 {output_file}")

if __name__ == "__main__":
    parser = ArticleParser()
    parser.scan_directory()
    parser.save_to_json()
