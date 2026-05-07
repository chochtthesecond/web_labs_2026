import React, { useState } from 'react';
import styles from '../styles/style_contact.module.css';

const Contact: React.FC = () => {
  return (
    <>
      <section className={styles.contact}>
        <form className={styles.form}>
          <h1>Связаться с нами</h1>
          <div>
            <input type="text" placeholder="Введите имя" required />
          </div>
          <div>
            <input type="email" placeholder="Введите адрес электронной почты" required />
          </div>
          <div>
            <textarea placeholder="Введите сообщение" rows={4} cols={50} required></textarea>
          </div>
          <button type="submit" className={styles.submit}>Отправить</button>
        </form>
        <img src="/img/contact.jpg" alt="man pointing at form" />
      </section>

      <section className={styles.info}>
        <div>
          <h2>Позвоните нам</h2>
          <p>1 (234) 567-891, 1 (234) 987-654</p>
        </div>
        <div>
          <h2>Расположение</h2>
          <p>г. Москва, ул. Пушкина, д. 1А</p>
        </div>
        <div>
          <h2>Часы работы</h2>
          <p>Пн – Пт 10:00 – 20:00</p>
        </div>
      </section>
    </>
  );
};

export default Contact;