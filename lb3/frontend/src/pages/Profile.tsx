import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { studentService } from '../services/studentService';
import { User } from '../types/auth';
import styles from '../styles/profile.module.css';

const Profile: React.FC = () => {
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState<User | null>(null);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  //получаем данные студента
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await studentService.getProfile();
        setProfile(data);
        setName(data.name);
        setPhone(data.phone || '');
      } catch (err: any) {
        setMessage({ type: 'error', text: err.response?.data?.detail || 'Не удалось загрузить профиль' });
      } finally {
        setFetching(false);
      }
    };
    loadProfile();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    try {
      const updated = await studentService.updateProfile({ name, phone: phone || undefined });
      setProfile(updated);
      setMessage({ type: 'success', text: 'Профиль успешно обновлён' });
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Ошибка обновления' });
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return <div className={styles.wrap}>Загрузка...</div>;
  }

  return (
    <div className={styles.wrap}>
      <form onSubmit={handleSubmit} className={styles.form}>
		{message && (
        <div className={`${styles.message} ${message.type === 'success' ? styles.success : styles.error}`}>
          {message.text}
        </div>
		)}
        <h1 className={styles.title}>Профиль</h1>
        <div className={styles.field}>
          <label className={styles.label}>Email:</label>
          <input
			type="email"
			value={user?.email || ''}
			disabled
			className={styles.input} />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className={styles.input}
          />
        </div>
        <div className={styles.field}>
          <label className={styles.label}>Phone:</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            className={styles.input}
          />
        </div>
        <div className={styles.buttons}>
          <button type="submit" disabled={loading} className={styles.button}>
            {loading ? 'Сохранение...' : 'Сохранить'}
          </button>
          <button type="button" onClick={logout} className={styles.button}>
            Выход
          </button>
        </div>
      </form>
    </div>
  );
};

export default Profile;