<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Достижение' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 8fr 3fr'
const isLoggedIn = computed(() => !!token.value)
const token = ref(localStorage.getItem('token') || '')
const achievementsData = ref([])
const searchQuery = ref('')
const role = computed(() => localStorage.getItem('role'))
const auth_user_department = computed(() => localStorage.getItem('department'))
const employee_department = ref('')
const sortBy = reactive({
  column: 'score',
  order: 'desc'
})
const route = useRoute()
const employeeId = route.params.id
// Флаг для отображения блока
const canDisplayBlock = ref(false)

onMounted(async () => {
  // Проверяем, есть ли токен
  if (!token.value) {
    // Если токена нет, перенаправляем на страницу авторизации
    window.location.href = '/login'
    return
  }
  try {
    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/v1/employe_achievments/employee/${employeeId}`
    )
    achievementsData.value = achievementsResponse.data.achievements
    console.log(achievementsData.value)
  } catch (error) {
    console.error(error)
  }
  try {
    const emp_response = await axios.get(`http://127.0.0.1:8000/api/v1/employees/${employeeId}`)
    employee_department.value = emp_response.data.department.id
  } catch (error) {
    console.error(error)
  }
  canDisplayBlock.value =
    role.value === 'ADMIN' ||
      role.value === 'OTV' ||
      (role.value === 'ZAV' &&
        String(employee_department.value) === String(auth_user_department.value))
  
})

const filteredAchievements = computed(() => {
  return achievementsData.value.filter((achievement) =>
    achievement.achievment_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const sortTable = (column) => {
  if (sortBy.column === column) {
    sortBy.order = sortBy.order === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.column = column
    sortBy.order = 'desc'
  }
}

const sortedAchievements = computed(() => {
  return [...filteredAchievements.value].sort((a, b) => {
    let aValue = a[sortBy.column]
    let bValue = b[sortBy.column]

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortBy.order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
    } else {
      return sortBy.order === 'asc' ? aValue - bValue : bValue - aValue
    }
  })
})

const totalScore = computed(() => {
  return sortedAchievements.value.reduce((sum, achievement) => sum + achievement.score, 0)
})
</script>

<template>
  <div class="m-auto mt-10">
    <headerBlock>
      <div class="flex justify-end">
        <div
          class="flex justify-end w-80 p-4 transition hover:scale-105 cursor-pointer bg-white rounded-2xl shadow-2xl"
          @click="() => $router.push('/profile')"
        >
          <div
            class="w-full flex justify-center items-center text-black text-3xl text-center font-sm"
          >
            Личный кабинет
          </div>
          <img src="../assets/profile.png" alt="Логотип" class="mr-4 h-20 w-auto" />
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

    <div class="grid grid-cols-3 mt-4 mx-4 gap-2">
      <div
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="() => $router.go(-1)"
      >
        Назад
      </div>
      <div></div>
      <div
        v-if="canDisplayBlock"
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="downloadReport"
      >
        Вывести данные в отчет
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
          v-for="(achievement, index) in sortedAchievements"
          :key="achievement.id"
          :columnTemplates="tableSizeColumns"
        >
          <TableColumn>{{ achievement.number }}</TableColumn>
          <TableColumn class="cursor-pointer">
            <router-link
              :to="{
                name: 'achievmentDetailed',
                params: { ach_id: achievement.id, empl_id: employeeId }
              }"
            >
              {{ achievement.achievment_name }}
            </router-link>
          </TableColumn>
          <TableColumn>{{ achievement.score }}</TableColumn>
        </TableRow>
      </template>
    </BaseTable>

    <div class="text-center text-2xl font-bold mt-4">Итого баллов: {{ totalScore }}</div>
  </div>
</template>
