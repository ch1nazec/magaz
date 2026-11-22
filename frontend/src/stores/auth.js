import { defineStore } from "pinia";
import { ref, computed } from "vue";
import authService from "@/services/auth";


export const useAuthStore = defineStore('auth', () => {

    const user = ref(null)
    const token = ref(localStorage.getItem('access_token') || sessionStorage.getItem('access_token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || sessionStorage.getItem('refresh_token') || null)
    const loading = ref(false)

    const email = ref(localStorage.getItem('reset_email') || '')

    const isAuthenticated = computed(() => !!token.value)
    const userName = computed(() => {
        if (!user.value) return ''
        return `${user.value.first_name} ${user.value.last_name}`})


    function setEmail (newEmail)  {
        email.value = newEmail
        localStorage.setItem('reset_email', newEmail)
    }
    function clearEmail() {
        email.value = ''
        localStorage.removeItem('reset_email')
    }

    async function login(credentials) {
        try {

            loading.value = true

            const response = await authService.login(credentials)
            if (response.data) {
                token.value = response.data.access
                refreshToken.value = response.data.refresh
                user.value = response.data.user

                console.log('Сохранение токена в storage:', { remember: credentials.remember, token: response.data.access })

                if (credentials.remember) {
                    localStorage.setItem('access_token', response.data.access)
                    localStorage.setItem('refresh_token', response.data.refresh)}
                else {
                    sessionStorage.setItem('access_token', response.data.access)
                    sessionStorage.setItem('refresh_token', response.data.refresh)}
                
                console.log('Загрузка токена из storage:', localStorage.getItem('access_token'))
                
                console.log('Login successfull! token: ', token.value)
                return { success: true }}
            return { success: false, error: 'Invalid response from server' }
        } catch (error) {
            console.log('Error to login: ', error)
            return { success: false, error: 'Invalid response from server'}}
        finally {loading.value = false}
    }

    async function updateProfileData(profileData) {
        try {
            loading.value = true

            const response = await authService.updateProfile(profileData)
            user.value = response.data
            
            return response.data
        } catch (error) {
            throw error}
        finally { loading.value = true }
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
        localStorage.removeItem('refresh_token')
        sessionStorage.removeItem('access_token')
        sessionStorage.removeItem('refresh_token')}


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
            if (response.data?.actions) {
                token.value = response.data.access

                if (localStorage.getItem('access_token')) {
                    localStorage.setItem('access_token', response.data.access)}
                else {
                    sessionStorage.setItem('access_token', response.data.access)}
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
    email,

    // Getters
    isAuthenticated,
    userName,

    // Actions
    login,
    register,
    logout,
    fetchProfile,
    refreshAccessToken,
    updateProfileData,
    initialize,
    setEmail,
    clearEmail
  }
})