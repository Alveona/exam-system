<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="title text-md-center"> {{response.name}}</p>
		</v-flex>
		<v-layout row wrap>
        	<v-flex xs12 sm4 class="px-4 py-4">
        		<v-flex xs12>
		        	<v-img 
		        	class="mb-3"
		        	:aspect-ratio="16/9" 
		            :src="response.image"
		            position="center center"
		            >
		            </v-img>
		        </v-flex>
	            <v-flex xs12>

	            	<v-flex xs12>
						<v-alert
				        :value="alert"
				        :type="successReq ? 'success' : infoReq ? 'info' : 'error'"
        				transition="scale-transition"
        				outline
				        >
					        {{alert_message}}

					      	<v-tooltip v-if="!successReq" top>
						        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
						        <span>Обновить</span>
						    </v-tooltip>
					    </v-alert>
			        </v-flex>	

		            <v-btn v-if="response.subscribed" round color="primary" :to="{ name: 'testing', params: { token: $route.params.token } }" dark block large>
						 Пройти тест
					</v-btn>
					<v-btn v-if="!response.subscribed" @click.native="subscribe()" round color="success" dark block large>
						 Подписаться
					</v-btn>
					<v-btn v-else round color="error" @click.native="unsubscribe()" dark block large>
						 Отписаться
					</v-btn>
				</v-flex>	
	        </v-flex>

	        <v-flex xs12 sm8>
	          <v-flex xs12>
	              <p><strong>Ссылка:</strong> http://web.ru/tests/{{$route.params.token}}</p>
	          </v-flex>
			  <v-flex xs12>
	              <p><strong>Автор:</strong> {{response.author}}</p>
	          </v-flex>
	          <v-flex xs12>
	          	<p>
	              	<span v-if="!response.subscribed">Не подписан на тест</span>
	              	<span v-else><strong>Использованные попытки:</strong> {{response.current_attempt}} / {{response.attempts}}</span>
	              </p>
	          </v-flex>
              <v-flex xs12 class="wrapText">
	            <p >{{response.description}}
				</p>
	      	  </v-flex>
	        </v-flex>
	    </v-layout>
	       
	</v-layout>
</template>

<script>
    import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		data() {
			return {
				alert_message: '',
				alert: false,
				successReq: false,
				response: []
			}
		},
		methods: {
            getTestData()
            {
		        console.log(this.$route.params.token)
            	Axios.get(`${TestingSystemAPI}/api/courses/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: { 'token' : this.$route.params.token}
		        }).then(({data}) => {
		          this.response = data[0]
		          this.alert = false
		          this.successReq = true
		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось получить данные теста.'
		          this.successReq = false
		          console.log(error)
		        })
            },
            subscribe() {
            	var token = { 'token' : this.$route.params.token }
            	Axios.post(`${TestingSystemAPI}/api/course-subsc/`, token, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.alert = true
		          this.alert_message = 'Вы успешно подписались!'
		          this.infoReq = false
		          this.successReq = true
		          this.response.subscribed = true
		        }).catch(error => {
		          this.alert = true
		          this.infoReq = false
		          this.alert_message = 'Не удалось подписаться.'
		          this.successReq = false

		          console.log(error)
		        })
            },
            unsubscribe() {
            	var token = { 'token' : this.$route.params.token }
            	Axios.post(`${TestingSystemAPI}/api/course-subsc/`, token, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.alert = true
		          this.alert_message = 'Вы отписались от теста.'
		          this.infoReq = true
		          this.successReq = false
		          this.response.subscribed = false
		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось отписаться.'
		          this.infoReq = false
		          this.successReq = false

		          console.log(error)
		        })
            },
			reloadPage() {
				window.location.reload(true)
			},
			hideAlert() {
				this.alert = false
			},
			startTimer() {
				setTimeout(this.hideAlert, 4000)
			}
		},
		mounted(){
			this.getTestData()
		},
		watch: {
			alert: function(val) {
				if (val)
					this.startTimer()
			}
		}
	}
</script>

<style>
.wrapText{
	word-wrap: break-word;
}
</style>