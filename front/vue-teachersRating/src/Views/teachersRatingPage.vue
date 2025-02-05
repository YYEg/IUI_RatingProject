<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive } from 'vue'
import axios from 'axios'

const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'fullName', label: 'ФИО' },
  { key: 'total_score', label: 'Сумма баллов' },
  { key: 'rating', label: 'Рейтинг' }
]
const tableSizeColumns = '1fr 8fr 3fr 3fr'
const employeesData = ref([])
const isLoggedIn = computed(() => !!token.value)
const token = ref(localStorage.getItem('token') || '')
const searchQuery = ref('')
const selectedPeriod = ref('01.09.2024-31.08.2025')

const sortBy = reactive({
  column: 'total_score',
  order: 'desc'
})

// Фильтрация данных
const filteredEmployees = computed(() => {
  return employeesData.value.filter(employee => {
    const fullName = `${employee.surname} ${employee.name} ${employee.parentName}`.toLowerCase();
    return fullName.includes(searchQuery.value.toLowerCase());
  });
});

// Функция сортировки
const sortTable = (column) => {
  if (sortBy.column === column) {
    sortBy.order = sortBy.order === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.column = column
    sortBy.order = 'desc'
  }
}

// Отсортированные данные
const sortedEmployees = computed(() => {
  return [...filteredEmployees.value].sort((a, b) => {
    let aValue, bValue
    
    if (sortBy.column === 'fullName') {
      aValue = `${a.surname} ${a.name} ${a.parentName}`.toLowerCase()
      bValue = `${b.surname} ${b.name} ${b.parentName}`.toLowerCase()
    } else {
      aValue = a[sortBy.column]
      bValue = b[sortBy.column]
    }

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortBy.order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
    } else {
      return sortBy.order === 'asc' ? aValue - bValue : bValue - aValue
    }
  })
})

// Вытягиваю данные с бека для всех сотрудников
onMounted(async () => {
  try {
    const employeeResponse = await axios.get('http://127.0.0.1:8000/api/v1/employees/')
    employeesData.value = employeeResponse.data
    console.log(employeesData.value)
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <div class="m-auto mt-10">
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
          v-model="selectedPeriod"
          class="bg-white border border-gray-300 text-sm rounded-md focus:ring-blue-900 block w-full p-2"
        >
          <option>01.09.2024-31.08.2025 (Текущий)</option>
          <option>01.09.2023-31.08.2024</option>
          <option>01.09.2022-31.08.2023</option>
        </select>
      </form>
    </div>

    <div class="grid grid-cols-2 items-center justify-items-center mt-4">
      <div class="grid grid-cols-2 items-center justify-items-center mt-4">
        <div class="text-2xl p-4 h-16 border-slate-300 border-x-2 border-t-2 text-center text-slate-400 font-sm transition cursor-pointer rounded-t-md shadow-2xl">
          <a href="/departamentRatingPage">Кафедры</a>
        </div>
        <div class="text-2xl p-4 h-16 border-slate-400 text-center text-white font-sm transition cursor-pointer bg-blue-900 rounded-t-md shadow-2xl">
          Преподаватели
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
          v-for="(employee, index) in sortedEmployees"
          :key="employee.id"
          :columnTemplates="tableSizeColumns"
        >
          <TableColumn>{{ index + 1 }}</TableColumn>
          <TableColumn class="cursor-pointer">
            <router-link :to="{ name: 'teachersInsidePage', params: { id: employee.id } }">
              {{ employee.surname }} {{ employee.name }} {{ employee.parentName }}
            </router-link>
          </TableColumn>
          <TableColumn>{{ employee.total_score }}</TableColumn>
          <TableColumn>{{ employee.rating }}</TableColumn>
        </TableRow>
      </template>
    </BaseTable>
  </div>
</template>
