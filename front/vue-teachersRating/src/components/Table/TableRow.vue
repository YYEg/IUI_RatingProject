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
  border-bottom: 2px solid #000000;
  background-color: #ffffff;
  position: relative;
  display: grid;
  column-gap: 10px;
  align-items: center;
  padding: 0 16px;
  text-align: center;
  
  @media screen and (max-width: 768px) {
    display: block;
  }
  &:last-child {
    border-bottom: none;
  }
  &--items-center {
    justify-items: center;
  }
}
</style>
