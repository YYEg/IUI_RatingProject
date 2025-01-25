<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const tableHeads = ['№', 'ФИО', 'Сумма балов', 'Рейтинг']
const tableSizeColumns = '1fr 8fr 3fr 3fr'

const teachersData = ref([])
const achivmentsData = ref([])
const departmentData = ref([])
const achievementData = ref([]) // Данные о достижениях
const scoresData = ref([]) //информация о стоимости достижений

const route = useRoute() // Получаем текущий маршрут

const departmentId = computed(() => {
  return Number(route.params.id)
})

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
    teachersData.value = teachersData.value.filter(
      (teacher) => teacher.department_id === departmentId.value
    )
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
  <div class="w-4/5 h-screen m-auto bg-slate-200 rounded-xl shadow-2xl mt-10">
    <headerBlock
      ><div
        class="text-2xl shadow-2xl text-slate-400 font-bold transition hover:text-blue-400 hover:scale-105 cursor-pointer bg-slate-200 ms-5 p-2 rounded-3xl"
        @click="() => $router.push('/profile')"
      >
        Переход в ЛК заведующего кафедрой
      </div></headerBlock
    >
    <div class="ms-5 p-5 items-center justify-items-center">
      <a
        class="text-3xl text-slate-400 font-bold hover:underline cursor-pointer"
        href="/departamentRatingPage"
      >
        ← Назад
      </a>
    </div>
    <base-table :head="tableHeads" :columnTemplates="tableSizeColumns">
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
