import Vue from 'vue'
import Router from 'vue-router'
import * as Auth from '@/components/pages/Authentication'

// Pages
import Main from '@/components/pages/Main'
import Authentication from '@/components/pages/Authentication/Authentication'
import AddedTests from '@/components/pages/AddedTests'
import QuestionsManagment from '@/components/pages/QuestionsManagment'
import TestsManagment from '@/components/pages/TestsManagment'
import Stats from '@/components/pages/Stats'
import UserGuide from '@/components/pages/UserGuide'
import AddQuestion from '@/components/pages/AddQuestion'

//Boxes
import AddedQuestion from '@/components/boxes/AddedQuestion'

Vue.component('added-question', AddedQuestion)

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main,
      children: [{
      	path: '',
      	component: AddedTests
      },{
      	path: 'addedtests',
      	component: AddedTests
      },{
      	path: 'questions',
      	component: QuestionsManagment,
      },{
      	path: 'questions/add',
      	component: AddQuestion,
      },{
      	path: 'questions/edit',
      	component: QuestionsManagment,
      },{
      	path: 'tests',
      	component: TestsManagment
      },{
      	path: 'stats',
      	component: Stats
      },{
      	path: 'guide',
      	component: UserGuide
      }]
  	},
    {
      path: '/login',
      name: 'Authentication',
      component: Authentication
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path !== '/login') {
    if (Auth.default.user.authenticated) {
      next()
    } else {
      router.push('/login')
    }
  } else {
    next()
  }
})

export default router
