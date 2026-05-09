import { defineStore } from "pinia";
import { ref, computed } from "vue";
import authService from "@/services/auth";


export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const token = ref(localStorage.getItem('access_token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)
    const loading = ref(false)

    const isAuthenticated = computed(() => !!token.value)
    const userName = computed(() => {
        if (!user.value) return ''
        return `${user.value.first_name} ${user.value.last_name}`})

    async function login(credentials) {
        try {

            loading.value = true

            const response = await authService.login(credentials)
            if (response.data) {
                token.value = response.data.access
                refreshToken.value = response.data.refresh
                user.value = response.data.user

                localStorage.setItem('access_token', response.data.access)
                localStorage.setItem('refresh_token', response.data.refresh)
                
                console.log('Login successfull! token: ', token.value)
                return { success: true }}
            return { success: false, error: 'Invalid response from server' }
        } catch (error) {
            console.log('Error to login: ', error)
            return { success: false, error: 'Invalid response from server'}}
        finally {loading.value = false}
    }

    async function register(credentials) {
        try {
            loading.value = true

            const response = await authService.register(credentials)
            if (response.data) {
                return { success: true, message: 'Registration successful' }}

        } catch (error) {console.log('Error to register: ', error)}
        finally {loading.value = false}
    }

    async function logout() {
        user.value = null
        token.value = null
        refreshToken.value = null

        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')}

    async function fetchProfile() {
        try {
            if (!token.value) {console.log('No token available  for profile fetch'); return}

            const response = await authService.getProfile()
            if (response.data) {
                user.value = response.data}
        } catch (error) {
            console.log('Fetch profile error: ', error)

            if (error.response?.status === 401 || error.response?.status === 403) {
                console.log('Profile fetch failed with auth error, logout out')
                await logout()
            }
        }
    }

    async function refreshAccessToken() {
        try {
            if (!refreshToken.value) {
                console.log('No refresh token')
                return false}
            
            console.log('Refreshing access token...')

            const response = await authService.refreshToken(refreshToken.value)
            if (response.data?.access) {
                token.value = response.data.access
                localStorage.setItem('access_token', response.data.access)
                console.log('Token refreshed successfully')
                return true
            }
        } catch (error) {
            console.error('Token refresh error:', error)
            await logout()
        }
        return false}

    async function initialize() {
        console.log('Initializing auth store...')
        console.log('Has stored token', !!token.value)

        if (token.value) { await fetchProfile() }
    }
    return {
    // State
    user,
    token,
    refreshToken,
    loading,

    // Getters
    isAuthenticated,
    userName,

    // Actions
    login,
    register,
    logout,
    fetchProfile,
    refreshAccessToken,
    initialize
  }
})