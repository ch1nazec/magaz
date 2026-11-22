import axios from "axios";
import { useAuthStore } from "@/stores/auth";


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const API_BASE_URL = 'http://127.0.0.1:8010/api/'


const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};


api.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore()

        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`}
        return config},
    (error) => {
        return Promise.reject(error)})

api.interceptors.response.use(
    (response) => { return response; },

    async (error) => {
        const originalRequest = error.config;
        const authStore = useAuthStore();

        console.log('Request error API: ', {
            url: originalRequest?.url,
            status: error.response?.status,
            message: error.message
        });
        
        if ((error.response?.status === 401 || error.response?.status === 403) && !originalRequest._retry) {
            
            // Если токен уже обновляется другим запросом, ставим текущий запрос в очередь
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                })
                .then(token => {
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                    return api(originalRequest);
                })
                .catch(err => {
                    return Promise.reject(err);
                });
            }

            originalRequest._retry = true;
            isRefreshing = true;

            if (authStore.refreshToken) {
                try {
                    const refreshed = await authStore.refreshAccessToken();

                    if (refreshed) {
                        // Передаем новый токен всем ожидающим запросам в очереди
                        processQueue(null, authStore.token); 
                        
                        originalRequest.headers.Authorization = `Bearer ${authStore.token}`;
                        return api(originalRequest);
                    }
                } catch (refreshError) {
                    processQueue(refreshError, null);
                    // Если обновление токена упало с ошибкой, принудительно разлогиниваем
                } finally {
                    isRefreshing = false;
                }
            }

            // Логика выхода, если нет рефреш-токена или метод обновления вернул false/упал
            authStore.logout();
            isRefreshing = false; // Сбрасываем флаг

            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);
export default api