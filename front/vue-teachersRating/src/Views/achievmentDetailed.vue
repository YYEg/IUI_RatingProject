<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const achivmentsData = ref([])
const isDeleting = ref(false)
const deletedAchForMail = ref([])
const employeeData = ref([])
const token = ref(localStorage.getItem('token') || '')
const route = useRoute()
const searchQuery = ref('')
const sortBy = reactive({
  column: 'score',
  order: 'desc'
})

// Шапка и размеры таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Достижение' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 5fr 2fr 2fr 2fr 2fr'

// Получение данных пользователя
const getUserData = async () => {
  try {
    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/employee/${route.params.empl_id}/achievement/${route.params.ach_id}/achievements/`
    )
    achivmentsData.value = achievementsResponse.data.achievements
    console.log(achivmentsData.value)
  } catch (error) {
    console.error('Проблема с получением данных пользователя:', error)
  }
}

const deleteAchievement = async (achievementId) => {
  isDeleting.value = true
  try {
    console.log(achievementId)
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/v1/delete_employee_achievement/${achievementId}/`,
      {
        headers: { Authorization: `Token ${token.value}` },
        data: { email: employeeData.value.email } // Добавляем email в тело запроса
      }
    )

    console.log('Достижение успешно удалено:', response.data)
    deletedAchForMail.value = response.data

    try {
      // Обновляем список достижений после удаления
      const achievementsResponse = await axios.get(
        `http://127.0.0.1:8000/api/employee/${route.params.empl_id}/achievement/${route.params.ach_id}/achievements/`
      )
      achivmentsData.value = achievementsResponse.data.achievements
    } catch (error) {
      achivmentsData.value = []
    }
  } catch (error) {
    console.error('Ошибка удаления достижения:', error)
  } finally {
    isDeleting.value = false
  }
}

onMounted(async () => {
  if (!token.value) {
    window.location.href = '/login'
    return
  }
  getUserData()
  try{
    const employeeResponse = await axios.get(
          `http://127.0.0.1:8000/api/v1/employees/${route.params.empl_id}/`
        )
        employeeData.value = employeeResponse.data
  } catch {
    console.error('Данные сотрудника получить не удалось:', error)
}

})

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

const downloadDocument = async (achievementRecordId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/download/${achievementRecordId}/`, {
      headers: {
        Authorization: `Token ${token.value}`
      },
      responseType: 'blob'
    })

    // Проверка на успешный ответ (200 OK)
    if (response.status === 200) {
      const contentDisposition = response.headers['content-disposition']
      const contentType = response.headers['content-type']
      const fileName = contentDisposition
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : `document_${achievementRecordId}`

      // Создаем объект Blob из полученных данных
      const blob = new Blob([response.data], { type: contentType })

      // Создаем ссылку для скачивания файла
      const url = URL.createObjectURL(blob)

      // Создаем ссылку для скачивания и программно "кликаем" по ней
      const link = document.createElement('a')
      link.href = url
      link.download = fileName // Используем имя файла из content-disposition или генерируем собственное
      document.body.appendChild(link)
      link.click()

      // Очищаем память от созданного объекта URL
      URL.revokeObjectURL(url)
      document.body.removeChild(link)
    } else {
      throw new Error('Ошибка при получении документа')
    }
  } catch (error) {
    console.error('Ошибка при скачивании документа:', error)
  }
}
</script>

<template>
  <div class="h-full">
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
            <TableColumn>
              <button
                @click="deleteAchievement(achievement.id)"
                class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
                :disabled="isDeleting"
              >
                <span v-if="isDeleting">
                  <svg
                    class="animate-spin h-4 w-4 inline-block"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                </span>
                <span v-else>Удалить</span>
              </button>
            </TableColumn>
            <TableColumn>
              <button
                v-if="achievement.verif_doc != null"
                @click="downloadDocument(achievement.id)"
                class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
              >
                Скачать документ
              </button>
            </TableColumn>
            <TableColumn>
              {{ achievement.verif_link }}
            </TableColumn>
          </TableRow>
        </template>
      </BaseTable>

      <div class="text-center text-2xl font-bold mt-4">Итого баллов: {{ totalScore }}</div>
    </div>
  </div>
</template>
