<template>
	<v-layout row wrap>
      <v-flex xs12>
        <v-card class="testItem px-2 py-2">  
        	<v-layout row wrap>
	        	<v-flex xs12 sm4>
		        	<v-img
		        	class="mb-2"
		        	:aspect-ratio="16/9" 
		            :src="image"
		            position="center center"
		          >
		          </v-img>
		      </v-flex>

				<v-flex xs12 sm8>
		          <v-card-title :to="{ name: 'testpage', params: { token: token }}" primary-title>
		            <div>
		              <div class="headline">{{title}}</div>
		              <div v-if="added">Автор: {{author}}</div>
		            </div>
		          </v-card-title>
		      </v-flex>

			</v-layout>
				<v-divider light></v-divider>

				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="successDelete ? success : error"
			      >
			        {{message}}

			      	<v-tooltip v-if="!successDelete" top>
				        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
				        <span>Обновить</span>
				    </v-tooltip>
			      </v-alert>
		      </v-flex>	

				<v-flex xs12>
		          <v-card-actions>
		            <v-btn icon @click="show = !show">
		              <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
		            </v-btn>
		            <v-btn v-if="!added" :to="{ name: 'edittest', params: { token: token }}" icon><v-icon>edit</v-icon></v-btn>
		            <v-btn v-if="!added" @click.native="deleteTest(token)" icon><v-icon>delete</v-icon></v-btn>
		          </v-card-actions>
		      </v-flex>

				<v-flex xs12 >
		          <v-slide-y-transition>
		            <v-card-text v-show="show">
		              {{description}}
		            </v-card-text>
		          </v-slide-y-transition>
		      </v-flex>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		props: ['title', 'token', 'author', 'image', 'description', 'added'],
		data() {
			return {
				show: false,
				added: false,
				successDelete: false,
				alert: false,
				message: ''
			}
		},
		methods: {
			deleteTest(token) {
				Axios.delete(TestingSystemAPI+'/api/courses/'+token+'/', {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.alert = true
		          this.successDelete = true
		          this.message = 'Тест успешно удален.'
		        }).catch(error => {
		          this.alert = true
		          this.successDelete = false
		          this.message = 'Не удалось удалить тест. Проверьте подключение к сети.'

		          console.log(error)
		        })
		    },
			reloadPage() {
				window.location.reload(true)
			}
		}
	}
</script>

<style>
	.testItem{
		margin-top: 10px
	}
</style>