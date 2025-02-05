<script setup>
const props = defineProps({
  columnTemplates: {
    type: String,
    required: false
  }
})
</script>

<template>
  <div class="table-row" :style="{ gridTemplateColumns: columnTemplates }">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.table-row {
  display: contents; /* Убирает лишний div, сохраняя стили ячеек */
}
</style>
