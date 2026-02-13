# 如说修行 - 现代化学习平台

## 项目简介

将传统佛学网站重构为现代化、简约、便捷的在线学习平台。

### 特点

- ✅ 纯静态网站，无需服务器
- ✅ 全站内容搜索（客户端索引）
- ✅ 保留原有文章颜色样式
- ✅ 响应式设计，支持手机/平板
- ✅ 支持多板块（佛学、道学、哲学）
- ✅ 本地管理，GitHub托管

## 技术栈

- **前端**: 原生 HTML/CSS/JavaScript（无框架依赖）
- **解析器**: Python + BeautifulSoup
- **托管**: GitHub Pages / Cloudflare Pages
- **搜索**: 客户端全文索引

## 使用步骤

### 1. 解析现有内容

```bash
# 安装依赖
pip install beautifulsoup4

# 运行解析器
python parser.py
```

这会生成 `articles.json` 文件，包含所有文章的结构化数据。

### 2. 本地预览

```bash
# 使用Python启动本地服务器
python -m http.server 8000

# 或使用Node.js
npx serve
```

访问 http://localhost:8000

### 3. 部署到GitHub Pages

```bash
# 初始化Git仓库
git init
git add .
git commit -m "初始化项目"

# 推送到GitHub
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main

# 在GitHub仓库设置中启用Pages
# Settings -> Pages -> Source: main branch
```

## 项目结构

```
├── index.html          # 主页
├── style.css           # 样式
├── app.js              # 前端逻辑
├── parser.py           # HTML解析器
├── articles.json       # 文章数据（自动生成）
├── My Web Sites/       # 原始HTML文件
└── README.md           # 说明文档
```

## 内容管理

### 添加新文章

1. 在 `My Web Sites/` 目录添加HTML文件
2. 运行 `python parser.py` 重新解析
3. 提交并推送到GitHub

### 修改文章

1. 编辑 `My Web Sites/` 中的HTML文件
2. 重新运行解析器
3. 推送更新

## 搜索功能

- 支持标题搜索
- 支持全文搜索
- 实时过滤结果
- 无需后端服务器

## 扩展板块

在 `app.js` 的 `getCategoryFromFile()` 函数中添加新分类：

```javascript
function getCategoryFromFile(file) {
    if (file.includes('dao')) return '道学';
    if (file.includes('zhe')) return '哲学';
    // 添加更多分类...
    return '佛学';
}
```

## 浏览器兼容性

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- IE11: ❌（不支持）

## License

本项目内容仅供学习交流使用。
