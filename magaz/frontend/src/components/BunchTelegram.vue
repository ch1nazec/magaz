<template>
    <div class="telegram-auth-container">
    <h3>Привязать Telegram</h3>
    
    <div ref="telegramWidget"></div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/services/api';
import { useRoute } from 'vue-router';
const telegramWidget = ref(null);

window.onTelegramAuth = async (user) => {
  try {
    const response = await api.post('users/telegram-link/',);
    console.log(response.data);
  } catch (error) {
    console.error('Ошибка привязки:', error.response?.data || error.message);
    alert('Не удалось привязать Telegram');
  }
};

const route = useRoute()
const tgId = route.params.telegramId
</script>

<style>

</style>