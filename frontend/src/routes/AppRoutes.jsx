import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

import Dashboard from "../pages/dashboard/Dashboard";
import DigitalTwin from "../pages/twin/DigitalTwin";
import Chat from "../pages/chat/Chat";
import Memory from "../pages/memory/Memory";
import Profile from "../pages/profile/Profile";

import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {
    return (
        <BrowserRouter>

            <Routes>

                {/* Public Routes */}

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                {/* Protected Routes */}

                <Route
                    element={<ProtectedRoute />}
                >

                    <Route
                        path="/"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/digital-twin"
                        element={<DigitalTwin />}
                    />

                    <Route
                        path="/chat"
                        element={<Chat />}
                    />

                    <Route
                        path="/memory"
                        element={<Memory />}
                    />

                    <Route
                        path="/profile"
                        element={<Profile />}
                    />

                </Route>

            </Routes>

        </BrowserRouter>
    );
}