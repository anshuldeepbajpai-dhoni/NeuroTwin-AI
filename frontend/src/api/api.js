import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 30000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {

        const token = localStorage.getItem("token");

        console.log("REQUEST:", config.url);
        console.log("TOKEN:", token);

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            console.log("AUTH HEADER:", config.headers.Authorization);
        }

        return config;

    }
);

api.interceptors.response.use(
    (response) => response,

    (error) => {

        if (error.response?.status === 401) {

            localStorage.removeItem("token");

            window.location.href = "/login";
        }

        return Promise.reject(error);

    }
);

export default api;