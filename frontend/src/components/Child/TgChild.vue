<template>
  <button
    type="button"
    class="a-telegram-button"
    @click="connectTelegram"
  >
    <div class="telegram-button">
      <img
        src="@/assets/TelegramLogo.png"
        alt=""
        width="30"
        height="30"
      />
      <p class="telegram-text">Подключить свой телеграм</p>
    </div>
  </button>
</template>

<script setup>
import api from '@/services/api';

const BOT_NAME = import.meta.env.VITE_TELEGRAM_BOT_NAME;

const connectTelegram = async () => {
  try {
    const response = await api.post('users/telegram-link/');
    const token = response.data.token;

    if (!token || !BOT_NAME) {
      throw new Error('Не получен токен или не задано имя Telegram-бота');
    }

    const botName = BOT_NAME.replace(/^@/, '');

    window.location.href =
      `https://t.me/${botName}?start=${encodeURIComponent(token)}`;
  } catch (error) {
    console.error('Ошибка при генерации ссылки:', error);
    alert('Не удалось сгенерировать ссылку для привязки');
  }
};
</script>
<style scoped>
.telegram-button img,
.telegram-button .telegram-text {
    pointer-events: none;
    -webkit-user-select: none;
    user-select: none;
    -webkit-user-drag: none;
}


.a-telegram-button {
    text-decoration: none;
    transition: all 0.3s ease-in-out;
    cursor: pointer;

    :hover {
        background-color: #006699;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 136, 204, 0.3);

        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }
    :active {
       transition: all 0.3s ease-in-out;
        cursor: pointer; 
    }
}
.telegram-button {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;

    border: solid 0px;
    margin-top: 24px;
    padding: 10px 10px;

    width: 230px;
    height: 40px;
    box-sizing: border-box;


    color: white;
    background-color: #24A1DE;
}

.telegram-text {
    font-size: 11px;
    width: 100px;
    margin: 0;
}
</style>