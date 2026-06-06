import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getHealth = () => api.get("/health");

export const getInstitutions = () => api.get("/institutions");

export const getInstitution = (name) =>
  api.get(`/institutions/${encodeURIComponent(name)}`);

export const runPipeline = () => api.post("/run-pipeline");

export const getReport = (name) =>
  api.get(`/reports/${encodeURIComponent(name)}`);

export default api;
