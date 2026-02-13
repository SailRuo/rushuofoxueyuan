# 如说修行 - 设计系统

## 产品定位
传统文化学习平台 - 佛学/道学/哲学在线教育

## 设计原则

### 核心价值
- **宁静致远** - 营造平和的学习氛围
- **传统与现代** - 传统文化 + 现代设计语言
- **专注阅读** - 优化长文本阅读体验
- **尊重内容** - 保留原文颜色和格式

---

## 视觉风格

### 主题：禅意极简 (Zen Minimalism)

**特征：**
- 大量留白，呼吸感强
- 柔和的色彩过渡
- 优雅的排版
- 细腻的微交互

---

## 色彩系统

### 主色调 - 禅意配色

```css
/* 主色 - 墨色系 */
--ink-900: #1a1a1a;      /* 深墨 - 标题 */
--ink-700: #2d2d2d;      /* 中墨 - 正文 */
--ink-500: #666666;      /* 淡墨 - 辅助文字 */
--ink-300: #999999;      /* 浅墨 - 说明文字 */

/* 辅助色 - 自然色系 */
--bamboo: #4a7c59;       /* 竹绿 - 主要操作 */
--lotus: #d4a574;        /* 莲金 - 强调 */
--tea: #8b7355;          /* 茶褐 - 次要操作 */
--mist: #e8f4f8;         /* 雾蓝 - 背景 */

/* 语义色 */
--zen-bg: #faf9f7;       /* 宣纸白 */
--zen-card: #ffffff;     /* 纯白卡片 */
--zen-border: #e5e5e5;   /* 淡边框 */
--zen-shadow: rgba(0,0,0,0.04); /* 轻阴影 */

/* 保留原文颜色 */
--sutra-red: #cc3300;    /* 经文红 */
--sutra-green: #198a8a;  /* 经文绿 */
--sutra-blue: #0066cc;   /* 经文蓝 */
```

### 渐变

```css
/* 页面背景 */
background: linear-gradient(135deg, #faf9f7 0%, #f0ede8 100%);

/* 卡片光泽 */
background: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
```

---

## 字体系统

### 中文字体栈

```css
font-family: 
  "Source Han Serif CN",    /* 思源宋体 - 优雅 */
  "Noto Serif SC",          /* 备选宋体 */
  "STSong",                 /* 华文宋体 */
  "SimSun",                 /* 宋体 */
  serif;

/* 标题使用 */
font-family:
  "Source Han Sans CN",     /* 思源黑体 */
  "Noto Sans SC",
  "PingFang SC",
  "Microsoft YaHei",
  sans-serif;
```

### 字号层级

```css
--text-xs: 0.75rem;    /* 12px - 标签 */
--text-sm: 0.875rem;   /* 14px - 辅助 */
--text-base: 1rem;     /* 16px - 正文 */
--text-lg: 1.125rem;   /* 18px - 大正文 */
--text-xl: 1.25rem;    /* 20px - 小标题 */
--text-2xl: 1.5rem;    /* 24px - 标题 */
--text-3xl: 1.875rem;  /* 30px - 大标题 */
--text-4xl: 2.25rem;   /* 36px - 主标题 */
```

### 行高

```css
--leading-tight: 1.4;   /* 标题 */
--leading-normal: 1.8;  /* 正文 */
--leading-relaxed: 2.0; /* 经文 */
```

---

## 布局系统

### 容器宽度

```css
--container-sm: 640px;   /* 移动端 */
--container-md: 768px;   /* 平板 */
--container-lg: 1024px;  /* 桌面 */
--container-xl: 1280px;  /* 大屏 */

/* 阅读最佳宽度 */
--reading-width: 720px;  /* 65-75字符/行 */
```

### 间距系统

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-24: 6rem;     /* 96px */
```

---

## 组件设计

### 导航栏

```
样式：浮动式，半透明毛玻璃
位置：顶部居中，距离边缘 24px
高度：64px
背景：rgba(255,255,255,0.8) + backdrop-blur(12px)
阴影：0 4px 24px rgba(0,0,0,0.06)
```

### 文章卡片

```
布局：网格 (3列桌面, 2列平板, 1列手机)
间距：24px
圆角：12px
阴影：0 2px 8px rgba(0,0,0,0.04)
悬停：上移 -4px, 阴影加深
过渡：transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)
```

### 搜索框

```
样式：圆角胶囊
高度：48px
圆角：24px
边框：1px solid var(--zen-border)
聚焦：边框变为 var(--bamboo), 阴影 0 0 0 3px rgba(74,124,89,0.1)
```

### 按钮

```css
/* 主按钮 */
background: var(--bamboo);
color: white;
padding: 12px 32px;
border-radius: 8px;
transition: all 0.2s;
hover: brightness(1.1);

/* 次按钮 */
background: transparent;
border: 1px solid var(--zen-border);
color: var(--ink-700);
hover: background: var(--mist);
```

---

## 动效系统

### 过渡时长

```css
--duration-fast: 150ms;     /* 快速反馈 */
--duration-base: 250ms;     /* 标准过渡 */
--duration-slow: 400ms;     /* 复杂动画 */
```

### 缓动函数

```css
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

### 微交互

```css
/* 卡片悬停 */
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

/* 按钮点击 */
.button:active {
  transform: scale(0.98);
}

/* 页面切换 */
.fade-enter {
  opacity: 0;
  transform: translateY(20px);
}
```

---

## 响应式断点

```css
/* Mobile First */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

---

## 无障碍设计

### 对比度
- 正文：至少 4.5:1
- 大文本：至少 3:1
- 交互元素：至少 3:1

### 焦点状态
```css
:focus-visible {
  outline: 2px solid var(--bamboo);
  outline-offset: 2px;
}
```

### 键盘导航
- Tab 顺序合理
- 所有交互元素可聚焦
- 跳过导航链接

---

## 图标系统

使用 **Lucide Icons** (简洁、优雅)

```html
<!-- 搜索 -->
<svg class="w-5 h-5"><use href="#search"/></svg>

<!-- 分类 -->
<svg class="w-5 h-5"><use href="#book-open"/></svg>

<!-- 返回 -->
<svg class="w-5 h-5"><use href="#arrow-left"/></svg>
```

---

## 反模式（避免）

❌ 不使用 emoji 作为图标
❌ 不使用过于鲜艳的颜色
❌ 不使用过多动画
❌ 不使用小于 14px 的字号
❌ 不使用纯黑 (#000000)
❌ 不使用过窄的行高 (<1.5)

---

## 实现技术栈

- **HTML5** - 语义化标签
- **Tailwind CSS** - 原子化样式
- **Alpine.js** - 轻量级交互（可选）
- **原生 JS** - 搜索和路由
