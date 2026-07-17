import {
    Navigate,
    Outlet,
} from "react-router-dom";

import {
    useAuth,
} from "../context/AuthContext";

export default function ProtectedRoute() {

    const {
        loading,
        isAuthenticated,
    } = useAuth();

    if (loading) {
        return <h2>Loading...</h2>;
    }

    return isAuthenticated
        ? <Outlet />
        : <Navigate to="/login" replace />;
}