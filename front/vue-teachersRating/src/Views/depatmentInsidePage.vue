<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const tableHeads = ['№', 'ФИО', 'Сумма баллов', 'Рейтинг']
const tableSizeColumns = '1fr 8fr 3fr 3fr'
const teachersData = ref([])
const token = ref(localStorage.getItem('token') || '') // Токен пользователя
const isLoggedIn = ref(!!token.value) // Проверка авторизации

const route = useRoute() // Получаем текущий маршрут
const departmentId = computed(() => {
  return Number(route.params.id)
})

// Вытягиваю данные с бека
onMounted(async () => {
  try {
    const teacherResponse = await axios.get(
      `http://127.0.0.1:8000/api/v1/departments/${departmentId.value}/teachers/`
    )
    teachersData.value = teacherResponse.data
    console.log(teachersData.value)
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <div class="h-screen m-auto mt-10">
    <headerBlock>
      <div class="flex justify-center">
        <div
          v-if="isLoggedIn"
          class="w-full flex justify-center items-center text-black text-2xl p-4 text-center font-sm transition hover:scale-105 cursor-pointer bg-white rounded-2xl shadow-2xl"
          @click="() => $router.push('/profile')"
        >
          Личный кабинет
        </div>
        <div
          v-else
          class="w-full flex justify-center items-center text-black text-2xl p-4 text-center font-sm transition hover:scale-105 cursor-pointer bg-white rounded-2xl shadow-2xl"
          @click="() => $router.push('/login')"
        >
          Войти
        </div>
      </div>
    </headerBlock>

    <!-- Фильтры -->
    <div class="flex grid grid-cols-2 items-center my-4 mx-4">
      <div class="relative">
        <input
          class="appearance-none border-2 pl-10 border-gray-300 hover:border-gray-400 transition-colors rounded-md w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:ring-purple-600 focus:border-purple-600 focus:shadow-outline"
          id="search"
          type="text"
          placeholder="Search..."
        />
        <div class="absolute right-0 inset-y-0 flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="-ml-1 mr-3 h-5 w-5 text-gray-400 hover:text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>
        <div class="absolute left-0 inset-y-0 flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6 ml-3 text-gray-400 hover:text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>
      <form class="mx-4">
        <select
          id="period"
          class="bg-white border border-gray-300 text-sm rounded-md focus:ring-blue-900 block w-full p-2"
        >
          <option selected>01.09.2024-31.08.2025 (Текущий)</option>
          <option>01.09.2023-31.08.2024</option>
          <option>01.09.2022-31.08.2023</option>
        </select>
      </form>
    </div>

    <div class="grid grid-cols-2 mt-4 mx-4">
      <div
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="() => $router.push('/')"
      >
        Назад
      </div>
      <div
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="downloadReport"
      >
        Вывести данные в отчет
      </div>
    </div>

    <base-table :head="tableHeads" :columnTemplates="tableSizeColumns">
      <table-row
        v-for="(teacher, index) in teachersData"
        :key="teacher.id"
        :columnTemplates="tableSizeColumns"
      >
        <table-column>{{ index + 1 }}</table-column>
        <table-column class="text-blue-400 underline cursor-pointer">
          <router-link :to="{ name: 'teachersInsidePage', params: { id: teacher.id } }">
            {{ teacher.surname }} {{ teacher.name }} {{ teacher.parentName }}
          </router-link>
        </table-column>
        <table-column>{{ teacher.total_score }}</table-column>
        <!-- Сумма баллов -->
        <table-column>{{ index + 1 }}</table-column>
      </table-row>
    </base-table>
  </div>
</template>
