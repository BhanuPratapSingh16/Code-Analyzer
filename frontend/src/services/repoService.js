import api from "./api";


export const createRepo = async () => {
    const response = await api.post("/repos/create")
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