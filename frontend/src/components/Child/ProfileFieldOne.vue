<template>
    <div :class="[nameClass, 'user__field']">
        <label :for="labelProps">{{ labelProps }}</label>
        <input :type="text" :id="nameProps" :name="nameProps" v-model="model">
    </div>
</template>

<script setup>
import { computed, defineEmits } from 'vue';


const props = defineProps({
    nameProps: String,
    labelProps: String
})
const model = defineModel([{ 'type': String, default: ''}])

const nameClass = computed(() => `data-user__${props.nameProps}`)
const emit = defineEmits(['update:valueProps'])
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