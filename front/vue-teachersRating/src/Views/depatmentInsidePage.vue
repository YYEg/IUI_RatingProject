<script setup>
import headerBlock from '../components/headerBlock.vue'
import BaseTable from '@/components/Table/BaseTable.vue'
import TableRow from '@/components/Table/TableRow.vue'
import TableColumn from '@/components/Table/TableColumn.vue'
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const tableHeads = ['№', 'ФИО', 'Сумма баллов', 'Рейтинг']
const tableSizeColumns = '1fr 8fr 3fr 3fr'
const teachersData = ref([])

const route = useRoute() // Получаем текущий маршрут
const departmentId = computed(() => {
  return Number(route.params.id)
})

// Вытягиваю данные с бека
onMounted(async () => {
  try {
    const teacherResponse = await axios.get(`http://127.0.0.1:8000/api/v1/departments/${departmentId.value}/teachers/`)
    teachersData.value = teacherResponse.data
    console.log(teachersData.value)
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <div class="w-4/5 h-screen m-auto bg-slate-200 rounded-xl shadow-2xl mt-10">
    <headerBlock>
      <div
        class="text-2xl shadow-2xl text-slate-400 font-bold transition hover:text-blue-400 hover:scale-105 cursor-pointer bg-slate-200 ms-5 p-2 rounded-3xl"
        @click="() => $router.push('/profile')"
      >
        Переход в ЛК заведующего кафедрой
      </div>
    </headerBlock>
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
        v-for="(teacher, index) in teachersData"
        :key="teacher.id"
        :columnTemplates="tableSizeColumns"
      >
        <table-column>{{ index + 1 }}</table-column>
        <table-column class="text-blue-400 underline cursor-pointer">
          <router-link :to="{ name: 'teachersInsidePage', params: { id: teacher.id } }">
            {{ teacher.surname }} {{ teacher.name }} {{ teacher.parentName }}
          </router-link>
        </table-column>
        <table-column>{{ teacher.total_score }}</table-column> <!-- Сумма баллов -->
        <table-column>{{ index + 1 }}</table-column>
      </table-row>
    </base-table>
  </div>
</template>