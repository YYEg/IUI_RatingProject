<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive } from 'vue'
import axios from 'axios'

const achivmentsData = ref([])
const allAchData = ref([])
const userData = ref(null) // Данные пользователя
const teacherId = ref(null) // ID преподавателя из данных пользователя
const userName = ref(null)
const successMessage = ref('')
const errorMessage = ref('')
const userDepatment = ref(null)
const token = ref(localStorage.getItem('token') || '')
const selectedAchievement = ref(null)
const inputed_meas_unit_val = ref('')
const isModalOpen = ref(false)

// Шапка и размеры таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Достижение' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 8fr 2fr'
const searchQuery = ref('')
const sortBy = reactive({
  column: 'score',
  order: 'desc'
})

// Получение данных пользователя
const getUserData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/profile/', {
      headers: {
        Authorization: `Token ${token.value}` // Убедитесь, что токен определён
      }
    })
    userData.value = response.data
    teacherId.value = userData.value.employee // Установите teacherId из userData
    console.log(teacherId.value)
    userName.value = userData.value.last_name
    userDepatment.value = userData.value.department

    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/v1/employe_achievments/employee/${teacherId.value}`
    )
    achivmentsData.value = achievementsResponse.data.achievements
    console.log(achievementsResponse.data)

    const AllAchResp = await axios.get('http://127.0.0.1:8000/api/v1/achievments/')
    allAchData.value = AllAchResp.data
    console.log(allAchData.value)
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}

const addAchievement = async () => {
  try {
    const data = {
      employee: userData.value.employee,
      achievment: selectedAchievement.value,
      meas_unit_val: inputed_meas_unit_val.value,
      verif_doc: 'Cсылка',
      score: inputed_meas_unit_val.value * 2
    }
    console.log(data)
    const response = await axios.post('http://127.0.0.1:8000/api/v1/employee_achievment/', data, {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })

    getUserData()

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
    successMessage.value = ''

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

const downloadReport = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/generate_report/', {
      responseType: 'blob' // Указываем, что ожидаем бинарный файл
    })

    // Создание объекта URL для скачивания
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)

    // Устанавливаем имя файла
    const filename =
      response.headers['content-disposition']?.split('filename=')[1]?.replace(/"/g, '') ||
      'ОТЧЕТ_ПО_КАФЕДРЕ.xlsx'
    link.download = filename

    // Инициируем скачивание
    link.click()
    URL.revokeObjectURL(link.href)
  } catch (error) {
    console.error('Ошибка при скачивании отчета:', error)
  }
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

// Вычисляемый список с фильтрацией и сортировкой
const filteredDepartmentData = computed(() => {
  return departmentData.value.filter((department) =>
    department.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

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
  <div class="h-full">
    <headerBlock>
      <div class="grid grid-cols-2">
        <div
          class="ml-4 flex justify-center items-center text-black bg-white text-2xl p-4 text-center font-sm cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
        >
          {{ userName }}
        </div>
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
      <div
        class="flex justify-center items-center bg-white text-xl text-black p-2 m-2 text-center font-sm transition hover:scale-105 cursor-pointer rounded-2xl shadow-2xl border-2 border-slate-400"
        @click="openModal"
      >
        Добавить достижение
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
            <TableColumn>{{ achievement.number }}</TableColumn>
            <TableColumn class="cursor-pointer">
              <router-link
                :to="{
                  name: 'achievmentDetailed',
                  params: { ach_id: achievement.id, empl_id: teacherId }
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

      <!-- Модальное окно -->
      <div
        v-if="isModalOpen"
        class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50"
      >
        <div class="bg-white p-5 rounded-lg shadow-lg max-w-lg w-full">
          <div class="flex justify-between items-center">
            <h2 class="text-3xl font-sm text-gray-800">Добавить достижение</h2>
            <button @click="closeModal" class="text-4xl text-red-500">×</button>
          </div>

          <select v-model="selectedAchievement" class="text-2xl mt-3 p-2 rounded-xl w-full">
            <option v-for="achievement in allAchData" :key="achievement.id" :value="achievement.id">
              {{ achievement.name }}
            </option>
          </select>

          <input v-model="inputed_meas_unit_val" placeholder="Единица измерения..." />

          <div
            class="w-full mt-2 shadow-2xl text-center text-2xl font-bold transition hover:scale-105 cursor-pointer p-2 rounded-2xl border-2 border-black"
            @click="addAchievement()"
          >
            Добавить
          </div>

          <!-- Сообщение об успехе -->
          <transition name="fade">
            <div v-if="successMessage" class="success-popup text-3xl font-bold text-green-400">
              {{ successMessage }}
            </div>
          </transition>

          <!-- Сообщение об ошибке -->
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
