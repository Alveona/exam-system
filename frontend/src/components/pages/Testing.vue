<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="title text-md-center">Вопрос {{question.order_number}}.</p>
		</v-flex>
		<v-flex v-if="question.image != null" xs12>
			<p>{{question.text}}</p>
		</v-flex>
		<v-layout v-else row wrap>
			<v-flex xs12 sm4>
	        	<v-img 
	        	class="mb-3"
	        	:aspect-ratio="16/9" 
	            src="https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg?auto=compress&cs=tinysrgb&h=350"
	            position="center center"
	            >
	            </v-img>
	        </v-flex>
	        <v-flex xs12 sm8>
				<p>{{question.text}}</p>
			</v-flex>
		</v-layout>
		<v-flex v-if="question.answer_type == 1" xs12>
            <v-text-field
              label="Ваш ответ"
              v-model=""
              required
      		  clearable
      		  :rules="rules"
      		  box
            ></v-text-field>
		</v-flex>
		<v-flex v-else-if="question.answer_type == 2" xs12>

		</v-flex>
		<v-flex v-else-if="question.answer_type == 3" xs12>

		</v-flex>

		<v-layout row wrap>
			<v-flex xs12 sm6 >
				<v-btn round color="success" dark block large>
					 Ответить
				</v-btn>
			</v-flex>
			<v-flex xs12 sm3>
				<v-btn round color="primary" dark block large>
					 Пропустить
				</v-btn>
			</v-flex>
			<v-flex xs12 sm3>
				<v-btn round color="error" dark block large>
					 Прервать тест
				</v-btn>
			</v-flex>
		</v-layout>
		<v-snackbar 
		:timeout="timeout"
        bottom="bottom"
        color="red lighten-1"
        v-model="snackbar"
        >
	      {{ message }}
	    </v-snackbar>
	</v-layout>
</template>

<script>
    import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default{
		data() {
			return {
				timeout: 0,
				message: '',
				snackbar: false,
				question: [],
				answers: []
			}
		},
		methods: {
            getQuestion()
            {
            	Axios.get(`${TestingSystemAPI}/api/session-q/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: { 'token' : $route.params.token }
		        }).then(({qdata}) => {
		        	
		          this.question = qdata

		          Axios.get(`${TestingSystemAPI}/api/session-a/`, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: { 'id' : this.question.id }
			        }).then(({adata}) => {
			          this.answers = adata
			        }).catch(error => {
			          this.snackbar = true
			          this.message = 'Не удалось получить данные для прохождения тестирования'

			          console.log(error)
			        })
			        
		        }).catch(error => {
		        	//ПОСЛАТЬ POST НА СОЗДАНИЕ ВОПРОСА
		          this.snackbar = true
		          this.message = 'Не удалось получить данные для прохождения тестирования'

		          console.log(error)
		        })
            }
		},
		mount(){
			this.getQuestion()
		}
	}
</script>

<style>
	
</style>