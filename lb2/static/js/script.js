document.addEventListener('DOMContentLoaded', () => {
	//сохраненная тема
	const savedTheme = localStorage.getItem('theme');
	//применение темы во время загрузки страницы
    applyTheme(savedTheme);
	
    //кнопка темы
    const themeBtn = document.getElementById('theme-button');
    themeBtn.addEventListener('click', toggleTheme);

    //кнопка меню
    const menuBtn = document.getElementById('menu-button');
    menuBtn.addEventListener('click', toggleMenu);
});

//функция открытия меню
function toggleMenu() {
    let menu = document.getElementById('menu');
    if (menu.style.maxHeight) {
        menu.style.maxHeight = null; //закрыть
    } else {
        menu.style.maxHeight = menu.scrollHeight + "px"; //открыть
    }
}

//функция применения темы
function applyTheme(theme) {
    const button = document.getElementById('theme-button');
    const img = button.querySelector('img');
    
    if (theme === 'dark') {
        document.documentElement.classList.add('dark-mode');
        img.src = '/static/img/sun-icon.png';
        img.alt = 'turn on light theme'; //темная тема
    } else {
        document.documentElement.classList.remove('dark-mode');
        img.src = '/static/img/moon-icon.png';
        img.alt = 'turn on dark theme'; //светлая тема
    }
}

//функция переключения темы
function toggleTheme() {
    const isDarkMode = document.documentElement.classList.contains('dark-mode');
    
    if (isDarkMode) {
        localStorage.setItem('theme', 'light');
        applyTheme('light');
    } else {

        localStorage.setItem('theme', 'dark');
        applyTheme('dark');
    }
}