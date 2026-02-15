// 文章数据和搜索索引
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
        // 尝试fetch
        const response = await fetch('articles-index.json');
        articles = await response.json();
        console.log(`加载了 ${articles.length} 篇文章`);
    } catch (error) {
        console.log('fetch失败,尝试XMLHttpRequest:', error.message);
        
        // 尝试XMLHttpRequest(支持file://协议)
        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', 'articles-index.json', false);
            xhr.send();
            if (xhr.status === 200 || xhr.status === 0) {
                articles = JSON.parse(xhr.responseText);
                console.log(`通过XMLHttpRequest加载了 ${articles.length} 篇文章`);
            }
        } catch (e) {
            console.error('XMLHttpRequest也失败:', e);
            articles = [];
        }
    }
}

// 构建搜索索引
function buildSearchIndex() {
    searchIndex = articles.map((article, index) => {
        const content = `${article.title} ${article.summary} ${article.sections.join(' ')}`.toLowerCase();
        
        return {
            index,
            title: article.title.toLowerCase(),
            content,
            category: article.category
        };
    });
}

// 从文件路径推断分类
function getCategoryFromFile(file) {
    // 现在从索引中直接获取
    return 'all';
}

// 渲染文章列表
function renderArticles(filteredArticles = null) {
    const articleList = document.getElementById('articleList');
    const articlesToRender = filteredArticles || articles;
    
    if (articlesToRender.length === 0) {
        articleList.innerHTML = '<p style="text-align: center; color: #64748B; padding: 4rem;">暂无文章</p>';
        return;
    }
    
    articleList.innerHTML = articlesToRender.map((article) => {
        const summary = article.summary 
            ? (article.summary.length > 100 ? article.summary.substring(0, 100) + '...' : article.summary)
            : '点击查看详情...';
        
        return `
            <div class="article-card" onclick="window.location.href='article.html?id=${article.id}'">
                <span class="category">${article.category}</span>
                <h3>${article.title}</h3>
                <p class="excerpt">${summary}</p>
                ${article.tags && article.tags.length > 0 ? 
                    `<div class="tags">${article.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}</div>` : 
                    ''}
            </div>
        `;
    }).join('');
}

// 显示文章详情(已废弃,使用article.html)
function showArticle(index) {
    const article = articles[index];
    window.location.href = `article.html?id=${article.id}`;
}
    
    // 渲染文章内容（保留原有颜色）
    const content = `
        <h1>${article.title}</h1>
        ${article.paragraphs.map(p => {
            const style = [];
            if (p.color) style.push(`color: ${p.color}`);
            if (p.size) style.push(`font-size: ${getFontSize(p.size)}`);
            
            const styleAttr = style.length ? `style="${style.join('; ')}"` : '';
            const tag = p.tag === 'h1' || p.tag === 'h2' ? 'h2' : 'p';
            
            return `<${tag} ${styleAttr}>${p.text}</${tag}>`;
        }).join('')}
    `;
    
    articleContent.innerHTML = content;
    articleList.classList.add('hidden');
    articleDetail.classList.remove('hidden');
    
    // 滚动到顶部
    window.scrollTo(0, 0);
}

// 字体大小映射
function getFontSize(size) {
    const sizeMap = {
        '1': '0.8rem',
        '2': '0.9rem',
        '3': '1rem',
        '4': '1.2rem',
        '5': '1.4rem',
        '6': '1.6rem',
        '7': '1.8rem'
    };
    return sizeMap[size] || '1rem';
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
    
    if (results.length === 0) {
        document.getElementById('articleList').innerHTML = 
            '<p style="text-align: center; padding: 2rem; color: #999;">未找到相关文章</p>';
    }
}

// 分类筛选
function filterByCategory(category) {
    currentCategory = category;
    
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
    // 搜索按钮
    document.getElementById('searchBtn').addEventListener('click', () => {
        const query = document.getElementById('searchInput').value;
        performSearch(query);
    });
    
    // 搜索框回车
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch(e.target.value);
        }
    });
    
    // 分类导航
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
            link.classList.add('active');
            filterByCategory(link.dataset.category);
        });
    });
    
    // 返回按钮
    document.getElementById('backBtn').addEventListener('click', () => {
        document.getElementById('articleList').classList.remove('hidden');
        document.getElementById('articleDetail').classList.add('hidden');
    });
}

// 示例数据（用于演示）
function getDemoArticles() {
    return [
        {
            title: "了凡四训",
            file: "102lfsx.html",
            paragraphs: [
                { text: "余童年丧父，老母命弃举业学医，谓可以养生，可以济人，且习一艺以成名，尔父夙心也。", color: "#198a8a", size: "4", tag: "p" },
                { text: "后余在慈云寺，遇一老者，修髯伟貌，飘飘若仙，余敬礼之。", color: "#000000", size: "3", tag: "p" },
                { text: "语余曰：子仕路中人也，明年即进学，何不读书？", color: "#198a8a", size: "4", tag: "p" }
            ]
        },
        {
            title: "自在学佛",
            file: "xiuxueyd/001zyxuefo.html",
            paragraphs: [
                { text: "学佛的目的是：解决生死问题，也是每一个学佛人的伟大使命。", color: "#000000", size: "3", tag: "p" },
                { text: "学佛首先必须发菩提心，因为菩提心是成佛的第一伟大使命。", color: "#000000", size: "3", tag: "p" }
            ]
        }
    ];
}
