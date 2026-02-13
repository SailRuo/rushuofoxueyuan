// 如说修行网上佛学院 - 重新设计版本
// 基于 UI/UX Pro Max 设计系统

// 全局状态
let articlesData = [];
let currentSection = 'home';
let searchTimeout = null;

// 课程数据结构
const courseData = {
    jingxiu: {
        name: '净修院',
        goal: '念佛往生，一心不乱',
        color: '#4F46E5',
        semesters: [
            {
                number: '第一学年',
                title: '一、断恶行善',
                goal: '建立正确知见',
                courses: [
                    { title: '地藏菩萨本愿经', file: '201_42.html' },
                    { title: '了凡四训', file: '102lfsx.html' },
                    { title: '俞净意公遇灶神记', file: '103yjy.html' },
                    { title: '王凤仪嘉言录', file: '105wangfengyijiayanlu.html' },
                    { title: '感应篇', file: '104ganyingp.html' }
                ]
            },
            {
                number: '第二学年',
                title: '二、持戒为本',
                goal: '持戒修行',
                courses: [
                    { title: '佛说四十二章经', file: '201_42.html' },
                    { title: '八大人觉经', file: '202bada.html' },
                    { title: '佛遗教经', file: '203foyj.html' },
                    { title: '十善业道经', file: '204ssydj.html' },
                    { title: '大念住经', file: '204danian.html' }
                ]
            },
            {
                number: '第三、四学年',
                title: '三、般若破妄',
                goal: '理论与实践结合',
                courses: [
                    { title: '金刚经', file: '301jgj.html' },
                    { title: '心经', file: '302xinj.html' },
                    { title: '六祖坛经', file: '303liuzutanjing.html' },
                    { title: '佛藏经', file: '304fozangj.html' },
                    { title: '真心直说', file: '502zhenxinzhishuojingjie.html' }
                ]
            },
            {
                number: '第五、六学年',
                title: '四、极乐为归',
                goal: '念佛往生',
                courses: [
                    { title: '阿弥陀经', file: '401amtj.html' },
                    { title: '念佛论', file: '402nianfolun.html' },
                    { title: '禅净要旨', file: '403chanjing.html' },
                    { title: '无量寿经会义', file: 'xiuxueyd/239wuliangshoujing-huiyi.html' },
                    { title: '念佛三昧摸象记', file: '404nianfosanmei.html' }
                ]
            }
        ]
    },
    chanxiu: {
        name: '禅修院',
        goal: '明心见性，顿悟成佛',
        color: '#D97706',
        semesters: [
            {
                number: '第一学年',
                title: '一、断恶行善',
                goal: '发菩提心',
                courses: [
                    { title: '地藏菩萨本愿经', file: '201_42.html' },
                    { title: '了凡四训', file: '102lfsx.html' },
                    { title: '俞净意公遇灶神记', file: '103yjy.html' },
                    { title: '王凤仪嘉言录', file: '105wangfengyijiayanlu.html' },
                    { title: '感应篇', file: '104ganyingp.html' }
                ]
            },
            {
                number: '第二学年',
                title: '二、持戒为本',
                goal: '戒定慧',
                courses: [
                    { title: '佛说四十二章经', file: '201_42.html' },
                    { title: '八大人觉经', file: '202bada.html' },
                    { title: '佛遗教经', file: '203foyj.html' },
                    { title: '十善业道经', file: '204ssydj.html' },
                    { title: '大念住经', file: '204danian.html' }
                ]
            },
            {
                number: '第三、四学年',
                title: '三、般若破妄',
                goal: '禅修实践',
                courses: [
                    { title: '金刚经', file: '301jgj.html' },
                    { title: '心经', file: '302xinj.html' },
                    { title: '六祖坛经', file: '303liuzutanjing.html' },
                    { title: '佛藏经选注', file: '304fozangj.html' },
                    { title: '真心直说', file: '502zhenxinzhishuojingjie.html' }
                ]
            },
            {
                number: '第五、六学年',
                title: '四、定慧等持',
                goal: '明心见性',
                courses: [
                    { title: '二入四行论', file: 'xiuxueyd/011errusx.html' },
                    { title: '修心诀', file: '502xiuxinjue.html' },
                    { title: '白云心要（观心宝笈）', file: '002baiyunxy.html' },
                    { title: '禅净要旨', file: '403chanjing.html' },
                    { title: '圆觉经', file: '502yuanjuejingjj.html' }
                ]
            }
        ]
    }
};

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initSearch();
    loadArticles();
});

// 导航初始化
function initNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const section = tab.dataset.section;
            switchSection(section);
        });
        
        // 键盘导航
        tab.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const section = tab.dataset.section;
                switchSection(section);
            }
        });
    });
}

