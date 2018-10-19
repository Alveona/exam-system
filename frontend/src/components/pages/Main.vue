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
        <span class="hidden-sm-and-down">Service Title</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>


      <v-menu
        v-model="menu"
        :close-on-content-click="false"
        offset-x
      >
        <v-btn
          slot="activator"
          large
          icon
        >
          <v-icon size="32px">
            more_vert
          </v-icon>
        </v-btn>
  
        <v-card>
          <v-list>
            <v-list-tile>
              <v-icon class="mr-3">
                account_circle
              </v-icon>
              <v-list-tile-title>Настройки профиля</v-list-tile-title>
            </v-list-tile>
  
            <v-list-tile @click="signout()">
              <v-icon class="mr-3">
                power_settings_new
              </v-icon>
              <v-list-tile-title>Выйти</v-list-tile-title>
            </v-list-tile>
          </v-list>
  
        </v-card>
      </v-menu>


    </v-toolbar>

    <v-content>
      <router-view></router-view>
    </v-content>
    
</main>
</template>

<script>
  import router from '@/router'
  import Authentication from '@/components/pages/Authentication'
  export default {
  	data () {
      return {
	      dialog: false,
	      drawer: null,
	      items: [
	      	{ icon: 'done', text: 'Добавленные тесты', link: '/' },
	        { icon: 'help_outline', text: 'Управление вопросами', link: '/questions' },
	        { icon: 'toc', text: 'Управление тестами', link: '/tests' },
	        { icon: 'trending_up', text: 'Статистика', link: '/stats' },
	        { icon: 'import_contacts', text: 'Руководство пользователя', link: '/guide' }
	      ]
	    }
	},
	methods: {
		signout(){
			Authentication.signout(this, '/login');
		},
		changePage(link){
			router.push(link)
		}
	}
  }
</script>

<style>
	
</style>