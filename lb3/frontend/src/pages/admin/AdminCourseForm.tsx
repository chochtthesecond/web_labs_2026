import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { adminService } from '../../services/adminService';
import { CourseCreate, CourseUpdate, Student } from '../../types/admin';
import { api } from '../../services/api';
import styles from '../../styles/course_form.module.css';

const AdminCourseForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = !!id;

  const [formData, setFormData] = useState<CourseCreate | CourseUpdate>({
    title: '',
    description: '',
    teacher: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  //состояния для управления студентами
  const [enrolledStudents, setEnrolledStudents] = useState<Student[]>([]);
  const [allStudents, setAllStudents] = useState<Student[]>([]);
  const [enrollmentLoading, setEnrollmentLoading] = useState(false);
  const [enrollmentError, setEnrollmentError] = useState<string | null>(null);
  const [selectedStudentId, setSelectedStudentId] = useState<string>('');

  //загрузка данных курса
  useEffect(() => {
    if (isEditing) {
      const loadCourse = async () => {
        try {
          const course = await adminService.getCourse(Number(id));
          setFormData({
            title: course.title,
            description: course.description || '',
            teacher: course.teacher || '',
          });
        } catch (err: any) {
          setError(err.message);
        }
      };
      loadCourse();
    }
  }, [id, isEditing]);

  //загрузка студентов
  useEffect(() => {
    if (isEditing && id) {
      loadEnrolledStudents();
      loadAllStudents();
    }
  }, [id, isEditing]);

  const loadEnrolledStudents = async () => {
    if (!id) return;
    setEnrollmentLoading(true);
    setEnrollmentError(null);
    try {
      const response = await api.get(`/admin/courses/${id}/students`);
      setEnrolledStudents(response.data);
    } catch (err: any) {
      console.error('Failed to load enrolled students:', err);
      setEnrollmentError('Не удалось загрузить список студентов курса');
    } finally {
      setEnrollmentLoading(false);
    }
  };

  const loadAllStudents = async () => {
    try {
      const students = await adminService.getStudents();
      setAllStudents(students);
    } catch (err: any) {
      console.error('Failed to load all students:', err);
      setEnrollmentError('Не удалось загрузить список всех студентов');
    }
  };

  //находим незачисленных на курс студентов
  const availableStudents = allStudents.filter(
    student => !enrolledStudents.some(enrolled => enrolled.id === student.id)
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEditing) {
        await adminService.updateCourse(Number(id), formData as CourseUpdate);
      } else {
        await adminService.createCourse(formData as CourseCreate);
      }
      navigate('/admin/courses');
    } catch (err: any) {
      alert('Ошибка сохранения: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStudent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudentId || !id) return;

    try {
      await adminService.enrollStudent(Number(selectedStudentId), Number(id));
      //обновляем списки после зачисления
      await loadEnrolledStudents();
      setSelectedStudentId('');
      //обновляем все списки чтобы убрать добавленного студента из доступных
      await loadAllStudents();
    } catch (err: any) {
      alert('Ошибка при зачислении студента: ' + err.message);
    }
  };

  const handleRemoveStudent = async (studentId: number) => {
    if (!id) return;
    
    const confirmed = window.confirm('Вы уверены, что хотите отчислить этого студента из курса?');
    if (!confirmed) return;

    try {
      await adminService.unenrollStudent(studentId, Number(id));
      //обновляем списки после отчисления
      await loadEnrolledStudents();
      await loadAllStudents();
    } catch (err: any) {
      alert('Ошибка при отчислении студента: ' + err.message);
    }
  };

  return (
    <section className={styles['course-form']}>
      <h1>{isEditing ? 'Редактировать курс' : 'Добавить курс'}</h1>

      {error && <div className={styles.error}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Название курса:</label>
          <input
            type="text"
            name="title"
            value={formData.title || ''}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Описание:</label>
          <textarea
            name="description"
            rows={4}
            value={formData.description || ''}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Учитель:</label>
          <input
            type="text"
            name="teacher"
            value={formData.teacher || ''}
            onChange={handleChange}
          />
        </div>

        <div>
          <button type="submit" disabled={loading}>
            {loading ? 'Сохранение...' : 'Сохранить'}
          </button>
          <Link to="/admin/courses">Отмена</Link>
        </div>
      </form>

      {/*управление студентами*/}
      {isEditing && (
        <>
          <hr />
          <section className={styles['course-enrollment']}>
            <h2>Управление студентами курса "{formData.title}"</h2>

            <h3>Записанные студенты</h3>
            {enrollmentLoading ? (
              <p>Загрузка списка студентов...</p>
            ) : enrollmentError ? (
              <p className={styles.error}>{enrollmentError}</p>
            ) : enrolledStudents.length > 0 ? (
              <table className={styles['student-table']} border={1} cellPadding={6}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Email</th>
                    <th>Действие</th>
                  </tr>
                </thead>
                <tbody>
                  {enrolledStudents.map(student => (
                    <tr key={student.id}>
                      <td>{student.id}</td>
                      <td>{student.name}</td>
                      <td>{student.email}</td>
                      <td>
                        <button
                          type="button"
                          onClick={() => handleRemoveStudent(student.id)}
                          className={styles['remove-btn']}
                        >
                          Отчислить
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>На данный курс не записан ни один студент.</p>
            )}

            <h3>Добавить студента</h3>
            {availableStudents.length > 0 ? (
              <form onSubmit={handleAddStudent} className={styles['add-student-form']}>
                <select
                  value={selectedStudentId}
                  onChange={(e) => setSelectedStudentId(e.target.value)}
                  required
                >
                  <option value="">-- Выберите студента --</option>
                  {availableStudents.map(student => (
                    <option key={student.id} value={student.id}>
                      {student.name} ({student.email})
                    </option>
                  ))}
                </select>
                <button type="submit">Записать студента</button>
              </form>
            ) : (
              <p>Нет доступных студентов для добавления.</p>
            )}
          </section>
        </>
      )}
    </section>
  );
};

export default AdminCourseForm;