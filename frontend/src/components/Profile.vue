<template>
    <div class="profile-page">
        <div class="profile__current">
            <h1 class="display-4">Личный кабинет</h1>
        </div>
        <ProfileFields />
    </div>
</template>

<script setup>
import ProfileFields from './ProfileFields.vue';
</script>

<style scoped>
.profile-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.profile__current {
    max-width: 1400px;
    /* margin: 0 auto; */
    /* padding: 0 100px; */
}
</style>