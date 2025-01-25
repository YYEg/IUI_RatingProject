<script setup>
import axios from 'axios'
import headerBlock from '../components/headerBlock.vue'
import { ref, onMounted } from 'vue'
import router from '@/router'

const token = ref(localStorage.getItem('token') || '')
const userData = ref(null)


const achivmentsData = ref([])
const achievementData = ref([]) // Данные о достижениях
const scoresData = ref([]) //информация о стоимости достижений

// Переменная для управления состоянием модального окна

// Функции получения данных
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

onMounted(async () => {
  try {
    if (token.value) {
      getUserData()
    } else {
      router.push({ name: 'login' })
    }
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
      (teacher) => teacher.department_id === userData.value.department
    )
  } catch (error) {
    console.log(error)
  }
})

// Функции для работы с достижениями





// Функция для закрытия модального окна

</script>

<template>
  <div class="w-4/5 h-full m-auto bg-slate-200 rounded-xl shadow-2xl mt-10">
    <headerBlock />
    <div class="m-auto grid grid-cols-1 items-center p-5 justify-items-center">
      <a class="text-3xl text-slate-400 font-bold hover:underline cursor-pointer" href="/">
        ← Назад
      </a>
    </div>

    <div class="m-auto grid grid-cols-1 items-center p-5">
      <!-- Кнопка для открытия модального окна -->
      <div
        class="text-2xl rounded-xl mt-5 cursor-pointer bg-blue-500 text-white p-3"
        @click="openModal"
      >
        Открыть модальное окно
      </div>
    </div>

    
  </div>
</template>

<style scoped>
.success-popup {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
}
</style>
