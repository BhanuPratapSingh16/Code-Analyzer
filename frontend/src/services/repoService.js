import api from "./api";


export const createRepo = async (data) => {
    const response = await api.post("/repos/create", data)
    return response.data;
}

export const getRepos = async () => {
    const response = await api.get("/repos/");
    return response.data;
}

export const getRepoById = async (id) => {
    const response = await api.get(`/repos/${id}`)
    return response.data;
}