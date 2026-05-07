import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from '../styles/nav.module.css';

const Navbar: React.FC = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [isDark, setIsDark] = useState(() => {
    return localStorage.getItem('theme') === 'dark';
  });
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.body.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  const handleLogout = () => {
    logout();
    navigate('/');
    setMenuOpen(false);
  };

  const toggleTheme = () => setIsDark(!isDark);
  const toggleMenu = () => setMenuOpen(!menuOpen);

  return (
    <header>
      <nav>
        <div className={styles['menu-container']}>
          <button id="theme-button" onClick={toggleTheme} className={styles['theme-btn']}>
            <img src={isDark ? '../../img/sun-icon.png' : '../../img/moon-icon.png'} alt='turn on dark theme'></img>
          </button>
          <button className={styles['menu-button']} onClick={toggleMenu}>
		  ☰
		  </button>
          <div className={`${styles.menu} ${menuOpen ? styles.open : ''}`} id="menu">
            <Link to="/" onClick={() => setMenuOpen(false)}>Главная</Link>
            <Link to="/about" onClick={() => setMenuOpen(false)}>О нас</Link>
            <Link to="/contact" onClick={() => setMenuOpen(false)}>Контакты</Link>

            {!user ? (
              <>
                <Link to="/register" onClick={() => setMenuOpen(false)}>Регистрация</Link>
                <Link to="/login" onClick={() => setMenuOpen(false)}>Вход</Link>
              </>
            ) : (
              <>
                <Link to="/profile" onClick={() => setMenuOpen(false)}>Профиль</Link>
                {!isAdmin && (
					<>
					  <Link to="/courses" onClick={() => setMenuOpen(false)}>Все курсы</Link>
					  <Link to="/my-courses" onClick={() => setMenuOpen(false)}>Мои курсы</Link>
					</>
				)}
                {isAdmin && (
                  <>
                    <Link to="/admin/students" onClick={() => setMenuOpen(false)}>Студенты (админ)</Link>
                    <Link to="/admin/courses" onClick={() => setMenuOpen(false)}>Курсы (админ)</Link>
                  </>
                )}
                <button onClick={handleLogout} className={styles['logout-btn']}>Выйти</button>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;