<template>	
	<v-layout row wrap>	

		<v-flex xs12>
			<p class="display-1">Управление вопросами</p>
		</v-flex>

		<v-flex xs12>
			<v-btn round color="success" to="add/question" class="mb-3" dark>
				<v-icon size="24px" class="mr-2">
					add
				</v-icon>
			Добавить новый вопрос</v-btn>
		</v-flex>

		<v-flex xs12>
			<p v-if="successLoad">{{success_message}}</p>
			<added-question
			v-for="question in questions"
				:id="question.id"
				:title="question.title"
				:text="question.text"
				:type="question.answer_type"
				:withchecks="0"
				:element="questions.indexOf(question)"
				:collection="questions"
			></added-question>
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
				alert: false,
				alert_message: '',
				successLoad: false
			}
		},
		methods: {
			getAddedQuestions() {
				Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = data
		          this.successLoad = true
		        }).catch(error => {
		          this.alert = true
		          this.message = 'Не удалось получить список вопросов. Проверьте подключение к сети.'

		          console.log(error)
		        })
			},
			reloadPage() {
				window.location.reload(true)
			}
		},
	    mounted () {
	      this.getAddedQuestions()
	    },
	    computed: {
	    	success_message: function() {
	          if (!this.questions.length)
	          	return 'В вашем профиле нет созданных вопросов.'
	          else return 'Добавлено ' + this.questions.length + ' вопросов:'
	    	}
	    }
	}
</script>

<style>
</style>