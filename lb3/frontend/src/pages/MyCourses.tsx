import React, { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';
import { MyCourse } from '../types/auth';
import styles from '../styles/courses.module.css';

const MyCourses: React.FC = () => {
  const [courses, setCourses] = useState<MyCourse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [withdrawLoading, setWithdrawLoading] = useState<number | null>(null);

  const fetchMyCourses = async () => {
    try {
      const data = await courseService.getMyCourses();
      setCourses(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки ваших курсов');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMyCourses();
  }, []);

  const handleWithdraw = async (courseId: number) => {
    setWithdrawLoading(courseId);
    try {
      await courseService.withdraw(courseId);
      //обновляем список после отписки
      setCourses(prev => prev.filter(c => c.id !== courseId));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Не удалось отписаться от курса');
    } finally {
      setWithdrawLoading(null);
    }
  };

  if (loading) return <div>Загрузка ваших курсов...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles['my-courses-container']}>
      <div className={styles['courses-list']}>
	  <h1>Мои курсы</h1>
      {courses.length === 0 && <p>Вы ещё не записаны ни на один курс.</p>}
        {courses.map(course => (
          <div key={course.id} className={styles['course-card']}>
            <h2>{course.title}</h2>
            <p>{course.description || 'Описание отсутствует'}</p>
            <p><strong>Преподаватель:</strong> {course.teacher || 'Не указан'}</p>
            <p><small>Дата записи: {new Date(course.enrolled_at).toLocaleDateString()}</small></p>
            <button
              onClick={() => handleWithdraw(course.id)}
              disabled={withdrawLoading === course.id}
              className={styles.btn}
            >
              {withdrawLoading === course.id ? 'Отписка...' : 'Отписаться'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyCourses;