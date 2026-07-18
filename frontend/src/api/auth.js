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
    api.get("/users/profile");

export const updateProfile = (data) =>
    api.put("/users/profile", data);

export const uploadAvatar = (file) => {

    const formData = new FormData();

    formData.append("file", file);

    return api.patch(
        "/users/profile/avatar",
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data",
            },
        }
    );

};

export const deleteAvatar = () =>
    api.delete("/users/profile/avatar");