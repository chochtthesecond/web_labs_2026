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
    let button = document.getElementById('theme-button');
	const img = button.querySelector('img');
    if (img.src.includes('moon-icon.png')) {
        document.documentElement.classList.add('dark-mode');
        img.src = 'img/sun-icon.png';
        img.alt = 'turn on light theme'; //тёмная тема
    } else {
        document.documentElement.classList.remove('dark-mode');
        img.src = 'img/moon-icon.png';
        img.alt = 'turn on dark theme'; //светлая тема
    }
}