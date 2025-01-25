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
  <!-- <headerBlock  /> -->
  <div class="h-screen">
    <div class="h-full w-full flex justify-center items-center">
      <div
        class="flex flex-col items-center justify-center border-2 rounded-2xl h-fit w-1/2 shadow-2xl bg-white p-10"
      >
      <div class="text-4xl font-sm mb-6 text-center">Авторизация</div>
        <div class="flex gird gird-cols-2 items-center justify-center w-full">
          <div class="w-40">
            <img
              src="../assets/hearld_left.png"
              alt="Логотип"
              class="flex h-35 w-auto flex-shrink-0 hidden md:block"
              @click="() => $router.push('/')"
            />
          </div>
          <div class="m-auto w-full p-auto">
            <form class="w-full" @submit.prevent="login">
              <div class="mb-6">
                <label for="login" class="mb-2 text-sm font-medium text-gray-900 block"
                  >Ваш логин</label
                >
                <input
                  v-model="username"
                  type="login"
                  id="login"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-3"
                  placeholder="Логин..."
                  required
                />
              </div>
              <div class="mb-6">
                <label for="password" class="mb-2 text-sm font-medium text-gray-900 block"
                  >Ваш пароль</label
                >
                <input
                  v-model="password"
                  type="password"
                  id="password"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-3"
                  placeholder="Пароль..."
                  required
                />
              </div>
              <button
                type="submit"
                class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full px-5 py-3 text-center"
              >
                Войти
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
