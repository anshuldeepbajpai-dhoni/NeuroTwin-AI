import api from "./api";

export const createTwin = (data) =>
    api.post("/digital-twin/", data);

export const getTwin = () =>
    api.get("/digital-twin/");

export const updateTwin = (data) =>
    api.put("/digital-twin/", data);

export const deleteTwin = () =>
    api.delete("/digital-twin/");