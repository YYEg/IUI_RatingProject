// store.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    teachersScores: {} // объект для хранения суммарных баллов преподавателей
  },
  mutations: {
    updateTeacherScore(state, { teacherId, score }) {
      state.teachersScores[teacherId] = score
    }
  },
  actions: {
    // Создайте действие для обновления суммарного балла преподавателя
    updateTeacherScore({ commit }, { teacherId, score }) {
      commit('updateTeacherScore', { teacherId, score })
    }
  },
  getters: {
    // Создайте геттер для получения суммарного балла преподавателя
    getTeacherScore: (state) => (teacherId) => {
      return state.teachersScores[teacherId] || 0
    }
  }
})
