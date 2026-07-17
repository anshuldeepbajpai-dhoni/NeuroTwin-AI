import api from "./api";

export const registerUser = (data) =>
    api.post("/auth/register", data);

export const loginUser = (data) =>
    api.post(
        "/auth/login",
        new URLSearchParams(data),
        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },
        }
    );

export const getProfile = () =>
    api.get("/auth/me");

// Change this only if your backend has an update endpoint.
// Otherwise leave it commented until you implement one.

// export const updateProfile = (data) =>
//     api.put("/profile", data);