<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref, reactive, watch } from 'vue'
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
const role = computed(() => localStorage.getItem('role'))
const selectedAchievement = ref(null)
const meas_unit = ref('')
const verif_doc_info = ref('')
//Для модального окна документом
const inputed_meas_unit_val = ref('')
const inputed_name = ref('')
const inputed_ver_link = ref('')
const inputed_doc_ver_link = ref('')
const isModalOpen = ref(false)
//Для модального статейного окна
const pubTypes = ref([])
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
// Выборы типа, грифа, уровня
const selectedPubType = ref(null)
const selectedPubGrief = ref(null)
const selectedPubLevel = ref(null)

const isPub = ref('')
const hasPublication = ref('')
const hasConference = ref('')

// Шапка и размеры таблицы
const tableHeads = [
  { key: 'id', label: '№' },
  { key: 'name', label: 'Наименование показателя' },
  { key: 'score', label: 'Балл' }
]
const tableSizeColumns = '1fr 8fr 2fr'
const searchQuery = ref('')
const sortBy = reactive({
  column: 'number',
  order: 'asc'
})

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
    const response = await axios.get('http://127.0.0.1:8000/profile/', {
      headers: {
        Authorization: `Token ${token.value}`
      }
    })

    userData.value = response.data
    teacherId.value = userData.value.employee // Установите teacherId из userData
    localStorage.setItem('role', userData.value.role)
    localStorage.setItem('department', userData.value.department)
    localStorage.setItem('email', userData.value.email)
    localStorage.setItem('current_id', userData.value.employee)
    role.value = localStorage.role
    userName.value = userData.value.last_name
    userDepatment.value = userData.value.department

    const achievementsResponse = await axios.get(
      `http://127.0.0.1:8000/api/v1/employe_achievments/employee/${teacherId.value}`
    )
    // Сортируем данные по полю number по возрастанию
    achivmentsData.value = achievementsResponse.data.achievements.sort(
      (a, b) => a.number - b.number
    )

    const AllAchResp = await axios.get('http://127.0.0.1:8000/api/v1/achievments/')
    allAchData.value = AllAchResp.data.filter((item) => item.meas_unit_score !== 0)
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}

const addAchievement = async () => {
  try {
    const oneAch = await axios.get(
      `http://127.0.0.1:8000/api/v1/achievments/${selectedAchievement.value}`
    )
    const data = new FormData()
    data.append('employee', userData.value.employee)
    data.append('achievment', selectedAchievement.value)
    data.append('meas_unit_val', inputed_meas_unit_val.value)
    data.append('verif_doc', inputed_doc_ver_link.value)
    data.append('verif_link', inputed_ver_link.value)
    data.append('full_achivment_name', inputed_name.value)
    data.append('score', inputed_meas_unit_val.value * oneAch.data.meas_unit_score)
    data.append('reciving_date', new Date().toISOString().split('T')[0])
    // Внешние ключи
    data.append('pub_type', selectedPubType.value)
    data.append('pub_grief', selectedPubGrief.value)
    data.append('pub_level', selectedPubLevel.value)
    //остальные поля
    data.append('language_pub', inputed_language_pub.value)
    data.append('doi', inputed_doi.value)
    data.append('empl_authors', inputed_empl_authors.value)
    data.append('stud_authors', inputed_stud_authors.value)
    data.append('out_authors', inputed_out_authors.value)
    data.append('bibliographic', inputed_bibliographic.value)
    data.append('publication_name', inputed_publication_name.value)
    data.append('publicator', inputed_publicator.value)
    // Добавляем publication_date только если она не пустая
    if (inputed_publication_date.value) {
      data.append(
        'publication_date',
        new Date(inputed_publication_date.value).toISOString().split('T')[0]
      )
    }
    data.append('yearVolNum', inputed_yearVolNum.value)
    data.append('conference_status', inputed_conference_status.value)
    // Добавляем conference_date только если она не пустая
    if (inputed_conference_date.value) {
      data.append(
        'conference_date',
        new Date(inputed_conference_date.value).toISOString().split('T')[0]
      )
    }
    data.append('conference_name', inputed_conference_name.value)

    const response = await axios.post('http://127.0.0.1:8000/api/v1/employee_achievment/', data, {
      headers: {
        Authorization: `Token ${token.value}`,
        'Content-Type': 'multipart/form-data' // Указываем, что отправляем FormData
      }
    })

    getUserData()
    console.log('Achievement added successfully:', response.data)

    selectedAchievement.value = null

    successMessage.value = 'Успешно добавлено достижение!'
    errorMessage.value = ''

    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
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
  } catch (error) {
    console.error('Ошибка при добавлении достижения:', error)
    errorMessage.value = 'Ошибка при добавлении достижения!'
    successMessage.value = ''

    setTimeout(() => {
      errorMessage.value = ''
    }, 3000)
  }
}

