<script setup>
import axios from 'axios'
import headerBlock from '../components/headerBlock.vue'
import { ref } from 'vue'
import router from '@/router'

const username = ref('')
const password = ref('')
const token = ref(localStorage.getItem('token') || '')

const login = (event) => {
  event.preventDefault()

  axios
    .post(`http://127.0.0.1:8000/auth/token`, {
      username: username.value,
      password: password.value
    })
    .then((response) => {
      setLogin(response.data.token)
    })
    .catch((error) => {
      console.log(error)
    })
}

const setLogin = (token) => {
  if (token) {
    localStorage.setItem('token', token)
    router.push({ name: 'profielPage' })
  } else {
    alert('Неверный логин или пароль')
  }
}


</script>
<template>
  <div class="w-4/5 h-screen m-auto bg-slate-200 rounded-xl shadow-2xl mt-10">
    <headerBlock />
    <div class="m-auto grid grid-cols-2 items-center p-5 justify-items-center">
      <div class="text-3xl text-blue-400 font-bold grid col-span-2">
        Вход в профиль заведующего кафедрой
      </div>
      <div class="grid col-span-2 mt-5">
        <form class="w-full max-w-sm" @submit="login">
          <div class="mb-5">
            <label for="login" class="mb-2 text-sm font-medium text-gray-900">Ваш логин</label>
            <input
              v-model="username"
              type="login"
              id="login"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5"
              placeholder="Логин..."
              required
            />
          </div>
          <div class="mb-5">
            <label for="password" class="mb-2 text-sm font-medium text-gray-900">Ваш пароль</label>
            <input
              v-model="password"
              type="password"
              id="password"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5"
              placeholder="Пароль..."
              required
            />
          </div>

          <button
            type="submit"
            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full px-5 py-2.5 text-center"
          >
            Войти
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
