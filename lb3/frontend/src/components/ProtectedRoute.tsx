import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface Props {
  children: JSX.Element;
}

export const ProtectedRoute = ({ children }: Props) => {
  const { user, loading } = useAuth();
  if (loading) return <div>Загрузка...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
};