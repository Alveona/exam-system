<template>
	<v-layout row wrap>
		<v-flex xs12>
		  <v-layout row wrap v-for="question in collection">
		    <v-flex xs12>
		        <v-card class="questionItem">  
		          <v-card-title primary-title :to="{ name: 'editquestion', params: { id: question.id }}">
		          	<v-flex xs1 v-if="withchecks">
		          		<v-checkbox v-model="questionsChecks" :value="question.id" @change="$emit('update:questionsChecks', questionsChecks)" hide-details class="shrink mr-2 mt-0"></v-checkbox>
		            </v-flex>
		          <v-flex v-if="withchecks ? 'xs11' : 'xs12'">
		              <span class="headline">{{question.title}} 
		              	<v-tooltip bottom>
		              	<v-btn icon slot="activator" small>
		              		<v-icon color="light-blue darken-1">info</v-icon>
		              	</v-btn>
		              	<span> {{question.answer_type==1 ? 'Тип ответа: ввод значения' : question.answer_type==2 ? 'Тип ответа: выбор одного правильного' : 'Тип ответа: выбор нескольких правильных'}} </span>
		              </v-tooltip>
		            </span>
		          </v-flex>
				  <v-spacer></v-spacer>

				  <v-tooltip bottom v-if="!withchecks && question.can_manage">
	              	<v-btn slot="activator" v-if="!withchecks" :to="{ name: 'editquestion', params: { id: question.id }}" icon><v-icon>edit</v-icon></v-btn>
	              	<span>Редактировать вопрос</span>
		          </v-tooltip>

				  <v-tooltip bottom v-if="!withchecks && question.can_manage">
	              	<v-btn slot="activator" @click.native="deleteQuestion(collection.indexOf(question), question.id)" icon><v-icon>delete</v-icon></v-btn>
	              	<span>Удалить вопрос</span>
		          </v-tooltip>
				  
				  <v-tooltip bottom>
		            <v-btn slot="activator" icon @click="$emit('update:collection', question.id)">
		              <v-icon>{{ question.show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
		            </v-btn>
	              	<span>{{ question.show ? 'Скрыть формулировку' : 'Показать формулировку'}}</span>
		          </v-tooltip>
		          </v-card-title>
		  
					<v-flex xs12>
						<v-alert
				          :value="alert"
				          :type="successDelete ? 'success' : 'error'"
				        >
				        {{alert_message}}

					      	<v-tooltip v-if="!successDelete" top>
						        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
						        <span>Обновить</span>
						    </v-tooltip>
					    </v-alert>
			      </v-flex>	

		          <v-slide-y-transition>
		            <v-card-text v-show="question.show">
		              <p class="wrappedText">
			            Создатель вопроса: {{question.author.surname}} {{question.author.name}}
			          </p>
		              <p class="wrappedText">
			            {{question.text}}
			          </p>
		            </v-card-text>
		          </v-slide-y-transition>

		          <v-snackbar 
			        color="green lighten-1"
			        v-model="snackbar"
			      >
				    {{ snackbar_message }}
				  </v-snackbar>

		        </v-card>
		    </v-flex>
		  </v-layout>
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
		props: ['withchecks', 'questionsChecks', 'collection'],
		data() {
			return {
				alert: false,
				alert_message: '',
				snackbar: false,
				snackbar_message: '',
				successDelete: false
			}
		},
		methods: {
			deleteQuestion(index, id) {
				Axios.delete(TestingSystemAPI+'/questions/'+id+'/', {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.collection.splice(index, 1)
		          this.snackbar = true
		          this.successDelete = true
		          this.snackbar_message = 'Вопрос успешно удален.'
		        }).catch(error => {
		          this.alert = true
		          this.successDelete = false
		          this.alert_message = 'Не удалось удалить вопрос. Проверьте подключение к сети.'

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
	.questionItem{
		margin-top: 10px
	}
	.wrappedText{
		word-wrap:break-word;
	}
</style>