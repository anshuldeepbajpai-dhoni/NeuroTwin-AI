import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function ProtectedRoute({ children }) {
    const { token, loading } = useAuth();

    if (loading) {
        return (
            <div
                style={{
                    height: "100vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    fontSize: "18px",
                }}
            >
                Loading...
            </div>
        );
    }

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    return children;
}