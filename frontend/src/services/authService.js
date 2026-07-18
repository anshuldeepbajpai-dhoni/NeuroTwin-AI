import {
    loginUser,
    registerUser,
    getProfile,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
} from "../api/auth";

const authService = {

    login: async (credentials) => {

        const response =
            await loginUser(credentials);

        return response.data;

    },

    register: async (data) => {

        const response =
            await registerUser(data);

        return response.data;

    },

    profile: async () => {

        const response =
            await getProfile();

        return response.data;

    },

    updateProfile: async (data) => {

    const response =
        await updateProfile(data);

    return response.data;

    },

    uploadAvatar: async (file) => {

        const response =
            await uploadAvatar(file);

        return response.data;

    },

    deleteAvatar: async () => {

        const response =
            await deleteAvatar();

        return response.data;

    },

};

export default authService;