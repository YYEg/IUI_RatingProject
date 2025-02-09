<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const achivmentsData = ref([])
const teacherId = ref(null) // ID преподавателя из данных пользователя
const successMessage = ref('')
const errorMessage = ref('')
const token = ref(localStorage.getItem('token') || '')
const route = useRoute()
const isLoggedIn = computed(() => !!token.value)

// Шапка и размеры таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Достижение' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 8fr 2fr 2fr'
const searchQuery = ref('')
const sortBy = reactive({
  column: 'score',
  order: 'desc'
})

// Получение данных пользователя
const getUserData = async () => {
  try {
    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/employee/${route.params.empl_id}/achievement/${route.params.ach_id}/achievements/`
    )
    achivmentsData.value = achievementsResponse.data.achievements
    console.log(achivmentsData.value)

  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}

const deleteAchievement = async (achievementId) => {
  try {
    console.log(achievementId)
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/v1/delete_employee_achievement/${achievementId}/`, // Обновленный URL
      {
        headers: { Authorization: `Token ${token.value}` }
      }
    )

    console.log('Achievement deleted successfully:', response.data)

    // Обновляем список достижений после удаления
    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/employee/${route.params.empl_id}/achievement/${route.params.ach_id}/achievements/`
    )
    achivmentsData.value = achievementsResponse.data.achievements

    // Показываем сообщение об успешном удалении
    successMessage.value = 'Успешно удалено достижение!'
    errorMessage.value = ''

    // Скрываем сообщение об успешном удалении после некоторого времени
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error('Error deleting achievement:', error)

    // Показываем сообщение об ошибке при удалении
    errorMessage.value = 'Ошибка при удалении достижения. Попробуйте позже.'
    successMessage.value = ''

    // Скрываем сообщение об ошибке после некоторого времени
    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}

onMounted(async () => {
  // Проверяем, есть ли токен
  if (!token.value) {
    // Если токена нет, перенаправляем на страницу авторизации
    window.location.href = '/login'
    return
  }
  getUserData()
  console.log(teacherId.value)
})

const setLogout = () => {
  localStorage.removeItem('token')
  window.location.href = '/login'
}

const filteredAchievements = computed(() => {
  return achivmentsData.value.filter((achievement) =>
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

// Вычисляемый список с фильтрацией и сортировкой
const filteredDepartmentData = computed(() => {
  return departmentData.value.filter((department) =>
    department.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const totalScore = computed(() => {
  return sortedAchievements.value.reduce((sum, achievement) => sum + achievement.score, 0)
})
</script>

<template>
  <div class="h-full">
    <headerBlock>
      <div class="grid grid-cols-1">
        <div
          class="ml-4 flex justify-center items-center text-black bg-white text-2xl p-4 text-center font-sm transition hover:scale-105 cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
          @click="setLogout()"
        >
          Выйти
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

    <div class="grid grid-cols-3 mt-4 mx-4">
      <div
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="() => $router.go(-1)"
      >
        Назад
      </div>
    </div>
    <div class="p-2">

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
            <TableColumn>{{ index + 1 }}</TableColumn>
            <TableColumn class="cursor-pointer">
              {{ achievement.full_name }}
          </TableColumn>
            <TableColumn>{{ achievement.score }}</TableColumn>
            <TableColumn
              ><button
                @click="deleteAchievement(achievement.id)"
                class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
              >
                Удалить
              </button></TableColumn
            >
          </TableRow>
        </template>
      </BaseTable>

      <div class="text-center text-2xl font-bold mt-4">Итого баллов: {{ totalScore }}</div>
    </div>
  </div>
</template>
