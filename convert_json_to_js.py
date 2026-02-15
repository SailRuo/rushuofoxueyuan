#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 articles-index.json 转换为 articles-index.js
这样可以在 file:// 协议下直接加载
"""

import json
import os

def convert_json_to_js():
    """转换JSON为JS文件"""
    
    input_file = 'webapp/articles-index.json'
    output_file = 'webapp/articles-index.js'
    
    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        return
    
    # 读取JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成JS文件
    js_content = f"""// 文章索引数据
// 自动生成，请勿手动编辑
// 生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const articlesIndexData = {json.dumps(data, ensure_ascii=False, indent=2)};

// 导出数据
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = articlesIndexData;
}}
"""
    
    # 写入JS文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # 计算文件大小
    size_kb = os.path.getsize(output_file) / 1024
    
    print(f"✅ 转换成功!")
    print(f"📄 输入: {input_file}")
    print(f"📄 输出: {output_file}")
    print(f"📦 大小: {size_kb:.2f} KB")
    print(f"📊 文章数: {len(data)}")

if __name__ == '__main__':
    print("🔄 开始转换 JSON 到 JS...\n")
    convert_json_to_js()
    print("\n✨ 完成!")
