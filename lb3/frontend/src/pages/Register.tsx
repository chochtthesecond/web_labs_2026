import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from '../styles/reg.module.css'

export const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(email, password, name, phone || undefined);
      navigate('/profile');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  return (
  <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
	  {error && <div className={styles.error}>{error}</div>}
	  <h2 className={styles.title}>Регистрация</h2>
        <div className={styles.field}>
          <label className={styles.label}>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
			className={styles.input}
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Пароль:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
			className={styles.input}
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>ФИО:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
			className={styles.input}
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Телефон:</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
			className={styles.input}
          />
        </div>
        <button type="submit" className={styles.submit}>Зарегистрироваться</button>
		<p className={styles.linkWrapper}>
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
      </form>
	</div>
  );
};