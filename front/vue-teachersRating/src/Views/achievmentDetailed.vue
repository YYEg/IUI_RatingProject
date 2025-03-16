<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const emplAch = ref([])
const JustAch = ref([])
const selectedAchievement = ref(null)
const achivmentsData = ref([])
const isDeleting = ref(false)
const isSending = ref(false)
const isMesModalOpen = ref('')
const deletedAchForMail = ref([])
const employeeData = ref([])
const token = ref(localStorage.getItem('token') || '')
const route = useRoute()
const currentUser = ref(localStorage.getItem('current_id') || '')
const searchQuery = ref('')
const role = ref(localStorage.getItem('role') || '')
const successMessage = ref('')
const errorMessage = ref('')
const verif_doc_info = ref('')
const sortBy = reactive({
  column: 'number',
  order: 'desc'
})
const isModalOpen = ref(false) // Состояние модального окна
const DelReason = ref('') // Причина удаления
const selectedAchievementId = ref(null) // ID выбранного достижения для удаления

// Шапка и размеры таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Достижение' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 5fr 2fr 2fr'

const isEditModalOpen = ref(false)
//Для модального окна документом
const inputed_meas_unit_val = ref('')
const inputed_name = ref('')
const inputed_ver_link = ref('')
const inputed_doc_ver_link = ref('')
//Для модального статейного окна
const pubTypes = ref([])
const achMeas = ref([])
const achName = ref([])
const pubGriefs = ref([])
const pubLevels = ref([])
const inputed_language_pub = ref('')
const inputed_doi = ref('')
const inputed_empl_authors = ref('')
const inputed_stud_authors = ref('')
const inputed_out_authors = ref('')
const inputed_bibliographic = ref('')
const inputed_publication_name = ref('')
const inputed_publicator = ref('')
const inputed_publication_date = ref('')
const inputed_yearVolNum = ref('')
const inputed_conference_status = ref('')
const inputed_conference_date = ref('')
const inputed_conference_name = ref('')
const currentAchievementId = ref('')
// Выборы типа, грифа, уровня
const selectedPubType = ref(null)
const selectedPubGrief = ref(null)
const selectedPubLevel = ref(null)

const isPub = ref('')
const hasPublication = ref('')
const hasConference = ref('')

const closeEditModal = () => {
  isEditModalOpen.value = false
  inputed_meas_unit_val.value = ''
  inputed_name.value = ''
  inputed_ver_link.value = ''
  inputed_doc_ver_link.value = null // Для файла лучше использовать null

  // Для модального статейного окна
  pubTypes.value = []
  pubGriefs.value = []
  pubLevels.value = []
  inputed_language_pub.value = ''
  inputed_doi.value = ''
  inputed_empl_authors.value = ''
  inputed_stud_authors.value = ''
  inputed_out_authors.value = ''
  inputed_bibliographic.value = ''
  inputed_publication_name.value = ''
  inputed_publicator.value = ''
  inputed_publication_date.value = ''
  inputed_yearVolNum.value = ''
  inputed_conference_status.value = ''
  inputed_conference_date.value = ''
  inputed_conference_name.value = ''

  // Сброс выбранных значений для типа, грифа и уровня
  selectedPubType.value = null
  selectedPubGrief.value = null
  selectedPubLevel.value = null
}

const openEditModal = () => {
  isEditModalOpen.value = true
}

const fetchPubTypes = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/pub_types/')
    pubTypes.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке типов публикаций:', error)
  }
}

const fetchPubGriefs = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/pub_griefs/')
    pubGriefs.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке грифов публикаций:', error)
  }
}

const fetchPubLevels = async (griefId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/pub_levels/?grief_id=${griefId}`)
    pubLevels.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке уровней публикаций:', error)
  }
}

// Получение данных пользователя
const getUserData = async () => {
  try {
    console.log(route.params.ach_id)
    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/employee/${route.params.empl_id}/achievement/${route.params.ach_id}/achievements/`
    )
    console.log(currentUser.value, route.params.empl_id)
    achivmentsData.value = achievementsResponse.data.achievements
    console.log(achivmentsData.value)
  } catch (error) {
    console.error('Проблема с получением данных пользователя:', error)
  }
}

