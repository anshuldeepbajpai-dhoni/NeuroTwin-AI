import api from "./api";

export const getDigitalTwin = () =>
    api.get("/digital-twin/");

export const createDigitalTwin = (data) =>
    api.post("/digital-twin/", data);

export const updateDigitalTwin = (data) =>
    api.put("/digital-twin/", data);

export const deleteDigitalTwin = () =>
    api.delete("/digital-twin/");