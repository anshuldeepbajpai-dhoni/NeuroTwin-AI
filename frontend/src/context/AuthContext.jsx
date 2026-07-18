import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import authService from "../services/authService";

const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        initialize();
    }, []);

    async function initialize() {

        const token = localStorage.getItem("token");

        if (!token) {
            setLoading(false);
            return;
        }

        try {

            const profile = await authService.profile();

            setUser(profile);

        } catch {

            localStorage.removeItem("token");

            setUser(null);

        } finally {

            setLoading(false);

        }
    }

    async function login(data) {

        console.log("Login Data:", data);

        const response = await authService.login(data);

        console.log("Login Response:", response);

        localStorage.setItem(
            "token",
            response.access_token
        );

        console.log(
            "Stored Token:",
            localStorage.getItem("token")
        );

        const profile = await authService.profile();

        console.log("Profile:", profile);

        setUser(profile);
    }

    async function register(data) {

        return await authService.register(data);

    }

    async function refreshUser() {

        try {

            const profile = await authService.profile();

            setUser(profile);

        } catch (error) {

            console.error(error);

        }

    }


    function logout() {

        localStorage.removeItem("token");

        setUser(null);

    }

    return (

        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                register,
                refreshUser,
                logout,
                isAuthenticated: !!user,
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}

export function useAuth() {
    return useContext(AuthContext);
}