const openDeleteModal = (achievementId) => {
  selectedAchievementId.value = achievementId // Сохраняем ID достижения
  isModalOpen.value = true // Открываем модальное окно
}

const closeModal = () => {
  isModalOpen.value = false // Закрываем модальное окно
  DelReason.value = '' // Очищаем причину удаления
}

const openMessageModal = (achievementId) => {
  selectedAchievementId.value = achievementId // Сохраняем ID достижения
  isMesModalOpen.value = true // Открываем модальное окно
}

const closeMessageModal = () => {
  isMesModalOpen.value = false // Закрываем модальное окно
  DelReason.value = '' // Очищаем причину удаления
}

const deleteAchievement = async () => {
  isDeleting.value = true
  try {
    const response = await axios.delete(
      `http://127.0.0.1:8000/api/v1/delete_employee_achievement/${selectedAchievementId.value}/`,
      {
        headers: { Authorization: `Token ${token.value}` },
        data: { email: employeeData.value.email, reason: DelReason.value } // Добавляем email и причину удаления в тело запроса
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
    closeModal() // Закрываем модальное окно после удаления
  }
}

const sendUpdateMessage = async () => {
  isSending.value = true
  try {
    console.log(employeeData.value.email)
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/update_message/${selectedAchievementId.value}/`,
      {
        headers: { Authorization: `Token ${token.value}` },
        params: { email: employeeData.value.email, reason: DelReason.value } // Передаем параметры в URL
      }
    )

    console.log('Сообщение отправлено:', response.data)
  } catch (error) {
    console.error('Ошибка удаления достижения:', error)
  } finally {
    isSending.value = false
    closeMessageModal()
  }
}



onMounted(async () => {
  if (!token.value) {
    window.location.href = '/login'
    return
  }
  getUserData()
  try {
    const employeeResponse = await axios.get(
      `http://127.0.0.1:8000/api/v1/employees/${route.params.empl_id}/`
    )
    employeeData.value = employeeResponse.data
  } catch (error) {
    console.error('Данные сотрудника получить не удалось:', error)
  }
  await fetchPubTypes()
  await fetchPubGriefs()
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

    if (response.status === 200) {
      const contentDisposition = response.headers['content-disposition']
      const contentType = response.headers['content-type']
      const fileName = contentDisposition
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : `document_${achievementRecordId}`

      const blob = new Blob([response.data], { type: contentType })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = fileName
      document.body.appendChild(link)
      link.click()
      URL.revokeObjectURL(url)
      document.body.removeChild(link)
    } else {
      throw new Error('Ошибка при получении документа')
    }
  } catch (error) {
    console.error('Ошибка при скачивании документа:', error)
  }
}

