<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'

// Заголовки столбцов таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Наименование кафедры' },
  { key: 'sum', label: 'Сумма баллов' },
  { key: 'rating', label: 'Рейтинг' }
]
const tableSizeColumns = '1fr 8fr 3fr 3fr'

const departmentData = ref([]) // Данные кафедр
const searchQuery = ref('') // Поиск по названию кафедры
const token = ref(localStorage.getItem('token') || '') // Токен пользователя
const isLoggedIn = ref(!!token.value) // Проверка авторизации

// Делаем объект реактивным
const sortBy = reactive({
  column: 'sum',
  order: 'desc'
})

onMounted(async () => {
  // Проверяем, есть ли токен
  if (!token.value) {
    // Если токена нет, перенаправляем на страницу авторизации
    window.location.href = '/login'
    return
  }
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/department_ratings/')
    departmentData.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки данных кафедр:', error)
  }
})

// Функция смены порядка сортировки
const sortTable = (column) => {
  if (sortBy.column === column) {
    sortBy.order = sortBy.order === 'asc' ? 'desc' : 'asc' // Меняем порядок сортировки
  } else {
    sortBy.column = column // Устанавливаем новый столбец
    sortBy.order = 'desc' // По умолчанию сортируем по убыванию
  }
}

// Вычисляемый список с фильтрацией и сортировкой
const filteredDepartmentData = computed(() => {
  return departmentData.value.filter((department) =>
    department.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const sortedDepartmentData = computed(() => {
  return [...filteredDepartmentData.value].sort((a, b) => {
    let aValue = a[sortBy.column]
    let bValue = b[sortBy.column]

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortBy.order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
    } else {
      return sortBy.order === 'asc' ? aValue - bValue : bValue - aValue
    }
  })
})
</script>

<template>
  <div class="h-screen m-auto mt-10">
    <headerBlock>
      <div class="flex justify-end">
        <div
          class="flex justify-end w-content p-4 transition hover:scale-105 cursor-pointer"
          @click="() => $router.push('/profile')"
        >
          <img src="../assets/vvv.png" alt="Логотип" class="h-20 w-auto" />
        </div>
      </div>
    </headerBlock>

    <div class="flex grid grid-cols-2 items-center mt-4 mx-4">
      <div class="relative">
        <input
          v-model="searchQuery"
          class="appearance-none border-2 pl-10 border-gray-300 hover:border-gray-400 transition-colors rounded-md w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:ring-blue-900 focus:border-blue-900 focus:shadow-outline"
          type="text"
          placeholder="Search..."
        />
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
          id="countries"
          class="bg-white border border-gray-300 text-sm rounded-md focus:ring-blue-900 block w-full p-2"
        >
          <option selected>01.09.2024-31.08.2025 (Текущий)</option>
          <option>01.09.2023-31.08.2024</option>
          <option>01.09.2022-31.08.2023</option>
        </select>
      </form>
    </div>

    <div class="grid grid-cols-2 items-center justify-items-center mt-4">
      <div class="grid grid-cols-2 items-center justify-items-center mt-4">
        <div
          class="text-2xl p-4 h-16 border-slate-400 text-center text-white font-sm transition cursor-pointer bg-blue-900 rounded-t-md shadow-2xl gap-2"
        >
          Подразделения
        </div>
        <div
          class="text-2xl p-4 h-16 border-slate-300 border-x-2 border-t-2 text-center text-slate-400 font-sm transition cursor-pointer rounded-t-md shadow-2xl"
        >
          <a href="/teachersRatingPage">Сотрудники</a>
        </div>
      </div>
    </div>

    <BaseTable :columnTemplates="tableSizeColumns">
      <TableRow :columnTemplates="tableSizeColumns">
        <TableColumn
          v-for="head in tableHeads"
          :key="head.key"
          @click="sortTable(head.key)"
          class="cursor-pointer font-sm text-white"
        >
          {{ head.label }}
          <span v-if="sortBy.column === head.key">
            {{ sortBy.order === 'asc' ? '▲' : '▼' }}
          </span>
        </TableColumn>
      </TableRow>

      <template #body>
        <TableRow
          v-for="(department, index) in sortedDepartmentData"
          :key="department.id"
          :columnTemplates="tableSizeColumns"
        >
          <TableColumn>{{ index + 1 }}</TableColumn>
          <TableColumn class="cursor-pointer">
            <router-link :to="{ name: 'departmentInsidePage', params: { id: department.id } }">
              {{ department.name }}
            </router-link>
          </TableColumn>
          <TableColumn>{{ department.sum }}</TableColumn>
          <TableColumn>{{ department.rating }}</TableColumn>
        </TableRow>
      </template>
    </BaseTable>
  </div>
</template>
