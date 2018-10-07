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
import EditQuestion from '@/components/pages/EditQuestion'
import AddTest from '@/components/pages/AddTest'
import EditTest from '@/components/pages/EditTest'
import TestPage from '@/components/pages/TestPage'
import Testing from '@/components/pages/TestPage'

//Boxes
import AddedQuestion from '@/components/boxes/AddedQuestion'

Vue.component('added-question', AddedQuestion)

Vue.use(Router)

const router = new Router({
  mode: 'history',
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
      	path: 'add/question',
      	component: AddQuestion,
      },{
      	path: 'edit/question/:id',
      	component: EditQuestion,
      	name: 'editquestion'
      },{
      	path: 'tests',
      	component: TestsManagment
      },{
      	path: 'tests/:token',
      	component: TestPage,
      	name: 'testpage'
      },{
      	path: 'tests/:token/testing',
      	component: Testing
      },{
      	path: 'add/test',
      	component: AddTest
      },{
      	path: 'edit/test/:token',
      	component: EditTest,
      	name: 'edittest'
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
