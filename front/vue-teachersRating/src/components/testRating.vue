<template>
  <header
    class="bg-blue-900 text-white py-4 px-6 shadow-lg mx-4 mt-4 mb-2 rounded-xl border-2 border-emerald-800 drop-shadow-2xl"
  >
    <div class="grid grid-cols-2">
      <div class="flex">
        <img
          src="../assets/hearld_left.png"
          alt="Логотип"
          class="h-20 w-auto flex-shrink-0 hidden md:block"
        />
        <div class="flex flex-col rows-2 items-start ml-3 justify-end my-4">
          <h1 class="text-2xl font-bold">ИЮИ (ф) УП РФ</h1>
          <p class="text-sm mt-1">Система эффективного контракта сотрудника университета</p>
        </div>
      </div>
      <button
        class="items-center justify-center p-2 mb-2 me-2 overflow-hidden text-xl font-medium text-white rounded-lg border-2 border cursor-pointer hover:scale-105 hover:shadow-2xl transition duration-700"
      >
        Иванов И.И. | Кафедра государственно-правовых...
      </button>
    </div>
  </header>
  <div class="flex flex-cols-2">
    <div
      class="ml-8 w-60 h-16 bg-blue-900 rounded-t-lg flex items-center justify-center drop-shadow-2xl"
    >
      <div class="font-bold text-white text-xl text-center">Персональный</div>
    </div>
    <div class="ml-8 w-60 h-16 border-2 rounded-t-lg flex items-center justify-center">
      <a
        class="font-bold text-slate-400 text-xl text-center cursor-pointer hover:scale-105 hover:text-black transition duration-700"
        href="/departamentRatingPage"
        >По подразделениям</a
      >
    </div>
  </div>
  <div class="px-3 bg-gray-50 min-h-screen">
    <div class="overflow-hidden rounded-lg shadow-lg">
      <table class="min-w-full table-auto border-collapse">
        <thead class="bg-blue-900 text-white drop-shadow-xl">
          <tr>
            <th class="border-r-2 border-black w-1/12 px-6 py-3 text-center text-l font-sm">№</th>
            <th class="border-r-2 border-black w-2/3 px-6 py-3 text-center text-l font-sm">ФИО</th>
            <th class="border-r-2 border-black w-1/12 px-6 py-3 text-center text-l font-sm">
              Сумма баллов
            </th>
            <th class="border-r-2 border-black w-1/12 px-6 py-3 text-center text-l font-sm">
              Рейтинг по ВУЗу
            </th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr
            v-for="(item, index) in items"
            :key="item.id"
            class="hover:bg-gray-100 hover:shadow-lg transition"
          >
            <td class="w-1/12 px-6 py-4 text-center text-l text-gray-700">
              {{ index + 1 }}
            </td>
            <td class="b w-2/3 px-6 py-4 text-center text-l text-gray-700 font-semibold">
              {{ item.name }}
            </td>
            <td class="w-1/12 px-6 py-4 text-center text-l text-gray-700">
              {{ item.points }}
            </td>
            <td class="w-1/12 px-6 py-4 text-center text-l text-gray-700">
              {{ item.rating }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [
        { id: 1, name: 'Юрковский Е.А.', points: 100, rating: 1 },
        { id: 2, name: 'Назаренко Е.Д.', points: 80, rating: 1 },
        { id: 3, name: 'Денисенко А.С.', points: 60, rating: 1 },
        { id: 1, name: 'Наумов П.А.', points: 40, rating: 1 },
        { id: 1, name: 'Юрковский Е.А.', points: 100, rating: 1 },
        { id: 2, name: 'Назаренко Е.Д.', points: 100, rating: 1 },
        { id: 3, name: 'Денисенко А.С.', points: 100, rating: 1 },
        { id: 1, name: 'Наумов П.А.', points: 100, rating: 1 }
      ]
    }
  }
}
</script>

<style scoped>
table {
  border-spacing: 0;
}
th,
td {
  border-bottom: 1px solid #e5e7eb;
}
th:last-child,
td:last-child {
  border-right: none;
}
</style>
