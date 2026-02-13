# 部署指南

## 方案一：GitHub Pages（推荐）

### 优点
- 完全免费
- 自动HTTPS
- 可绑定自定义域名
- 全球CDN加速

### 步骤

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 仓库名：`rushuo-xuexing`（或任意名称）
   - 设为Public

2. **推送代码**
```bash
git init
git add .
git commit -m "初始化项目"
git remote add origin https://github.com/你的用户名/rushuo-xuexing.git
git branch -M main
git push -u origin main
```

3. **启用GitHub Pages**
   - 进入仓库 Settings
   - 左侧菜单找到 Pages
   - Source 选择 `main` 分支
   - 点击 Save

4. **访问网站**
   - 地址：`https://你的用户名.github.io/rushuo-xuexing/`
   - 通常5分钟内生效

### 自定义域名（可选）

1. 在域名DNS设置中添加CNAME记录：
   ```
   www  CNAME  你的用户名.github.io
   ```

2. 在GitHub Pages设置中填入自定义域名

---

## 方案二：Cloudflare Pages

### 优点
- 国内访问更快
- 免费额度更大
- 自动构建部署

### 步骤

1. **注册Cloudflare账号**
   - 访问 https://pages.cloudflare.com/

2. **连接GitHub仓库**
   - 点击 "Create a project"
   - 选择你的GitHub仓库
   - 构建设置留空（纯静态）

3. **部署**
   - 自动部署
   - 获得 `xxx.pages.dev` 域名

---

## 方案三：Gitee Pages（国内）

### 优点
- 国内访问快
- 中文界面

### 步骤

1. **创建Gitee仓库**
   - 访问 https://gitee.com/

2. **推送代码**
```bash
git remote add gitee https://gitee.com/你的用户名/rushuo-xuexing.git
git push gitee main
```

3. **启用Gitee Pages**
   - 进入仓库 -> 服务 -> Gitee Pages
   - 点击启动
   - 需要实名认证

---

## 更新内容流程

### 添加/修改文章

1. 编辑 `My Web Sites/` 中的HTML文件
2. 运行解析器：
```bash
python parser.py
```
3. 提交更新：
```bash
git add .
git commit -m "更新文章"
git push
```
4. 自动部署（1-5分钟）

### 修改样式

1. 编辑 `style.css`
2. 提交推送即可

---

## 性能优化建议

### 1. 压缩JSON
如果 `articles.json` 很大（>1MB），可以压缩：

```bash
# 安装工具
npm install -g json-minify

# 压缩
json-minify articles.json > articles.min.json
```

然后在 `app.js` 中改为加载 `articles.min.json`

### 2. 图片优化
- 使用WebP格式
- 压缩图片大小
- 使用CDN托管

### 3. 启用缓存
在仓库根目录创建 `_headers` 文件（Cloudflare Pages）：

```
/articles.json
  Cache-Control: public, max-age=3600

/*.css
  Cache-Control: public, max-age=86400

/*.js
  Cache-Control: public, max-age=86400
```

---

## 监控和分析

### Google Analytics（可选）

在 `index.html` 的 `</head>` 前添加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 故障排查

### 页面空白
- 检查浏览器控制台错误
- 确认 `articles.json` 存在
- 检查文件路径大小写

### 搜索不工作
- 确认 `articles.json` 格式正确
- 检查浏览器控制台

### 样式错乱
- 清除浏览器缓存
- 检查CSS文件路径

---

## 备份建议

1. GitHub仓库本身就是备份
2. 定期导出 `articles.json`
3. 保留原始HTML文件
