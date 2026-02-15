// 如说修行 - 应用逻辑
let articles = [];
let searchIndex = [];
let currentCategory = 'all';

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    await loadArticles();
    buildSearchIndex();
    renderArticles();
    setupEventListeners();
});

// 加载文章数据
async function loadArticles() {
    try {
        const response = await fetch('articles-index.json');
        if (!response.ok) {
            throw new Error('Failed to load articles');
        }
        articles = await response.json();
        console.log(`✓ 加载了 ${articles.length} 篇文章`);
    } catch (error) {
        console.error('加载文章失败:', error);
        articles = [];
    }
}

// 构建搜索索引
function buildSearchIndex() {
    searchIndex = articles.map((article, index) => {
        const content = article.paragraphs
            .map(p => p.text)
            .join(' ')
            .toLowerCase();
        
        return {
            index,
            title: article.title.toLowerCase(),
            content,
            category: getCategoryFromFile(article.file)
        };
    });
}

// 从文件路径推断分类
function getCategoryFromFile(file) {
    if (file.includes('chan') || file.includes('禅') || file.includes('jingtu') || file.includes('净土')) {
        return '佛学';
    }
    if (file.includes('dao') || file.includes('道') || file.includes('taishang')) {
        return '道学';
    }
    if (file.includes('zhe') || file.includes('哲')) {
        return '哲学';
    }
    return '佛学'; // 默认
}

// 渲染文章列表
function renderArticles(filteredArticles = null) {
    const articleList = document.getElementById('articleList');
    const articlesToRender = filteredArticles || articles;
    
    if (articlesToRender.length === 0) {
        articleList.innerHTML = `
            <div class="col-span-full text-center py-16">
                <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-gray-500">未找到相关文章</p>
            </div>
        `;
        return;
    }
    
    articleList.innerHTML = articlesToRender.map((article, index) => {
        const category = getCategoryFromFile(article.file);
        const excerpt = article.paragraphs
            .slice(0, 3)
            .map(p => p.text)
            .join('')
            .substring(0, 120) + '...';
        
        const categoryColors = {
            '佛学': 'bg-bamboo/10 text-bamboo',
            '道学': 'bg-lotus/20 text-amber-700',
            '哲学': 'bg-blue-50 text-blue-700'
        };
        
        return `
            <article 
                class="article-card bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
                data-index="${index}"
                role="button"
                tabindex="0"
                aria-label="阅读文章：${article.title}"
            >
                <span class="inline-block px-3 py-1 rounded-full text-xs font-medium mb-3 ${categoryColors[category] || categoryColors['佛学']}">
                    ${category}
                </span>
                <h3 class="text-xl font-heading font-semibold mb-3 text-ink-900 group-hover:text-bamboo transition-colors duration-200">
                    ${article.title.replace(/-如说修行网上佛学院$/, '')}
                </h3>
                <p class="text-ink-500 text-sm leading-relaxed line-clamp-3">
                    ${excerpt}
                </p>
            </article>
        `;
    }).join('');
    
    // 添加点击和键盘事件
    document.querySelectorAll('.article-card').forEach(card => {
        card.addEventListener('click', () => {
            const index = parseInt(card.dataset.index);
            showArticle(index);
        });
        
        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const index = parseInt(card.dataset.index);
                showArticle(index);
            }
        });
    });
}

// 显示文章详情
function showArticle(index) {
    const article = articles[index];
    const articleList = document.getElementById('articleList');
    const articleDetail = document.getElementById('articleDetail');
    const articleContent = document.getElementById('articleContent');
    
    // 渲染文章内容（保留原有颜色）
    const content = `
        <h1 class="text-3xl md:text-4xl font-heading font-bold mb-8 text-ink-900 leading-tight">
            ${article.title.replace(/-如说修行网上佛学院$/, '')}
        </h1>
        <div class="prose prose-lg max-w-none">
            ${article.paragraphs.map(p => {
                const styles = [];
                if (p.color) styles.push(`color: ${p.color}`);
                if (p.size) {
                    const sizeMap = {
                        '1': '0.875rem', '2': '1rem', '3': '1.125rem',
                        '4': '1.25rem', '5': '1.5rem', '6': '1.875rem', '7': '2.25rem'
                    };
                    styles.push(`font-size: ${sizeMap[p.size] || '1rem'}`);
                }
                
                const styleAttr = styles.length ? `style="${styles.join('; ')}"` : '';
                const tag = ['h1', 'h2', 'h3'].includes(p.tag) ? 'h2' : 'p';
                const className = tag === 'h2' ? 'font-heading font-semibold mt-8 mb-4' : 'mb-4 leading-relaxed';
                
                return `<${tag} class="${className}" ${styleAttr}>${p.text}</${tag}>`;
            }).join('')}
        </div>
    `;
    
    articleContent.innerHTML = content;
    articleList.classList.add('hidden');
    articleDetail.classList.remove('hidden');
    
    // 平滑滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 搜索功能
function performSearch(query) {
    if (!query.trim()) {
        renderArticles();
        return;
    }
    
    const lowerQuery = query.toLowerCase();
    const results = searchIndex
        .filter(item => 
            item.title.includes(lowerQuery) || 
            item.content.includes(lowerQuery)
        )
        .map(item => articles[item.index]);
    
    renderArticles(results);
}

// 分类筛选
function filterByCategory(category) {
    currentCategory = category;
    
    // 更新导航样式
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.dataset.category === category) {
            link.classList.remove('text-ink-700');
            link.classList.add('text-bamboo');
        } else {
            link.classList.remove('text-bamboo');
            link.classList.add('text-ink-700');
        }
    });
    
    if (category === 'all') {
        renderArticles();
    } else {
        const filtered = articles.filter((article, index) => 
            searchIndex[index].category === category
        );
        renderArticles(filtered);
    }
}

// 设置事件监听
function setupEventListeners() {
    // 搜索框
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300); // 防抖
    });
    
    // 分类导航
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            filterByCategory(link.dataset.category);
        });
    });
    
    // 返回按钮
    document.getElementById('backBtn').addEventListener('click', () => {
        document.getElementById('articleList').classList.remove('hidden');
        document.getElementById('articleDetail').classList.add('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
