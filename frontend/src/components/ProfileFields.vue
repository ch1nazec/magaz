<template>
        <div class="profile__current-profile">
            <h1 class="display-4">Личный кабинет</h1>
        </div>
        <div class="data-user" v-if="user">
            <div v-for="(value, key) in user" :key='key' v-if="key !== 'id'">
                <div class="field" v-if="key !== 'id'">
                    <ProfileFieldOne 
                    :nameProps='key'
                    v-model=user[key]
                    :labelProps=translateKeys[key]
                    />
                </div>
            </div>
            <!-- for (const [key, value] of Object.entires(user)) {
                <ProfileFieldOne 
                nameProps="key"
                v-model="value"
                :labelProps="translateKeys[key]"
            />
            }
            <ProfileFieldOne 
                nameProps="user.first_name"
                v-model="userData.first_name"
                :labelProps="translateKeys['first_name']"
            />
            <div class="data-user__last_name user__field">
                <label for="last_name">Фамилия</label>
                <input type="text" id="last_name" name="last_name" v-model="user.last_name">
            </div>
            <div class="data-user__email user__field">
                <label for="email">Почта</label>
                <input type="text" id="email" name="email" v-model="user.email">
            </div>
            <div class="data-user__phone user__field">
                <label for="phone">Номер телефона</label>
                <input type="text" id="phone" name="phone" v-model="user.phone">
            </div>
            <div class="data-user__telegram_id user__field">
                <label for="telegram_id">ID телеграмм</label>
                <input type="text" id="telegram_id" name="telegram_id" v-model="user.telegram_id">
            </div>
            <div class="data-user__address user__field">
                <label for="address">Адрес доставки</label>
                <input type="text" id="address" name="address" v-model="user.address">
            </div> -->
        </div>
        <div class="data-user-loading" v-else>
            Loading...
        </div>
</template>


<script setup>
import ProfileFieldOne from './Child/ProfileFieldOne.vue';

import { useAuthStore } from '@/stores/auth';
import { computed, onMounted, ref } from 'vue';

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const userData = ref({
  first_name: 'Иван',
  last_name: '',
  username: '',
  email: '',
  phone_number: '',
  address: '',
  telegram_id: '',
})

const translateKeys = {
    'first_name': 'Имя',
    'last_name': 'Фамилия',
    'username': 'Логин',
    'email': 'Почта',
    'phone_number': 'Номер телефона',
    'address': 'Адрес',
    'telegram_id': 'ID Tg',
}

onMounted(async () => {
    authStore.initialize()})
</script>

<style>
.data-user {
    padding-top: 100px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    
    width: 600px;
    height: 150px;
}
</style>