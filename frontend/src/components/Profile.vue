<template>
    <div class="profile-page">
        <ProfileFields />
    </div>
</template>

<script setup>
import ProfileFields from './ProfileFields.vue';
</script>

<style>
.profile-page {
    display: flex;
    flex-direction: row;
    gap: 200px;
}
</style>