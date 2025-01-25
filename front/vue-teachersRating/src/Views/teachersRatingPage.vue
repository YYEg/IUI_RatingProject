<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'

const tableHeads = ['№', 'ФИО', 'Сумма баллов', 'Рейтинг']
const tableSizeColumns = '1fr 8fr 3fr 3fr'

const teachersData = ref([])
const achivmentsData = ref([])
const achievementData = ref([]) // Данные о достижениях
const scoresData = ref([]) // информация о стоимости достижений
const isLoggedIn = computed(() => !!token.value); // Проверяем, есть ли токен

const token = ref(localStorage.getItem('token') || '')
// Вытягиваю данные с бека
onMounted(async () => {
  try {
    const [teacherAchivmentsResponse, achievementDataResponse, scoreDataResponce, teacherResponce] =
      await Promise.all([
        axios.get('http://127.0.0.1:8000/api/v1/teacher_achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/score_values/'),
        axios.get('http://127.0.0.1:8000/api/v1/teachers/')
      ])

    achivmentsData.value = teacherAchivmentsResponse.data
    achievementData.value = achievementDataResponse.data
    scoresData.value = scoreDataResponce.data
    teachersData.value = teacherResponce.data
  } catch (error) {
    console.log(error)
  }
})

// Функция для получения баллов достижения по его идентификатору
const getAchievementScore = (achievementId) => {
  const score = scoresData.value.find((item) => item.Achivment === achievementId)
  return score ? score.score : 0
}

// Функция для вычисления суммы баллов для каждого преподавателя
const calculateSumScore = (teacherId) => {
  const filteredAchievements = achivmentsData.value.filter(
    (achievement) => achievement.teacher_id === teacherId
  )

  return filteredAchievements.reduce((total, achievement) => {
    return total + getAchievementScore(achievement.Achivment_id)
  }, 0)
}

// Обработка сортировки
const sortBy = ref({ column: 'sum', order: 'desc' }) // Изначально сортируем по сумме баллов по убыванию

const sortTable = (column) => {
  if (sortBy.value.column === column) {
    sortBy.value.order = sortBy.value.order === 'asc' ? 'desc' : 'asc'
  } else {
    sortBy.value.column = column
    sortBy.value.order = 'desc'
  }
}

const sortedTeachersData = computed(() => {
  return teachersData.value.slice().sort((a, b) => {
    const aValue = calculateSumScore(a.id)
    const bValue = calculateSumScore(b.id)
    if (sortBy.value.order === 'asc') {
      return aValue - bValue
    } else {
      return bValue - aValue
    }
  })
})
</script>

<template>
  <div class="m-auto mt-10">
    <headerBlock>
      <div class="flex justify-center">
        <div
          v-if="isLoggedIn"
          class="w-full flex justify-center items-center text-black text-2xl p-4 text-center text-balck font-sm transition hover:scale-105 cursor-pointer bg-white rounded-2xl shadow-2xl"
          @click="() => $router.push('/profile')"
        >
          Личный кабинет
        </div>
        <div
          v-else
          class="w-full flex justify-center items-center text-black text-2xl p-4 text-center text-balck font-sm transition hover:scale-105 cursor-pointer bg-white rounded-2xl shadow-2xl"
          @click="() => $router.push('/login')"
        >
          Войти
        </div>
      </div>
    </headerBlock>

    <div class="flex grid grid-cols-2 items-center mt-4 mx-4">
      <div class="relative">
        <input
          class="appearance-none border-2 pl-10 border-gray-300 hover:border-gray-400 transition-colors rounded-md w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:ring-purple-600 focus:border-purple-600 focus:shadow-outline"
          id="username"
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
          class="text-2xl p-4 h-16 border-slate-300 border-x-2 border-t-2 text-center text-slate-400 font-sm transition cursor-pointer rounded-t-md shadow-2xl"
        >
          <a href="/departamentRatingPage">Кафедры</a>
        </div>
        <div
          class="text-2xl p-4 h-16 border-slate-400 text-center text-white font-sm transition cursor-pointer bg-blue-900 rounded-t-md shadow-2xl"
        >
          Преподаватели
        </div>
      </div>
    </div>
    <base-table :head="tableHeads" :columnTemplates="tableSizeColumns" @sorting="sortTable">
      <table-row
        v-for="(teacher, index) in sortedTeachersData"
        :key="teacher.id"
        :columnTemplates="tableSizeColumns"
      >
        <table-column>{{ index + 1 }}</table-column>
        <table-column class="text-blue-400 underline cursor-pointer"
          ><router-link :to="{ name: 'teachersInsidePage', params: { id: teacher.id } }"
            >{{ teacher.surname }} {{ teacher.name }} {{ teacher.parentName }}</router-link
          >
        </table-column>
        <table-column @click="sortTable('sum')">{{ calculateSumScore(teacher.id) }}</table-column>
        <table-column>{{ index + 1 }}</table-column>
      </table-row>
    </base-table>
  </div>
</template>
