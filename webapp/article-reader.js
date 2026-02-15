// 文章阅读器 - 加载并渲染文章

let articlesIndex = [];

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    await loadIndex();
    await loadArticle();
});

// 加载索引
async function loadIndex() {
    try {
        // 尝试fetch
        const response = await fetch('articles-index.json');
        articlesIndex = await response.json();
    } catch (error) {
        // 如果fetch失败,尝试XMLHttpRequest
        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', 'articles-index.json', false);
            xhr.send();
            if (xhr.status === 200 || xhr.status === 0) {
                articlesIndex = JSON.parse(xhr.responseText);
            }
        } catch (e) {
            console.error('加载索引失败:', e);
        }
    }
}

// 加载文章
async function loadArticle() {
    // 获取URL参数
    const urlParams = new URLSearchParams(window.location.search);
    const articleId = urlParams.get('id');
    
    if (!articleId) {
        showError('未指定文章ID');
        return;
    }
    
    // 加载文章JSON文件
    try {
        const response = await fetch(`articles/${articleId}.json`);
        if (!response.ok) {
            throw new Error('文章不存在');
        }
        
        const article = await response.json();
        renderArticle(article);
        
    } catch (error) {
        console.error('加载文章失败:', error);
        showError('加载文章失败: ' + error.message);
    }
}

// 渲染文章
function renderArticle(article) {
    // 构建文章HTML
    const articleHTML = `
        <div class="article-header">
            <h1 class="article-title">${article.title}</h1>
            <div class="article-meta">
                ${article.author ? `<span>📝 ${article.author}</span>` : ''}
                <span>📚 ${article.category}</span>
                ${article.tags.length > 0 ? `<span>🏷️ ${article.tags.join(', ')}</span>` : ''}
            </div>
        </div>
        
        ${article.summary ? `
            <div class="article-summary">
                ${article.summary}
            </div>
        ` : ''}
        
        ${article.sections.length > 0 ? `
            <nav class="article-toc">
                <h2 class="toc-title">📑 目录</h2>
                <ul class="toc-list">
                    ${article.sections.map((section, index) => `
                        <li><a href="#section-${index}">${section}</a></li>
                    `).join('')}
                </ul>
            </nav>
        ` : ''}
        
        <div class="article-content">
            ${renderContent(article.content)}
        </div>
    `;
    
    // 显示文章
    document.getElementById('loading').style.display = 'none';
    const articleEl = document.getElementById('article');
    articleEl.innerHTML = articleHTML;
    articleEl.style.display = 'block';
    
    // 更新页面标题
    document.title = `${article.title} - 如说修行网上佛学院`;
}

// 渲染内容
function renderContent(content) {
    let html = '';
    let sectionIndex = 0;
    
    for (const item of content) {
        switch (item.type) {
            case 'section':
                html += `<h4 id="section-${sectionIndex}" class="article-section-title">${item.text}</h4>`;
                sectionIndex++;
                break;
                
            case 'highlight':
                const style = item.style || {};
                const color = style.color || '#DC2626';
                html += `<p class="article-summary-inline" style="color: ${color}">${item.text}</p>`;
                break;
                
            case 'paragraph':
                html += `<p>${item.text}</p>`;
                break;
                
            case 'table':
                html += '<table class="article-table"><tbody>';
                for (const row of item.rows) {
                    html += '<tr>';
                    for (const cell of row) {
                        html += `<td>${cell}</td>`;
                    }
                    html += '</tr>';
                }
                html += '</tbody></table>';
                break;
        }
    }
    
    return html;
}

// 显示错误
function showError(message) {
    document.getElementById('loading').innerHTML = `
        <div style="text-align: center; padding: 4rem 2rem;">
            <svg width="64" height="64" fill="none" stroke="#EF4444" viewBox="0 0 24 24" style="margin: 0 auto 1rem;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <h2 style="color: #EF4444; margin-bottom: 1rem;">加载失败</h2>
            <p style="color: #64748B;">${message}</p>
            <a href="index.html" style="display: inline-block; margin-top: 2rem; padding: 0.75rem 2rem; background: #4F46E5; color: white; text-decoration: none; border-radius: 8px;">返回首页</a>
        </div>
    `;
}
