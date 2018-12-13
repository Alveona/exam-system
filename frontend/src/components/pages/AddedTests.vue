<template>	
	<div>
		<v-flex xs12>
			<p class="display-1">Добавленные тесты</p>
		</v-flex>
		<v-flex xs12>
			<v-label>{{notify}}</v-label>
			 <created-test
				v-for="test in tests"
				:token="test.token"
				:title="test.name"
				:author="test.author"
				:added="1"
				:description="test.description"
				:image="!!test.image ? test.image : emptyPic"
			></created-test>
		</v-flex>
		<v-flex xs12>
			<v-alert
	        :value="alert"
	        type="error"
	      >
	        {{message}}

	      	<v-tooltip top>
		        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
		        <span>Обновить</span>
		    </v-tooltip>
	      </v-alert>
      </v-flex>		
	</div>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
  	import CreatedTest from '@/components/boxes/CreatedTest'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default{
		components: { CreatedTest },
		data() {
			return {
				tests: [],
				message: '',
				notify: '',
				alert: false,
				emptyPic: require('@/assets/images/no_image.png')
			}
		},
		methods: {
			getAddedTests() {
				Axios.get(`${TestingSystemAPI}/api/courses-added/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.tests = data
		          this.tests.reverse()
		          if (this.tests.length == 0)
		          	this.notify = 'Нет добавленных тестов.'
		          else this.notify = 'Вы добавили ' + this.tests.length + ' тестов:'
		        }).catch(error => {
		          this.alert = true
		          this.message = 'Не удалось получить список тестов. Проверьте подключение к сети.'

		          console.log(error)
		        })
			},
			reloadPage() {
				window.location.reload(true)
			}
		},
		mounted() {
			this.getAddedTests()
		}
	}
</script>

<style>
	
</style>