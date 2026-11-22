<template>
    <div class="d-flex justify-content-center pt-5 vh-90">
        <form class="forget-password" @submit.prevent="resetPassword">
            <BaseInput
            v-model="forgetPasswordData.email"
            type="email"
            label="Email Address"
            >
            </BaseInput>

            <BaseButton type="submit" class="bg-black text-white hover:bg-gray-800 focus:ring-black">Сброс пароля</BaseButton>
        </form>
    </div>
</template>

<script setup>
import BaseInput from '../common/BaseInput.vue';
import BaseButton from '../common/BaseButton.vue';
import { useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/auth.js';
import api from '@/services/api.js';
import { ref } from 'vue';


const router = useRouter()

const forgetPasswordData = ref({email: '',})
const authStore = useAuthStore()
const isLoading = ref(false)

const resetPassword = async () => {
    try {
        if (isLoading.value) return

        isLoading.value = true
        const response = await api.post('users/forget-password/', forgetPasswordData.value)
        authStore.setEmail(forgetPasswordData.value)

        router.push('/reset-password')
    } catch (error) {
        console.error(error)
        authStore.clearEmail()
    }
    finally {
        isLoading.value = false
    }
}
</script>

<style>

</style>