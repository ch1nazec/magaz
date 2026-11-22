import api from "./api";


const authService = {
    async login(credentials) {
        return await api.post('users/login/', credentials)},
    async register(credentials) {
        return await api.post('users/register/', credentials)},
    async refreshToken(credentials) {
        return await api.post('token/refresh/', credentials)},
    async getProfile() {
        return await api.get('users/profile/')},
    async updateProfile(userData) {
        return await api.put('users/profile/update/', userData)},
    async logout() {return Promise.resolve()}}


export default authService