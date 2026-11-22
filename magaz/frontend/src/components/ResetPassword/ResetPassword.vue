<template>
    <div class="d-flex justify-content-center pt-5 vh-90">
        <form class="forget-password" @submit.prevent="resetPassword">
            <BaseInput
            v-model="forgetData.otp_code"
            type="text"
            label="Код из почты"
            >
            </BaseInput>
            <BaseInput
            v-model="forgetData.new_password"
            type="password"
            label="Новый пароль"
            >
            </BaseInput>
            <BaseInput
            v-model="forgetData.confirm_password"
            type="password"
            label="Подтверждение пароля"
            >
            </BaseInput>

            <BaseButton type="submit" class="bg-black text-white hover:bg-gray-800 focus:ring-black">Сбросить</BaseButton>
        </form>
    </div>
</template>

<script setup>
import BaseInput from '../common/BaseInput.vue';
import BaseButton from '../common/BaseButton.vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';


import { useAuthStore } from '@/stores/auth.js';
import api from '@/services/api.js';
import { ref } from 'vue';

const router = useRouter()

const authStore = useAuthStore()
const { email } = storeToRefs(authStore)

const isLoading = ref(false)

const forgetData = ref({
    otp_code: '',
    new_password: '',
    confirm_password: '',
})

const resetPassword = async () => {
    try {
        if (isLoading.value) return

        const payload = {
            email: email.value.email,
            ...forgetData.value
        }
        console.log(payload)

        isLoading.value = true
        console.log(forgetData.value)
        const response = await api.post('users/reset-password/', payload)
        authStore.clearEmail()

        router.push('/login')
    } catch (error) {
        console.error(error)
    }
    finally {
        isLoading.value = false
    }
}
</script>

<style>

</style>