<template>
    <div :class="[nameClass, 'user__field']" v-if="(props.nameProps !== 'telegram_id' || model)">
        <label :for="nameProps">{{ labelProps }}</label>
        <input :disabled="isDisableLogin" type="text" :id="nameProps" :name="nameProps" v-model="model">
    </div>

    <div :class='[nameClass, "field telegram-btn", "user__field"]' v-else-if="nameProps === 'telegram_id' && !model">
        <TgChild />
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import TgChild from './TgChild.vue';


const props = defineProps({
    nameProps: String,
    labelProps: String})
const model = defineModel({ type: [String, Number], default: '' });

const nameClass = computed(() => `data-user__${props.nameProps}`)
const isDisableLogin = ref(false)
onMounted(() => {
    if (props.nameProps === 'username') {
        isDisableLogin.value = true
    }

})
</script>

<style scoped>
.user__field {
    margin-bottom: 5px;

    label {
        display: block;
        margin-bottom: 4px;}
    input {
        border-radius: 0px;

        height: 35px;
        border: 1px solid #dee2e6;
        &:hover, &:active, &:focus {
            border-color: black;

            outline: none !important;
            box-shadow: none !important;
        }
    }
}
</style>