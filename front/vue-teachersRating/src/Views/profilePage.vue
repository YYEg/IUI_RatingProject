<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'

const achivmentsData = ref([]) // Достижения преподавателя
const achievementData = ref([]) // Все достижения
const scoresData = ref([]) // Стоимости достижений
const teacherData = ref([]) // Данные преподавателя
const userData = ref(null) // Данные пользователя
const teacherId = ref(null) // ID преподавателя из данных пользователя
const userName = ref(null)
const successMessage = ref('')
const errorMessage = ref('')
const userDepatment = ref(null)
const token = ref(localStorage.getItem('token') || '')
const selectedAchievement = ref(null)
const isModalOpen = ref(false) 

// Шапка и размеры таблицы
const tableHeads = ['№', 'Достижение', 'Балл', '']
const tableSizeColumns = '1fr 8fr 2fr 2fr'

// Вычисляемое свойство для фильтрации достижений
const filteredAchievements = computed(() => {
  return achivmentsData.value.filter((achievement) => achievement.teacher_id === teacherId.value)
})

// Функция для получения текста достижения по его идентификатору
const getAchievementText = (achievementId) => {
  const achievement = achievementData.value.find((item) => item.id === achievementId)
  return achievement ? achievement.name : 'Достижение не найдено'
}


// Получение данных пользователя
const getUserData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/profile/', {
      headers: {
        Authorization: `Token ${token.value}` // Убедитесь, что токен определён
      }
    })
    userData.value = response.data
    console.log(userData.value)
    teacherId.value = userData.value.teacher // Установите teacherId из userData
    userName.value = userData.value.first_name
    userDepatment.value = userData.value.department
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}
const deleteAchievement = async (achievementId) => {
  try {
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/v1/teacher_achivments/${achievementId}/`,
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    )

    console.log('Achievement deleted successfully:', response.data)

    // Обновляем список достижений после удаления
    const teacherAchivmentsResponse = await axios.get(
      'http://127.0.0.1:8000/api/v1/teacher_achivments/'
    )
    achivmentsData.value = teacherAchivmentsResponse.data

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
    errorMessage.value = 'Error deleting achievement. Please try again later.'
    successMessage.value = ''

    // Скрываем сообщение об ошибке после некоторого времени
    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}

// Основная загрузка данных
const loadData = async () => {
  try {
    await getUserData() // Сначала получаем данные пользователя

    if (!teacherId.value) {
      throw new Error('Teacher ID not found in user data')
    }

    const [teacherAchivmentsResponse, achievementDataResponse, scoreDataResponce, teacherResponce] =
      await Promise.all([
        axios.get('http://127.0.0.1:8000/api/v1/teacher_achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/achivments/'),
        axios.get('http://127.0.0.1:8000/api/v1/score_values/'),
        axios.get(`http://127.0.0.1:8000/api/v1/teachers/${teacherId.value}`)
      ])

    achivmentsData.value = teacherAchivmentsResponse.data
    achievementData.value = achievementDataResponse.data
    scoresData.value = scoreDataResponce.data
    teacherData.value = teacherResponce.data
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

const addAchievement = async () => {
  try {
    const data = {
      teacher_id: userData.value.department,
      Achivment: selectedAchievement.value,
      score: getAchievementScore(selectedAchievement.value)
    }
    console.log(data)
    const response = await axios.post('http://127.0.0.1:8000/api/v1/teacher_achivments/', data, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })

    loadData()

    console.log('Achievement added successfully:', response.data)

    // Очистить выбранное достижение после добавления
    selectedAchievement.value = null

    // Показать сообщение об успехе
    successMessage.value = 'Успешно добавлено достижение!'
    errorMessage.value = '' // Обнуляем ошибку, если запрос успешен

    
    // Скрыть сообщение через некоторое время
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error('Ошибка при добавлении достижения:', error)
    // Устанавливаем сообщение об ошибке только при наличии ошибки
    errorMessage.value = 'Ошибка при добавлении достижения!'
    successMessage.value = '' // Убираем сообщение об успехе

    // Скрыть сообщение об ошибке через некоторое время
    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}

