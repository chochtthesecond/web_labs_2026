import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/style.module.css';

const Home: React.FC = () => {
  return (
    <>
      <section id="main" className={styles.main}>
        <img src="/img/main1.png" alt="a man with headphones smiling" />
        <div>
          <p>MODERN & FUN</p>
          <h1>Онлайн-музыкальное образование</h1>
          <p>
            Хотите научиться играть или петь? Присоединяйтесь к нашему дружному сообществу
            и занимайтесь любимым делом, не выходя из дома. Раскроем талант вместе!
          </p>
          <Link to="/about" className={styles['read-more']}>Читать далее</Link>
        </div>
      </section>

      <section className={styles.features}>
        <article>
          <img src="/img/mainicon1.png" alt="note icon" />
          <h3>Музыкальная терапия</h3>
          <p>Музыка лечит. Наши бережные занятия под руководством опытных преподавателей помогут снять стресс и подарить радость творчества.</p>
        </article>
        <article>
          <img src="/img/mainicon2.png" alt="disk icon" />
          <h3>Наша миссия</h3>
          <p>Мы хотим сделать качественное музыкальное образование доступным для каждого. Научим каждого!</p>
        </article>
        <article>
          <img src="/img/mainicon3.png" alt="headphones icon" />
          <h3>Музыкальные лагеря</h3>
          <p>Лето с музыкой незабываемо! Вас ждут интенсивы с лучшими преподавателями и настоящая творческая атмосфера.</p>
        </article>
        <article>
          <img src="/img/mainicon4.png" alt="microphone icon" />
          <h3>Библиотека</h3>
          <p>Ноты, обучающие видео, лекции ждут вас в нашей библиотеке. Заглядывайте за вдохновением в любое время!</p>
        </article>
      </section>

      <section className={styles['what-we-do']}>
        <img src="/img/main2.png" alt="man pointing at viewer" />
        <div>
          <h2>Чем мы занимаемся</h2>
          <p>
            В нашей школе музыка становится частью жизни. Мы сочетаем современные методики обучения
            с заботой о внутреннем состоянии учеников. Помогаем развивать таланты, верить в себя
            и получать удовольствие от каждого аккорда.
          </p>
          <Link to="/contact" className={styles.contact}>Связаться с нами</Link>
        </div>
		<div className={styles.img2}></div>
      </section>
    </>
  );
};

export default Home;