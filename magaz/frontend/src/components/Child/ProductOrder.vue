<template>
    <div class="ordering">
        <select v-model="variantOrder" class="select__order">
            <option value="name">А-Я (A-Z)</option>
            <option value="-name">Я-А (Z-A)</option>
        </select>
    </div>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';

const variantOrder = ref('')
const emit = defineEmits(['select-order'])


watch(variantOrder, (newElem) => {
    emit('select-order', newElem)
})
</script>

<style>
.ordering {
  margin-bottom: 20px;
}

.select__order {
  /* Сброс стандартного вида */
  appearance: none; 
  -webkit-appearance: none;
  -moz-appearance: none;

  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  border: 0.5px solid;
  
  background-color: #fff;
  border-radius: 4px;
  padding: 8px 35px 8px 15px; /* Запас справа для своей стрелочки */
  cursor: pointer;
  transition: all 0.3s ease;

  /* Кастомная стрелочка (SVG) */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

.select__order:hover {
  background-color: #f5f5f5;
}

.select__order:focus {
  outline: none;
}

/* Стилизация option (работает ограниченно в Chrome/Safari) */
.select__order option {
  font-family: 'Montserrat', sans-serif;
  background-color: #fff;
  padding: 10px;
}
</style>