const editAchievement = async (achievementId) => {
  try {
    // Получаем данные достижения по ID
    const response = await axios.get(`http://127.0.0.1:8000/employee_achievments/${achievementId}/`)
    emplAch.value = response.data

    // Заполняем поля модального окна
    selectedAchievement.value = emplAch.value.id
    inputed_meas_unit_val.value = emplAch.value.meas_unit_val
    inputed_name.value = emplAch.value.full_achivment_name
    inputed_ver_link.value = emplAch.value.verif_link
    selectedPubType.value = emplAch.value.pub_type || null
    selectedPubGrief.value = emplAch.value.pub_grief || null
    await fetchPubLevels(emplAch.value.pub_grief)
    await fetchPubGriefs()
    await fetchPubTypes()
    selectedPubLevel.value = emplAch.value.pub_level || null
    inputed_language_pub.value = emplAch.value.pub_language
    inputed_doi.value = emplAch.value.pub_doi
    inputed_empl_authors.value = emplAch.value.pub_authors_employees
    inputed_stud_authors.value = emplAch.value.pub_authors_students
    inputed_out_authors.value = emplAch.value.pub_out_authors
    inputed_bibliographic.value = emplAch.value.bibliographic_desc
    inputed_publication_name.value = emplAch.value.publication_name
    inputed_publicator.value = emplAch.value.publicator
    inputed_publication_date.value = emplAch.value.publication_data
    inputed_yearVolNum.value = emplAch.value.publication_year_vol_num
    inputed_conference_status.value = emplAch.value.conference_status
    inputed_conference_date.value = emplAch.value.conference_date
    inputed_conference_name.value = emplAch.value.conference_name
    console.log(emplAch.value)
    const achAch = await axios.get(
      `http://127.0.0.1:8000/api/v1/achievments/${emplAch.value.achievment}`
    )
    JustAch.value = achAch.data
    // Подгружаем дополнительные данные, такие как isPub
    achName.value = JustAch.value.name
    achMeas.value = JustAch.value.meas_unit
    isPub.value = JustAch.value.is_pub || false
    hasPublication.value = JustAch.value.has_publication || false
    hasConference.value = JustAch.value.has_conference || false
    verif_doc_info.value = JustAch.value.verif_doc_info

    // Открываем модальное окно
    isEditModalOpen.value = true

    // Сохраняем ID достижения для обновления
    currentAchievementId.value = emplAch.value.achievment
  } catch (error) {
    console.error('Ошибка при получении данных достижения:', error)
  }
}

