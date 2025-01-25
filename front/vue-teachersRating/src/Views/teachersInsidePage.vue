<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, onUpdated } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const achivmentsData = ref([])
const achievementData = ref([]) // Данные о достижениях
const scoresData = ref([]) //информация о стоимости достижений
const teacherData = ref([]) //Преподаватель
const userData = ref(null)

//Шапка и размеры таблицы
const tableHeads = ['№', 'Достижение', 'Балл']
const tableSizeColumns = '1fr 8fr 3fr'

const route = useRoute() // Получаем текущий маршрут

const teacherId = computed(() => {
  return Number(route.params.id)
})

onMounted(async () => {
  try {
    const [teacherAchivmentsResponse, achievementDataResponse, scoreDataResponce, teacherResponce] =
      await Promise.all([
        axios.get('http://127.0.0.1:8000/api/v1/teacher_achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/score_values/'),
        axios.get('http://127.0.0.1:8000/api/v1/teachers/' + teacherId.value)
      ])

    achivmentsData.value = teacherAchivmentsResponse.data
    achievementData.value = achievementDataResponse.data
    scoresData.value = scoreDataResponce.data
    teacherData.value = teacherResponce.data

    // Перед началом перебора достижений обнуляем сумму баллов
    resetSumScore()
  } catch (error) {
    console.log(error)
  }
})

// Вычисляемое свойство для получения суммы баллов
const sumScore = computed(() => {
  // Используем метод reduce для подсчёта суммы баллов
  return filteredAchievements.value.reduce((total, achievement) => {
    return total + getAchievementScore(achievement.Achivment_id)
  }, 0)
})

// Функция для получения текста достижения по его идентификатору
const getAchievementText = (achievementId) => {
  const achievement = achievementData.value.find((item) => item.id === achievementId)
  return achievement ? achievement.name : 'Достижение не найдено'
}

// Функция для обнуления суммы баллов
const resetSumScore = () => {
  sumScore.value = 0
}

// Функция для получения баллов достижения по его идентификатору
const getAchievementScore = (achievementId) => {
  const score = scoresData.value.find((item) => item.Achivment === achievementId)
  return score ? score.score : 0
}

const filteredAchievements = computed(() => {
  return achivmentsData.value.filter((achievement) => achievement.teacher_id === teacherId.value)
})

const getUserData = () => {
  axios
    .get('http://127.0.0.1:8000/profile/', {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      userData.value = response.data
    })
    .catch((error) => {
      console.error('Error fetching user data:', error)
    })
}
</script>

<template>
  <div class="w-4/5 h-full m-auto bg-slate-200 rounded-xl shadow-2xl mt-10">
    <headerBlock @click="() => $router.push('/')" />

    <div class="m-auto grid grid-cols-2 items-center p-5 justify-items-center">
      <a
        class="text-3xl text-slate-400 font-bold hover:underline cursor-pointer"
        @click="$router.go(-1)"
      >
        ← Назад
      </a>
      <div class="items-center p-2 justify-items-center text-3xl font-bold text-blue-400">
        {{ teacherData.surname }} {{ teacherData.name }} {{ teacherData.parentName }}
      </div>
    </div>

    <base-table :head="tableHeads" :columnTemplates="tableSizeColumns" @sorting="setSort">
      <table-row
        v-for="(achievement, index) in filteredAchievements"
        :key="achievement.id"
        :columnTemplates="tableSizeColumns"
      >
        <table-column>{{ index + 1 }}</table-column>
        <table-column>
          {{ getAchievementText(achievement.Achivment_id) }}
        </table-column>
        <table-column>{{ getAchievementScore(achievement.Achivment_id) }}</table-column>
      </table-row>
    </base-table>

    <div class="m-auto grid grid-cols-2 items-center p-5 justify-items-center">
      <div class="text-3xl text-blue-400 font-bold">Итого баллов:</div>
      <div class="text-5xl text-blue-400 font-bold">{{ sumScore }}</div>
    </div>
  </div>
</template>
