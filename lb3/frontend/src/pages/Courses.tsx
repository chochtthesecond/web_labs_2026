import React, { useState, useEffect } from 'react';
import { courseService } from '../services/courseService';
import { Course, CourseWithEnrolled } from '../types/auth';
import styles from '../styles/courses.module.css';

const Courses: React.FC = () => {
  const [allCourses, setAllCourses] = useState<Course[]>([]);
  const [myCourseIds, setMyCourseIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  //загружаем все курсы и посещаемые курсы
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [courses, myCourses] = await Promise.all([
          courseService.getAll(),
          courseService.getMyCourses(),
        ]);
        setAllCourses(courses);
        setMyCourseIds(new Set(myCourses.map(c => c.id)));
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Ошибка загрузки курсов');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleEnroll = async (courseId: number) => {
    setActionLoading(courseId);
    try {
      await courseService.enroll(courseId);
      setMyCourseIds(prev => new Set(prev).add(courseId));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Не удалось записаться на курс');
    } finally {
      setActionLoading(null);
    }
  };

  const handleWithdraw = async (courseId: number) => {
    setActionLoading(courseId);
    try {
      await courseService.withdraw(courseId);
      setMyCourseIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(courseId);
        return newSet;
      });
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Не удалось отписаться от курса');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) return <div>Загрузка курсов...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles['courses-container']}>
      <div className={styles['courses-list']}>
	  <h1>Все курсы</h1>
      {allCourses.length === 0 && <p>Нет доступных курсов.</p>}
        {allCourses.map(course => {
          const isEnrolled = myCourseIds.has(course.id);
          return (
            <div key={course.id} className={styles['course-card']}>
              <h2>{course.title}</h2>
              <p>{course.description || 'Описание отсутствует'}</p>
              <p><strong>Преподаватель:</strong> {course.teacher || 'Не указан'}</p>
              <button
                onClick={() => isEnrolled ? handleWithdraw(course.id) : handleEnroll(course.id)}
                disabled={actionLoading === course.id}
                className={styles.btn}
              >
                {actionLoading === course.id
                  ? 'Обработка...'
                  : isEnrolled
                  ? 'Отписаться'
                  : 'Записаться'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Courses;