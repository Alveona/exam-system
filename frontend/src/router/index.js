import Vue from 'vue'
import Router from 'vue-router'
import * as Auth from '@/components/pages/Authentication'

// Pages
import Main from '@/components/pages/Main'
import Authentication from '@/components/pages/Authentication/Authentication'
import Register from '@/components/pages/Authentication/Register'
import AddedTests from '@/components/pages/AddedTests'
import QuestionsManagment from '@/components/pages/QuestionsManagment'
import TestsManagment from '@/components/pages/TestsManagment'
import Stats from '@/components/pages/Stats'
import UserGuide from '@/components/pages/UserGuide'
import Profile from '@/components/pages/Profile'
import AddQuestion from '@/components/pages/AddQuestion'
import EditQuestion from '@/components/pages/EditQuestion'
import AddTest from '@/components/pages/AddTest'
import EditTest from '@/components/pages/EditTest'
import TestPage from '@/components/pages/TestPage'
import ModesPage from '@/components/pages/ModesPage'
import Testing from '@/components/pages/Testing'
import TestResult from '@/components/pages/TestResult'
import ProfilesPage from '@/components/pages/ProfilesPage'

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
        path: 'modes',
        component: ModesPage,
      },{
      	path: 'edit/question/:id',
      	component: EditQuestion,
      	name: 'editquestion'
      },{
      	path: 'test_pages',
      	component: TestsManagment
      },{
      	path: 'test_pages/:token',
      	component: TestPage,
      	name: 'testpage'
      },{
      	path: 'test_pages/:token/testing',
      	component: Testing,
      	name: 'testing'
      },{
      	path: 'tests/:token/result',
      	component: TestResult,
      	name: 'result'
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
        path: 'profile',
        component: Profile
      },{
        path: 'profiles',
        component: ProfilesPage
      },{
      	path: 'guide',
      	component: UserGuide
      }]
  	},
    {
      path: '/login',
      name: 'Authentication',
      component: Authentication
    },
    {
      path: '/register',
      component: Register
    },{
      path: '/tests/:token',
      component: TestPage,
      name: 'ext_testpage'
    }
  ]
})

router.beforeEach((to, from, next) => {

  if (to.path !== '/login' && to.path !== '/register' && (!to.path.includes('/tests/'))) {
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