const saveAchievement = async () => {
  try {
    const data = new FormData()
    data.append('achievment', selectedAchievement.value)
    data.append('meas_unit_val', inputed_meas_unit_val.value)
    data.append('verif_link', inputed_ver_link.value)
    data.append('full_achivment_name', inputed_name.value)
    data.append('pub_type', selectedPubType.value)
    data.append('pub_grief', selectedPubGrief.value)
    data.append('pub_level', selectedPubLevel.value)
    data.append('language_pub', inputed_language_pub.value)
    data.append('doi', inputed_doi.value)
    data.append('empl_authors', inputed_empl_authors.value)
    data.append('stud_authors', inputed_stud_authors.value)
    data.append('out_authors', inputed_out_authors.value)
    data.append('bibliographic', inputed_bibliographic.value)
    data.append('publication_name', inputed_publication_name.value)
    data.append('publicator', inputed_publicator.value)
    data.append('publication_date', inputed_publication_date.value)
    data.append('yearVolNum', inputed_yearVolNum.value)
    data.append('conference_status', inputed_conference_status.value)
    data.append('conference_date', inputed_conference_date.value)
    data.append('conference_name', inputed_conference_name.value)

    if (inputed_doc_ver_link.value) {
      data.append('verif_doc', inputed_doc_ver_link.value)
    }

    let response
    if (currentAchievementId.value) {
      // Если есть ID, отправляем PUT-запрос на обновление
      response = await axios.put(
        `http://127.0.0.1:8000/employee_achievments/update/${selectedAchievement.value}/`,
        data,
        {
          headers: {
            Authorization: `Token ${token.value}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      )
    } else {
      // Иначе отправляем POST-запрос на добавление
      response = await axios.post('http://127.0.0.1:8000/api/v1/employee_achievments/', data, {
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    getUserData()
    console.log('Достижение успешно сохранено:', response.data)

    successMessage.value = 'Достижение успешно сохранено!'
    errorMessage.value = ''

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)

    // Закрываем модальное окно и сбрасываем данные
    closeEditModal()
  } catch (error) {
    console.error('Ошибка при сохранении достижения:', error)
    errorMessage.value = 'Ошибка при сохранении достижения!'
    successMessage.value = ''

    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}
</script>

<template>
  <div class="h-full">
    <headerBlock>
      <div class="flex justify-end">
        <div
          class="flex justify-end w-content p-4 transition hover:scale-105 cursor-pointer"
          @click="() => $router.push('/profile')"
        >
          <img src="../assets/vvv.png" alt="Логотип" class="h-20 w-auto" />
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
              <div class="row flex justify-center" style="display: flex; gap: 8px">
                <img
                  v-if="
                    route.params.empl_id === currentUser || ['ADMIN', 'ZAV', 'OTV'].includes(role)
                  "
                  src="../assets/delete.png"
                  alt="Логотип"
                  @click="openDeleteModal(achievement.id)"
                  style="cursor: pointer; width: 24px; height: 24px"
                />
                <img
                  v-if="achievement.verif_doc != null"
                  @click="downloadDocument(achievement.id)"
                  src="../assets/downl.png"
                  alt="Логотип"
                  style="cursor: pointer; width: 24px; height: 24px"
                />
                <img
                  v-if="
                    route.params.empl_id === currentUser || ['ADMIN', 'ZAV', 'OTV'].includes(role)
                  "
                  @click="editAchievement(achievement.id)"
                  src="../assets/карандаш.png"
                  alt="Логотип"
                  style="cursor: pointer; width: 24px; height: 24px"
                />
                <img
                  v-if="
                    route.params.empl_id === currentUser || ['ADMIN', 'ZAV', 'OTV'].includes(role)
                  "
                  @click="openMessageModal(achievement.id)"
                  src="../assets/mes.png"
                  alt="Логотип"
                  style="cursor: pointer; width: 24px; height: 24px"
                />
              </div>
            </TableColumn>
          </TableRow>
        </template>
      </BaseTable>

      <div class="text-center text-2xl font-bold mt-4">Итого баллов: {{ totalScore }}</div>
    </div>

    <!-- Модальное окно для удаления -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50"
    >
      <div class="bg-white p-5 rounded-lg shadow-lg max-w-lg w-full">
        <div class="flex justify-between items-center">
          <h2 class="text-3xl font-sm text-gray-800">Удаление достижения</h2>
          <button @click="closeModal" class="text-4xl text-red-500">×</button>
        </div>

        <div class="mt-4">
          <label for="reason" class="block text-sm font-medium text-gray-700"
            >Причина удаления:</label
          >
          <textarea
            id="reason"
            v-model="DelReason"
            class="mt-1 p-2 w-full border border-gray-300 rounded-md"
            rows="4"
            placeholder="Введите причину удаления..."
          ></textarea>
        </div>

        <div class="mt-4 flex justify-end">
          <button
            @click="deleteAchievement"
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
        </div>
      </div>
    </div>

    <!-- Модальное окно для уведомления -->
    <div
      v-if="isMesModalOpen"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50"
    >
      <div class="bg-white p-5 rounded-lg shadow-lg max-w-lg w-full">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-sm text-gray-800">Уведомление пользователя о необходимости корректировки</h2>
          <button @click="closeMessageModal" class="text-4xl text-red-500">×</button>
        </div>

        <div class="mt-4">
          <label for="reason" class="block text-sm font-medium text-gray-700"
            >Причина корректировки:</label
          >
          <textarea
            id="reason"
            v-model="DelReason"
            class="mt-1 p-2 w-full border border-gray-300 rounded-md"
            rows="4"
            placeholder="Введите причины обновления..."
          ></textarea>
        </div>

        <div class="mt-4 flex justify-end">
          <button
            @click="sendUpdateMessage"
            class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
            :disabled="isSending"
          >
            <span v-if="isSending">
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
            <span v-else>Отправить</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно -->
    <div
      v-if="isEditModalOpen"
      class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50"
    >
      <div class="bg-white p-5 rounded-lg shadow-lg max-w-lg w-full">
        <div class="flex justify-between items-center">
          <h2 class="text-3xl font-sm text-gray-800">Изменить достижение</h2>
          <button @click="closeEditModal" class="text-4xl text-red-500">×</button>
        </div>

        <!-- Выбор достижения -->
        <input
          class="text-l mt-3 p-2 rounded-xl w-full"
          v-model="achName"
          placeholder="Полное наименование..."
          readonly
        />

        <!-- Подтверждение документом -->
        <div v-if="!isPub">
          <div class="mt-4">
            <label for="reason" class="block text-sm font-medium text-gray-700"
              >Информация о подтверждающем документе:</label
            >
            <textarea
              class="mt-1 p-2 w-full border border-gray-300 rounded-md"
              rows="2"
              placeholder="Информация о подтверждающем документе"
              readonly
              v-model="verif_doc_info"
            ></textarea>
          </div>

          <input
            class="text-l mt-3 p-2 rounded-xl w-full"
            v-model="inputed_name"
            placeholder="Полное наименование..."
          />

          <div class="grid grid-cols-2">
            <div>
              <!-- Подставленный mes_unit -->

              <input
                class="text-l text-right mt-3 p-2 rounded-xl w-full"
                v-model="achMeas"
                placeholder="Единица измерения..."
                readonly
              />
            </div>
            <div>
              <!-- mes_unit_val -->
              <input
                class="text-l mt-3 p-2 rounded-xl w-full"
                v-model="inputed_meas_unit_val"
                placeholder="Значение единицы измерения..."
              />
            </div>
          </div>
          <input
            class="text-l mt-3 p-2 rounded-xl w-full"
            v-model="inputed_ver_link"
            placeholder="Ссылка для подтверждения..."
          />

          <input
            type="file"
            class="text-l mt-3 p-2 rounded-xl w-full"
            @change="handleFileUpload"
            accept=".pdf,.docx,.jpg,.png"
            ref="fileInput"
          />
        </div>

        <!-- Статейное подтверждение -->
        <div v-if="isPub">
          <!-- Информация 1й уровень -->
          <div class="flex grid grid-cols-3">
            <div>
              <!-- Выбор типа публикации -->
              <select v-model="selectedPubType" class="text-2xl mt-3 p-2 rounded-xl w-full">
                <option v-for="pubType in pubTypes" :key="pubType.id" :value="pubType.id">
                  {{ pubType.name }}
                </option>
              </select>
            </div>

            <div>
              <!-- Выбор грифа публикации -->
              <select
                v-model="selectedPubGrief"
                @change="fetchPubLevels(selectedPubGrief)"
                class="text-2xl mt-3 p-2 rounded-xl w-full"
              >
                <option v-for="grief in pubGriefs" :key="grief.id" :value="grief.id">
                  {{ grief.name }}
                </option>
              </select>
            </div>

            <div>
              <!-- Выбор уровня публикации (если есть уровни) -->
              <select
                v-if="selectedPubGrief && pubLevels.length > 0"
                v-model="selectedPubLevel"
                class="text-2xl mt-3 p-2 rounded-xl w-full"
              >
                <option v-for="level in pubLevels" :key="level.id" :value="level.id">
                  {{ level.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="flex grid grid-cols-3">
            <div>
              <!-- Язык -->
              <input
                class="text-l mt-3 p-2 rounded-xl w-full"
                v-model="inputed_language_pub"
                placeholder="Язык оригинала..."
              />
            </div>
            <div>
              <!-- Наименование -->
              <input
                class="text-l mt-3 p-2 rounded-xl w-full"
                v-model="inputed_name"
                placeholder="Наименование..."
              />
            </div>
            <div>
              <!-- DOI -->
              <input
                class="text-l mt-3 p-2 rounded-xl w-full"
                v-model="inputed_doi"
                placeholder="DOI"
              />
            </div>
          </div>

          <!-- Информация 2й уровень авторы -->
          <input
            class="text-l mt-3 p-2 rounded-xl w-full"
            v-model="inputed_empl_authors"
            placeholder="Авторы сотрудники..."
          />
          <input
            class="text-l mt-3 p-2 rounded-xl w-full"
            v-model="inputed_stud_authors"
            placeholder="Авторы студенты..."
          />
          <input
            class="text-l mt-3 p-2 rounded-xl w-full"
            v-model="inputed_out_authors"
            placeholder="Внешние авторы..."
          />
          <textarea
            class="mt-1 p-2 w-full border border-gray-300 rounded-md"
            rows="2"
            placeholder="Библиографическое описание..."
            v-model="inputed_bibliographic"
          ></textarea>

          <!-- Информация 3й уровень данные об издании -->
          <div v-if="hasPublication">
            <div class="text-xl mt-2 text-center rounded-xl w-full">Данные об издании:</div>
            <input
              class="text-l mt-3 p-2 rounded-xl w-full"
              v-model="inputed_publication_name"
              placeholder="Наименование издания..."
            />
            <div class="flex grid grid-cols-3">
              <div>
                <!-- Издатель -->
                <input
                  class="text-l mt-3 p-2 rounded-xl w-full"
                  v-model="inputed_publicator"
                  placeholder="Издатель..."
                />
              </div>
              <div>
                <!-- Дата -->
                <input
                  class="text-l mt-3 p-2 rounded-xl w-full"
                  type="date"
                  v-model="inputed_publication_date"
                  placeholder="Дата печати/публикации..."
                />
              </div>
              <div>
                <!-- Год,том,номер издания -->
                <input
                  class="text-l mt-3 p-2 rounded-xl w-full"
                  v-model="inputed_yearVolNum"
                  placeholder="Год,том,номер издания..."
                />
              </div>
            </div>

            <input
              class="text-l mt-3 p-2 rounded-xl w-full"
              v-model="inputed_ver_link"
              placeholder="Ссылка для подтверждения..."
            />
            <div class="text-l mt-1 rounded-xl w-full">Загрузка текста статьи:</div>
            <input
              type="file"
              class="text-l mt-1 p-2 rounded-xl w-full"
              @change="handleFileUpload"
              accept=".pdf,.docx,.jpg,.png,.xls,.zip"
              ref="fileInput2"
            />
          </div>

          <!-- Уровень 4 Инофрмация о конференции -->
          <div v-if="hasConference">
            <div class="text-xl mt-2 text-center rounded-xl w-full">Данные об конференции:</div>
            <div class="grid grid-cols-2">
              <div>
                <!-- Статус конференции -->
                <input
                  class="text-l mt-3 p-2 rounded-xl w-full"
                  v-model="inputed_conference_status"
                  placeholder="Статус конференции..."
                />
              </div>
              <div>
                <!-- Дата конференции -->
                <div>
                  <input
                    class="text-l mt-3 p-2 rounded-xl w-full"
                    type="date"
                    v-model="inputed_conference_date"
                    placeholder="Дата печати/публикации..."
                  />
                </div>
              </div>
            </div>
            <!-- Полное наименование конференции -->
            <input
              class="text-l mt-3 p-2 rounded-xl w-full"
              v-model="inputed_conference_name"
              placeholder="Полное наименование конференции..."
            />
            <div class="grid grid-cols-2">
              <div>
                <!-- Подставленный mes_unit -->

                <input
                  class="text-l text-right mt-3 p-2 rounded-xl w-full"
                  v-model="achMeas"
                  placeholder="Единица измерения..."
                  readonly
                />
              </div>
              <div>
                <!-- mes_unit_val -->
                <input
                  class="text-l mt-3 p-2 rounded-xl w-full"
                  v-model="inputed_meas_unit_val"
                  placeholder="Значение единицы измерения..."
                />
              </div>
            </div>
          </div>
        </div>

        <div
          class="w-full mt-2 shadow-2xl text-center text-xl transition hover:scale-105 cursor-pointer p-2 rounded-2xl border-2 border-black"
          @click="saveAchievement()"
        >
          Изменить
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
    <!-- Конец модального окна -->
  </div>
</template>
