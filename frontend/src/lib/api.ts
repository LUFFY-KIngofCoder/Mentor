import axios from "axios";

// Create an Axios instance pointing to the FastAPI backend
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add an interceptor to inject the JWT token into every request
api.interceptors.request.use(
  (config) => {
    // Only access localStorage in the browser (not during server-side rendering)
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
