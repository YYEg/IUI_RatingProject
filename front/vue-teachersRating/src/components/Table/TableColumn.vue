<template>
  <div class="table-column">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.table-column {
  padding: 15px 0;
  position: relative;
  color: #000000;
  &__title {
    margin: 5px;
    display: none;
    @media screen and (max-width: 768px) {
      display: inline-block;
    }
  }
}
</style>
