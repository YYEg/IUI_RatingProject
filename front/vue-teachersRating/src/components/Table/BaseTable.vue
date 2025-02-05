<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  columnTemplates: {
    type: String,
    required: false
  }
})
</script>

<template>
  <div class="flex justify-center mb-10 rounded-t-xl">
    <div class="w-11/12 h-full rounded-t-xl text-l font-bold shadow-xl">
      <!-- Шапка таблицы -->
      <div class="grid border-4 border-blue-900 p-2 rounded-t-md shadow-xl "
        :style="{ gridTemplateColumns: columnTemplates }"
      >
        <slot></slot> <!-- Заголовки -->
      </div>

      <!-- Тело таблицы -->
      <div class="grid" :style="{ gridTemplateColumns: columnTemplates }">
        <slot name="body"></slot> <!-- Данные -->
      </div>
    </div>
  </div>
</template>