// 切换板块
function switchSection(section) {
    currentSection = section;
    
    // 更新导航状态
    document.querySelectorAll('.nav-tab').forEach(tab => {
        const isActive = tab.dataset.section === section;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });
    
    // 更新内容显示
    document.querySelectorAll('.section-view').forEach(view => {
        view.classList.toggle('active', view.id === section);
    });
    
    // 加载对应内容
    if (section === 'jingxiu' && !document.querySelector('#jingxiuContent .semester-card')) {
        renderSemesters('jingxiu');
    } else if (section === 'chanxiu' && !document.querySelector('#chanxiuContent .semester-card')) {
        renderSemesters('chanxiu');
    } else if (section === 'xiuxue' && !document.querySelector('#xiuxueContent .article-card')) {
        renderArticles();
    }
    
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 渲染学期课程
function renderSemesters(section) {
    const container = document.getElementById(`${section}Content`);
    const data = courseData[section];
    
    if (!data) return;
    
    const html = data.semesters.map(semester => `
        <div class="semester-card">
            <span class="semester-number">${semester.number}</span>
            <h3 class="semester-title">${semester.title}</h3>
            <p class="semester-goal">${semester.goal}</p>
            <ul class="course-list">
                ${semester.courses.map(course => `
                    <li class="course-item">${course.title}</li>
                `).join('')}
            </ul>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 搜索初始化
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });
}

// 执行搜索
function performSearch(query) {
    if (!query.trim()) {
        if (currentSection === 'xiuxue') {
            renderArticles();
        }
        return;
    }
    
    const lowerQuery = query.toLowerCase();
    const filtered = articlesData.filter(article => 
        article.title.toLowerCase().includes(lowerQuery) ||
        (article.paragraphs && article.paragraphs.some(p => 
            p.text && p.text.toLowerCase().includes(lowerQuery)
        ))
    );
    
    if (currentSection === 'xiuxue') {
        renderArticles(filtered);
    } else {
        // 切换到修学园地显示搜索结果
        switchSection('xiuxue');
        renderArticles(filtered);
    }
}

// 加载文章数据
async function loadArticles() {
    try {
        const response = await fetch('articles.json');
        if (!response.ok) {
            throw new Error('Failed to load articles');
        }
        articlesData = await response.json();
        console.log(`成功加载 ${articlesData.length} 篇文章`);
    } catch (error) {
        console.error('加载文章失败:', error);
        articlesData = [];
    }
}

// 渲染文章列表
function renderArticles(articles = null) {
    const container = document.getElementById('xiuxueContent');
    const data = articles || articlesData;
    
    if (!data || data.length === 0) {
        container.innerHTML = `
            <div class="loading">
                <p>暂无文章数据</p>
            </div>
        `;
        return;
    }
    
    const html = data.map((article, index) => `
        <article class="article-card" onclick="showArticle(${index})" role="button" tabindex="0">
            <h3 class="article-title">${article.title || '无标题'}</h3>
            <div class="article-meta">
                <span class="article-tag">${getCategoryFromFile(article.file)}</span>
                ${article.paragraphs ? `<span class="article-tag">${article.paragraphs.length} 段</span>` : ''}
            </div>
        </article>
    `).join('');
    
    container.innerHTML = html;
    
    // 添加键盘导航
    document.querySelectorAll('.article-card').forEach((card, index) => {
        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                showArticle(index);
            }
        });
    });
}

// 获取文章分类
function getCategoryFromFile(file) {
    if (!file) return '佛学';
    
    const lower = file.toLowerCase();
    if (lower.includes('dao') || lower.includes('taishang') || lower.includes('yjy')) {
        return '道学';
    }
    if (lower.includes('zhe') || lower.includes('wang')) {
        return '哲学';
    }
    if (lower.includes('chan') || lower.includes('juezhichan')) {
        return '禅修';
    }
    if (lower.includes('nianfo') || lower.includes('amtj') || lower.includes('jingtu')) {
        return '净土';
    }
    return '佛学';
}

// 显示文章详情
function showArticle(index) {
    const article = articlesData[index];
    if (!article) return;
    
    // 创建模态框显示文章内容
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--space-xl);
        animation: fadeIn 200ms ease;
    `;
    
    const content = document.createElement('div');
    content.style.cssText = `
        background: white;
        border-radius: 16px;
        padding: var(--space-2xl);
        max-width: 800px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: var(--shadow-xl);
    `;
    
    const paragraphsHtml = article.paragraphs ? article.paragraphs.map(p => {
        const style = `
            color: ${p.color || '#312E81'};
            font-size: ${p.fontSize || '16px'};
            line-height: 1.8;
            margin-bottom: var(--space-md);
        `;
        return `<p style="${style}">${p.text || ''}</p>`;
    }).join('') : '<p>暂无内容</p>';
    
    content.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-xl);">
            <h2 style="font-family: 'Noto Serif SC', serif; font-size: 1.8rem; color: var(--color-primary);">
                ${article.title || '无标题'}
            </h2>
            <button onclick="this.closest('[style*=fixed]').remove()" 
                    style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748B;"
                    aria-label="关闭">
                ✕
            </button>
        </div>
        <div style="font-family: 'Noto Sans SC', sans-serif;">
            ${paragraphsHtml}
        </div>
    `;
    
    modal.appendChild(content);
    document.body.appendChild(modal);
    
    // 点击背景关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // ESC 键关闭
    const closeOnEsc = (e) => {
        if (e.key === 'Escape') {
            modal.remove();
            document.removeEventListener('keydown', closeOnEsc);
        }
    };
    document.addEventListener('keydown', closeOnEsc);
}

// 导出全局函数
window.switchSection = switchSection;
window.showArticle = showArticle;
