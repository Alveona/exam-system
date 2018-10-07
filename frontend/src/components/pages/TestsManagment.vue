<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="display-1">Управление тестами
			</p>
		</v-flex>
		<v-flex xs12>
			<v-btn round color="success" to="add/test" dark>
				<v-icon size="32px">
					add
				</v-icon>
			 Создать новый тест</v-btn>
		</v-flex>
		<v-flex xs12>
			<created-test
				v-for="test in tests"
				:token="test.token"
				:title="test.name"
				:description="test.description"
				:image="test.image"
				:added="0"
			></created-test>
		</v-flex>
	    <v-snackbar :timeout="timeout"
	                bottom="bottom"
	                color="red lighten-1"
	                v-model="snackbar">
	      {{ message }}
	    </v-snackbar>
	</v-layout>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
  	import CreatedTest from '@/components/boxes/CreatedTest'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		components: { CreatedTest },
		data() {
			return {
				tests: [],
				timeout: 0,
				message: '',
				snackbar: false
			}
		},
		methods: {
			getCreatedTests() {
				Axios.get(`${TestingSystemAPI}/api/courses-created/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.tests = data
		        }).catch(error => {
		          this.snackbar = true
		          this.message = 'Не удалось получить список тестов'

		          console.log(error)
		        })
			}
		},
		mounted() {
			this.getCreatedTests()
		}
	}
</script>

<style>
	
</style>