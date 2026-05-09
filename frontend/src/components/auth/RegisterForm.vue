<template>

</template>

<script>
import { ref, computed } from 'vue';
import BaseInput from '../common/BaseInput.vue';
import BaseButton from '../common/BaseButton.vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { useToast } from 'bootstrap-vue-next';


export default {
    name: 'RegisterForm',
    components: {
        BaseInput, BaseButton},
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()
        const {showSucces, showError} = useToast

        const formData = ref({
            email: '',
            username: '',
            first_name: '',
            last_name: '',
            password: '',
            confirm_password: '',
            agree_terms: false,})
            
    }
}
</script>

<style>

</style>