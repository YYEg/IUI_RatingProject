import { createRouter, createWebHistory } from 'vue-router'
import teachersRatingPage from './Views/teachersRatingPage.vue'
import departamentRatingPage from './Views/departamentRatingPage.vue'
import depatmentInsidePage from './Views/depatmentInsidePage.vue'
import teachersInsidePage from './Views/teachersInsidePage.vue'
import loginPage from './Views/loginPage.vue'
import profilePage from './Views/profilePage.vue'
import addAchievements from './Views/addAchivmnetPage.vue'
import testRating from './components/testRating.vue'
import TeachersInsidePage from './Views/teachersInsidePage.vue'
import achievmentDetailed from './Views/achievmentDetailed.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: teachersRatingPage,
      name: 'teachersRatingPage',
      alias: '/teachersRatingPage'
    },
    {
      path: '/testRating',
      component: testRating,
      name: 'testRating'
    },
    {
      path: '/departamentRatingPage',
      component: departamentRatingPage
    },
    {
      path: '/department/:id',
      name: 'departmentInsidePage',
      component: depatmentInsidePage
    },
    {
      path: '/teachers/:id',
      name: 'teachersInsidePage',
      component: TeachersInsidePage,  // Компонент для отображения информации о преподавателе
      props: true,  // Это позволяет передавать параметр `id` в компонент как пропс
    },
    //auth
    {
      path: '/login',
      name: 'login',
      component: loginPage
    },
    {
      path: '/profile',
      name: 'profielPage',
      component: profilePage
    },
    // страница добавления достижений(список преподавателей и модальные окна добавления достижений)
    {
      path: '/profile/addAchievements',
      name: 'addAchievements',
      component: addAchievements
    },
    {
      path: '/employee/:empl_id/achievment/:ach_id',
      name: 'achievmentDetailed',
      component: achievmentDetailed
    },
  ]
})
