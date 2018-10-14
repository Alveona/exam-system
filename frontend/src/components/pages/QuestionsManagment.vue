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
				:withchecks="0"
				:collection="questions"
				@update:collection="toggleShow($event)"
			></added-question>
		</v-flex>

	    <v-flex xs12>
			<v-alert
	        :value="alert"
	        type="error"
	      >
	        {{alert_message}}

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
		          for (var i = 0; i < this.questions.length; ++i)
		          {
		          	this.questions[i].show = false
					console.log(this.questions[i].show)
		          }
		          this.successLoad = true
		        }).catch(error => {
		          this.alert = true
		          this.message = 'Не удалось получить список вопросов. Проверьте подключение к сети.'

		          console.log(error)
		        })
			},
			reloadPage() {
				window.location.reload(true)
			},
			toggleShow(id) {
				for (var i = 0; i < this.questions.length; ++i)
					if (this.questions[i].id == id)
					{
						this.questions[i].show = !this.questions[i].show
						this.questions.push(null)
						this.questions.pop()
						return
					}
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