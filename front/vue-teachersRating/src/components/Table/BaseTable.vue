<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  head: {
    type: Array,
    required: false
  },
  columnTemplates: {
    type: String,
    required: false
  }
})

const emit = defineEmits(['sorting'])

const clickOnHead = (name) => {
  emit('sorting', name)
}
</script>

<template>
  <div class="flex justify-center mb-10 rounded-t-xl">
    <div class="w-11/12 h-full rounded-t-xl text-l font-bold shadow-xl">
      <div 
        class="grid gap-2 items-center border-b-2 border-blue-900 bg-blue-900 cursor-pointer p-2 rounded-t-md shadow-xl" 
        :style="{ gridTemplateColumns: columnTemplates }">
        <div 
          class="flex justify-center items-center text-white cursor-pointer" 
          v-for="(item, i) of head" 
          :key="i" 
          @click="clickOnHead(item)">
          {{ item }}
        </div>
      </div>
      <slot></slot>
    </div>
  </div>
</template>