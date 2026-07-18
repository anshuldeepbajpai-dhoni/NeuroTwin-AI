import {
    getDigitalTwin,
    createDigitalTwin,
    updateDigitalTwin,
    deleteDigitalTwin,
} from "../api/digitalTwin";

const digitalTwinService = {

    get: async () => {

        const response = await getDigitalTwin();

        return response.data;

    },

    create: async (data) => {

        const response = await createDigitalTwin(data);

        return response.data;

    },

    update: async (data) => {

        const response = await updateDigitalTwin(data);

        return response.data;

    },

    remove: async () => {

        const response = await deleteDigitalTwin();

        return response.data;

    },

};

export default digitalTwinService;