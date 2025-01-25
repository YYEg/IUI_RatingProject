import { createRouter, createWebHistory } from 'vue-router'
import teachersRatingPage from './Views/teachersRatingPage.vue'
import departamentRatingPage from './Views/departamentRatingPage.vue'
import depatmentInsidePage from './Views/depatmentInsidePage.vue'
import teachersInsidePage from './Views/teachersInsidePage.vue'
import loginPage from './Views/loginPage.vue'
import profilePage from './Views/profilePage.vue'
import addAchievements from './Views/addAchivmnetPage.vue'
import testRating from './components/testRating.vue'

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
      name: 'testRating',
    },
    {
      path: '/departamentRatingPage',
      component: departamentRatingPage
    },
    {
      path: '/departamentRatingPage/:id',
      name: 'depatmentInsidePage',
      component: depatmentInsidePage,
      props: true
    },
    {
      path: '/teachersRatingPage/:id',
      name: 'teachersInsidePage',
      component: teachersInsidePage,
      props: true
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
    }
  ]
})
