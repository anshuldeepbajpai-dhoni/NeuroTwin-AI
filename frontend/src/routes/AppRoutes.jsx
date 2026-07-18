import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

import Dashboard from "../pages/dashboard/Dashboard";
import Profile from "../pages/profile/Profile";
import DigitalTwin from "../pages/twin/DigitalTwin";
import Memory from "../pages/memory/Memory";
import Chat from "../pages/chat/Chat";

import AppLayout from "../components/layout/AppLayout";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <AppLayout>
                                <Dashboard />
                            </AppLayout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/profile"
                    element={
                        <ProtectedRoute>
                            <AppLayout>
                                <Profile />
                            </AppLayout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/digital-twin"
                    element={
                        <ProtectedRoute>
                            <AppLayout>
                                <DigitalTwin />
                            </AppLayout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/memory"
                    element={
                        <ProtectedRoute>
                            <AppLayout>
                                <Memory />
                            </AppLayout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/chat"
                    element={
                        <ProtectedRoute>
                            <AppLayout>
                                <Chat />
                            </AppLayout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />

            </Routes>

        </BrowserRouter>

    );

}