const closeModal = () => {
  isModalOpen.value = false
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
  await fetchPubTypes()
  await fetchPubGriefs()
})

const setLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('department')
  localStorage.removeItem('logout')
  localStorage.removeItem('current_id')
  window.location.href = '/login'
}

const downloadReport = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/generate_personal_report/?teacher_id=${teacherId.value}`, // Передаем teacherId в запросе
      {
        responseType: 'blob' // Указываем, что ожидаем бинарный файл
      }
    )

    // Создание объекта URL для скачивания
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)

    // Устанавливаем имя файла
    const filename =
      response.headers['content-disposition']?.split('filename=')[1]?.replace(/"/g, '') ||
      'Приложение№4_Сотрудник.xlsx'
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

const onAchievementChange = async () => {
  selectedPubGrief.value = ''
  selectedPubLevel.value = ''
  selectedPubType.value = ''
  if (selectedAchievement.value) {
    try {
      const achievement = allAchData.value.find((ach) => ach.id === selectedAchievement.value)

      if (achievement) {
        meas_unit.value = achievement.meas_unit || ''
        verif_doc_info.value = achievement.verif_doc_info || ''
        isPub.value = achievement.is_pub || false
        hasPublication.value = achievement.is_pub || false
        hasConference.value = achievement.is_pub || false
      }
    } catch (error) {
      console.error('Ошибка при подстановке данных для достижения', error)
    }
  }
}

// Слежение за изменениями в selectedAchievement
watch(selectedAchievement, onAchievementChange)

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    inputed_doc_ver_link.value = file
  }
}


</script>

<template>
  <div class="h-full">
    <headerBlock>
      <div class="grid grid-cols-1">
        <!-- <div
          class="ml-4 flex justify-center items-center text-black bg-white text-2xl p-4 text-center font-sm cursor-pointer bg-blue-900 rounded-2xl shadow-2xl"
        >
          {{ userName }}
        </div> -->
        <div
          class="ml-4 flex justify-end items-end text-black p-4 text-end font-sm transition hover:scale-105 cursor-pointer"
          @click="setLogout()"
        >
          <img src="../assets/kost.png" alt="Логотип" class="h-20 w-auto" />
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
      <div
        v-if="['ADMIN', 'ZAV', 'OTV'].includes(role)"
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
            class="cursor-pointer font-sm text-white"
          >
            {{ head.label }}
          </TableColumn>
        </TableRow>

        <template #body>
          <TableRow
            v-for="(achievement, index) in sortedAchievements"
            :key="achievement.id"
            :columnTemplates="tableSizeColumns"
          >
            <TableColumn>{{ achievement.number }}</TableColumn>
            <TableColumn v-if="achievement.meas_unit_score !== 0" class="cursor-pointer">
              <router-link
                :to="{
                  name: 'achievmentDetailed',
                  params: { ach_id: achievement.id, empl_id: teacherId }
                }"
              >
                {{ achievement.achievment_name }}
              </router-link>
            </TableColumn>
            <TableColumn v-else>
              {{ achievement.achievment_name }}
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

          <!-- Выбор достижения -->
          <select v-model="selectedAchievement" class="text-2xl mt-3 p-2 rounded-xl w-full">
            <option v-for="achievement in allAchData" :key="achievement.id" :value="achievement.id">
              {{ achievement.number }} {{ achievement.name }}
            </option>
          </select>

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
                  v-model="meas_unit"
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
              readonly
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
                    v-model="meas_unit"
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
      <!-- Конец модального окна -->
    </div>
  </div>
</template>
