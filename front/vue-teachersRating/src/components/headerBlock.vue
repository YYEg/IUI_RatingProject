<template>
  <header
    class="bg-blue-900 text-white py-4 px-6 shadow-lg mx-4 mt-4 mb-2 rounded-xl border-2 border-emerald-800 drop-shadow-2xl items-center"
  >
    <div class="grid grid-cols-2">
      <div class="flex items-center">
        <img
          src="../assets/hearld_left.png"
          alt="Логотип"
          class="flex h-20 w-auto flex-shrink-0 hidden md:block"
        />
        <div class="flex flex-col rows-2 items-start ml-3 justify-end my-4">
          <h1 class="text-2xl font-bold">ИЮИ (ф) УП РФ</h1>
          <p class="text-sm mt-1">Система эффективного контракта сотрудника университета</p>
        </div>
      </div>
     <slot></slot>
    </div>
  </header>
</template>