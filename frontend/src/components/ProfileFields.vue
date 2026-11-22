<template>
    <form class="data-user" v-if="user" @submit.prevent="handleUpdate">

        <template v-for="(value, key) in user" :key="key" class="user_fields">
            <div class="field" v-if="key !== 'id' && translateKeys[key]">
                <ProfileFieldOne 
                    :nameProps="String(key)"
                    v-model="user[key]"
                    :labelProps="translateKeys[key]"
                />
            </div>
        </template>


        <div class="form-actions" >
            <button type="submit" :disabled="!isFormChanged" class="btn-update">Обновить данные</button>
        </div>
    </form>

    <div class="data-user-loading" v-else>
        Loading...
    </div>
</template>


<script setup>
import ProfileFieldOne from './Child/ProfileFieldOne.vue';

import { useAuthStore } from '@/stores/auth';
import { computed, onMounted, ref, watch } from 'vue';

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const form = ref(null)
const isFormChanged = computed(() => {
    if (!form.value || !user.value) return false
    return JSON.stringify(form.value) !== JSON.stringify(user.value)})

const translateKeys = {
    'first_name': 'Имя',
    'last_name': 'Фамилия',
    'username': 'Логин',
    'email': 'Почта',
    'phone_number': 'Номер телефона',
    'address': 'Адрес',
    'telegram_id': 'ID Tg',
}


const handleUpdate = async () => {
    user.value['phone_number'] = parseInt(user.value['phone_number'])
    user.value['telegram_id'] = parseInt(user.value['telegram_id'])

    await authStore.updateProfileData(user.value)
    location.reload()
}


watch(user, (newUser) => {
    if (newUser && !form.value) {
        form.value = JSON.parse(JSON.stringify(newUser))
    }
}, {immediate: true})

onMounted(async () => {
    authStore.initialize()})
</script>

<style>
.data-user {
    padding-top: 100px;
    display: grid;
    grid-template-columns: repeat(2, 1fr); 
    gap: 20px;
    
    width: 600px;
    min-height: 150px; 

    align-items: center; 
}

.field {
    width: 100%; 
}


.form-actions {
    display: flex;
    justify-content: center; 
    width: 100%;
}

.btn-update {
    border: solid 0px;
    padding: 10px;
    margin-top: 24px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
}

@media (max-width: 550px) {
    .data-user {
        width: 100%;
        grid-template-columns: 1fr;
    }
}
</style>