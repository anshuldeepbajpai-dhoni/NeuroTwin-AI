import {
    getMemories,
    getMemory,
    createMemory,
    updateMemory,
    deleteMemory,
} from "../api/memory";

const memoryService = {

    getAll: async () => {

        const response = await getMemories();

        return response.data;

    },

    getById: async (id) => {

        const response = await getMemory(id);

        return response.data;

    },

    create: async (data) => {

        const response = await createMemory(data);

        return response.data;

    },

    update: async (id, data) => {

        const response = await updateMemory(id, data);

        return response.data;

    },

    remove: async (id) => {

        await deleteMemory(id);

    },

};

export default memoryService;