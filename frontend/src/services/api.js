import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercepteur pour inclure le token JWT automatiquement
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour rafraîchir le token si expiré
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) throw new Error("No refresh token found");

        const response = await axios.post(`${API_BASE_URL}/authentication/token/refresh/`, {
          refresh: refreshToken,
        });

        localStorage.setItem("access_token", response.data.access);
        originalRequest.headers["Authorization"] = `Bearer ${response.data.access}`;
        return axios(originalRequest);
      } catch (refreshError) {
        console.error("Session expirée, veuillez vous reconnecter.");
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
