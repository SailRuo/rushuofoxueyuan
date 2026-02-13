#!/usr/bin/env python
# -*- coding: utf-8 -*-

files = [
    ('rushuofoxueyuan/My Web Sites/000jxdg.html', 'temp_jxdg.txt'),
    ('rushuofoxueyuan/My Web Sites/xiuxueyd/001zyxuefo.html', 'temp_zyxuefo.txt'),
    ('rushuofoxueyuan/My Web Sites/000jxdg-chan.html', 'temp_jxdg_chan.txt'),
]

for input_file, output_file in files:
    try:
        with open(input_file, 'rb') as f:
            content = f.read().decode('gb2312', errors='ignore')
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(content)
        print(f'✓ {input_file} -> {output_file}')
    except Exception as e:
        print(f'✗ {input_file}: {e}')

print('\nDone!')
