import {
    loginUser,
    registerUser,
    getProfile,
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

};

export default authService;