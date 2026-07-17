import api from "./api";

export const getMemories = () =>
    api.get("/memories/");

export const createMemory = (data) =>
    api.post("/memories/", data);

export const updateMemory = (id, data) =>
    api.put(`/memories/${id}`, data);

export const deleteMemory = (id) =>
    api.delete(`/memories/${id}`);