<template>
	<v-layout row wrap>
		<v-flex xs12>
		<v-btn round color="success" to="/tests/add" dark>
			<v-icon size="32px">
				add
			</v-icon>
		 Создать новый тест</v-btn>
		</v-flex>
<v-flex xs12>
		 <created-test
			v-for="test in tests"
			:id="test.id"
			:title="test.title"
			author="author"
			:description="test.body"
			:image="'https://datalore.io/logo/RGB/Logo-RGB.svg'"
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
				Axios.get('https://jsonplaceholder.typicode.com/posts', {
		          //headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
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