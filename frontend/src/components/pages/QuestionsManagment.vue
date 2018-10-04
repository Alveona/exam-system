<template>	
	<v-layout row wrap>
		<v-flex xs12>
		<v-btn round color="success" to="/tests/add" dark>
			<v-icon size="32px">
				add
			</v-icon>
		 Добавить новый вопрос</v-btn>
		</v-flex>
		<v-flex xs12>
		<added-question
		v-for="question in questions"
			:title="question.title"
			:text="question.body"
			:type="2"
		></added-question>
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
  	import AddedQuestion from '@/components/boxes/AddedQuestion'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default{
		data() {
			return {
				questions: [],
				snackbar: false,
				message: '',
				timeout: 0
			}
		},
		methods: {
			getAddedQuestions() {
				//Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
				Axios.get('https://jsonplaceholder.typicode.com/posts', {
		          //headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = data
		        }).catch(error => {
		          this.snackbar = true
		          this.message = 'Не удалось получить список вопросов'

		          console.log(error)
		        })
			}
		},
	    mounted () {
	      this.getAddedQuestions()
	    }
	}
</script>

<style>
	
</style>