const closeModal = () => {
  isModalOpen.value = false
}

// Функция для открытия модального окна
const openModal = () => {
  isModalOpen.value = true
}

const getAchievementScore = (achievementId) => {
  const score = scoresData.value.find((item) => item.Achivment === achievementId)
  return score ? score.score : 0
}

onMounted(() => {
  loadData()
})
</script>


<template>
  <div class="h-full">
    <headerBlock>
      <div class="grid grid-cols-2">
        <div>
          <div
            class="flex justify-center mr-2 items-center border-4 text-xl p-2 text-center font-bold transition hover:scale-105 cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
            @click="downloadReport"
          >
            Вывести данные в отчет
          </div>
          <div
            class="flex justify-center mr-2 items-center border-4 border-green-400 text-xl p-2 mt-2 text-center text-green-500 font-bold transition hover:scale-105 cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
            @click="openModal"
          >
            Добавить достижение
          </div>
        </div>

        <div
          class="flex justify-center items-center border-4 border-red-400 text-2xl p-4 text-center text-red-400 font-bold transition hover:scale-105 cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
          @click="setLogout()"
        >
          Выйти
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
    <div class="m-auto grid grid-cols-2 items-center mt-4 justify-items-center">
      <a class="text-3xl text-slate-400 font-bold hover:underline cursor-pointer" href="/">
        ← Назад
      </a>
      <div v-if="userData">
        <div
          class="text-3xl text-blue-400 font-bold m-auto grid grid-cols-1 items-center justify-items-center"
        >
          {{ userName }}
        </div>
      </div>
    </div>

    <div class="p-2">
      <!-- <div v-if="userData">
        <div
          class="text-3xl text-blue-400 font-boldm-auto grid grid-cols-1 items-center p-5 justify-items-center"
        >
          Кафедра
        </div>
      </div> -->
      <base-table :head="tableHeads" :columnTemplates="tableSizeColumns">
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
          <TableColumn><button
              @click="deleteAchievement(achievement.id)"
              class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
            >
              Удалить
            </button></TableColumn>
        </table-row>
      </base-table>

      <div class="m-auto grid grid-cols-2 items-center p-5 justify-items-center">
        <div class="text-3xl text-blue-400 font-bold">Итого баллов:</div>
        <div class="text-5xl text-blue-400 font-bold">{{ calculateTotalScore }}</div>
      </div>
      <!-- Модальное окно -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50"
    >
      <div class="bg-white p-5 rounded-lg shadow-lg max-w-lg w-full">
        <div class="flex justify-between items-center">
          <h2 class="text-3xl font-bold text-gray-800">Добавить достижение</h2>
          <button @click="closeModal" class="text-2xl text-red-500">×</button>
        </div>

        <select v-model="selectedAchievement" class="text-2xl rounded-xl mt-5 w-full">
          <option v-for="achievement in achievementData" :key="achievement.id" :value="achievement.id">
            {{ getAchievementScore(achievement.id) }} баллов | {{ achievement.name }}
          </option>
        </select>

        <div
          class="w-full shadow-2xl text-center hover:bg-green-300 text-2xl text-slate-400 font-bold transition hover:text-slate-600 hover:scale-105 cursor-pointer bg-green-200 ms-5 p-2 rounded-3xl m-5"
          @click="addAchievement()"
        >
          Добавить
        </div>

        <!-- Success Message Popup -->
        <transition name="fade">
          <div v-if="successMessage" class="success-popup text-3xl font-bold text-green-400">
            {{ successMessage }}
          </div>
        </transition>

        <!-- Error Message Popup -->
        <transition name="fade">
          <div v-if="errorMessage" class="success-popup text-3xl font-bold text-red-400">
            {{ errorMessage }}
          </div>
        </transition>
      </div>
    </div>
    </div>
  </div>
</template>
