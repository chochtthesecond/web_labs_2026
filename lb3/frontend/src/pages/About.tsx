import React from 'react';
import styles from '../styles/style_about.module.css';

const About: React.FC = () => {
  return (
    <>
      <section className={styles.school}>
        <div className={styles.deepblue}></div>
        <div className={styles.container}>
          <img src="/img/about1.jpg" alt="woman with guitar doing studies" />
          <div className={styles['music-school']}>
            <h2>Музыкальная школа</h2>
            <p>
              Школа объединяет в себе около тысячи юных музыкантов, художников, танцоров,
              а десятки опытных, ищущих новые пути педагогов, дают им возможность раскрыть
              свои таланты, постичь тайны искусств и мастерства.
            </p>
          </div>
        </div>
        <div className={styles.lightblue}></div>
      </section>

      <section className={styles.pedagogy}>
        <div className={styles.title}>
          <h2>Музыкальная психология и педагогия</h2>
        </div>
        <div className={styles.info}>
          <img src="/img/about2.jpg" alt="teacher portrait" />
          <p>Высоко оцененная программа</p>
          <p>
            В наших программах обучения подчеркиваются пять основных принципов,
            призванных подготовить студентов к успешной карьере в области музыки:
          </p>
          <ul>
            <li>Гибкость</li>
            <li>Новаторство</li>
            <li>Пытливость</li>
            <li>Лидерство</li>
            <li>Равенство во всех отношениях</li>
          </ul>
        </div>
      </section>
    </>
  );
};

export default About;