document.addEventListener('DOMContentLoaded', () => {
    //кнопка темы
    const themeBtn = document.getElementById('theme-button');
    themeBtn.addEventListener('click', setTheme);

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

//функция установки темы
function setTheme() {
    let theme = document.getElementById('theme-button');
    if (theme.textContent === '☀️') {
        document.documentElement.classList.add('dark-mode');
        theme.textContent = '🌙'; //тёмная тема
    } else {
        document.documentElement.classList.remove('dark-mode');
        theme.textContent = '☀️'; //светлая тема
    }
}