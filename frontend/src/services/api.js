import axios from "axios";
import { useAuthStore } from "@/stores/auth";


const API_BASE_URL = 'http://localhost:8000/api/'


const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore()

        if (authStore.token) {
            config.headers.Authorization = `Bearer ${authStore.token}`}
        
        console.log('API Request:', {
            url: config.url,
            method: config.method,
            headers: config.headers,
            hasToken: !!authStore.token
            })
        return config},
    (error) => {
        return Promise.reject(error)})

api.interceptors.response.use(
    (response) => {return response},

    async (error) => {
        const originalRequest = error.config
        const authStore = useAuthStore()

        console.log('Request error API: ', {
            url: originalRequest?.url,
            status: error.response?.status,
            message: error.message})
        
        if ((error.response?.status === 401 || error.response?.status === 403) && !originalRequest._retry) {
            originalRequest._retry = true

            if (authStore.refreshToken) {
                const refreshed = await authStore.refreshAccessToken()

                if (refreshed) {
                    originalRequest.headers.Authorization = `Bearer ${authStore.token}`
                    return api(originalRequest)
                }
            }

            authStore.logout()

            if (window.location.pathname ==! '/login') {
                window.location.href = '/login'}
        }

        return Promise.reject(error)
    }
)
export default api