<template>
	<main class="l-home-page">
    <v-navigation-drawer
      fixed
      :clipped="$vuetify.breakpoint.mdAndUp"
      app
      v-model="drawer"
    >
      <v-list dense>
<template v-for="item in items">
	
          <v-layout
            row
            v-if="item.heading"
            align-center
            :key="item.heading"
          >
            <v-flex xs6>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
            <v-flex xs6 class="text-xs-center">
              <a href="#!" class="body-2 black--text">EDIT</a>
            </v-flex>
          </v-layout>
          <v-list-tile v-else @click="changePage(item.link)" :key="item.text">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      color="blue darken-3"
      dark
      app
      :clipped-left="$vuetify.breakpoint.mdAndUp"
      fixed
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span class="hidden-sm-and-down"></span>
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn
          large
          icon
          @click.native="signout()"
        >
          <v-icon size="32px">
            power_settings_new
          </v-icon>
        </v-btn>
      
    </v-toolbar>

    <v-content class="innerContent">
      <router-view></router-view>
    </v-content>
    
</main>
</template>

<script>
  import Axios from 'axios'
  import router from '@/router'
  import Authentication from '@/components/pages/Authentication'
  import connection from '@/router/connection'

  const TestingSystemAPI = connection.server
  export default {
  	data () {
      return {
	      dialog: false,
	      drawer: null,
	      items: [
          //{ icon: 'import_contacts', text: 'Руководство пользователя', link: '/' },
	      	{ icon: 'done', text: 'Добавленные тесты', link: '/addedtests' },
	        //{ icon: 'trending_up', text: 'Статистика', link: '/stats' }
          { icon: 'account_circle', text: 'Настройка профиля', link: '/profile'}
	      ]
	    }
  	},
  	methods: {
  		signout(){
  			Authentication.signout(this, '/login');
  		},
  		changePage(link){
  			router.push(link)
        
  		},
      toProfile(){
        router.push('/profile')
      },
      async getMy(){
        await Axios.get(`${TestingSystemAPI}/my`, {
              headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
              params: {}
            }).then(({data}) => {
              if (data.group != 'student')
              {
                this.items.push({ icon: 'supervisor_account', text: 'Настройка преподавателей', link: '/modes' })
                this.items.push({ icon: 'help_outline', text: 'Управление вопросами', link: '/questions' })
                this.items.push({ icon: 'toc', text: 'Управление тестами', link: '/test_pages' })
              }
              if (data.has_user_list_access)
                this.items.push({ icon: 'account_circle', text: 'Доступ к пользователям', link: '/profiles' })
            }).catch(error => {
              this.error = true
              console.log(error)
            })
      }
  	},
    mounted(){
      this.getMy()
    }
  }
</script>

<style>
	.innerContent{
    margin:0 0 0 -260px;
  }
  .l-home-page{
    margin: 0 0 0 260px;
    width:100%;
  }
</style>