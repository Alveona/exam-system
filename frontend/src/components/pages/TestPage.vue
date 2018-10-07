<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="title text-md-center"> Имя теста</p>
		</v-flex>
		<v-layout row wrap>
        	<v-flex xs12 sm4 class="px-4 py-4">
        		<v-flex xs12>
		        	<v-img 
		        	class="mb-3"
		        	:aspect-ratio="16/9" 
		            src="https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg?auto=compress&cs=tinysrgb&h=350"
		            position="center center"
		            >
		            </v-img>
		        </v-flex>
	            <v-flex xs12>
	            <v-btn v-if="response.subscribed" round color="primary" dark block large>
					 Пройти тест
				</v-btn>
				<v-btn v-if="!response.subscribed" round color="success" dark block large>
					 Подписаться
				</v-btn>
				<v-btn v-else round color="error" dark block large>
					 Отписаться
				</v-btn>
			  </v-flex>	
	        </v-flex>

	        <v-flex xs12 sm8>
			  <v-flex xs12>
	              <p>Автор: {{response.author}}</p>
	          </v-flex>
	          <v-flex xs12>
	              <p>Статус: 
	              	<span v-if="!response.subscribed">Не подписан на тест</span>
	              	<span v-else>Использованные попытки: {{response.attempts}} / {{response.max_attempts}}</span>
	              </p>
	          </v-flex>
              <v-flex xs12>
	            <p>Curabitur magna eros, lacinia sed magna eu, aliquet vestibulum dolor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ut leo dignissim risus pharetra feugiat. Proin volutpat felis massa, sit amet volutpat odio interdum et. Vestibulum imperdiet sapien quis euismod tempor. Mauris tristique id eros ac facilisis. Ut consectetur dictum tincidunt. Duis a convallis nulla, quis sodales lectus. Sed in enim sit amet quam rhoncus rhoncus. Integer ut consectetur magna. Nunc auctor viverra est, et volutpat neque aliquet in. Suspendisse dapibus tristique tincidunt. Mauris ut mi ultrices, rhoncus felis quis, tempor orci. Morbi congue enim quis tellus tristique vestibulum. Proin pharetra velit sed eros sollicitudin molestie.

				Donec blandit dui auctor, euismod nulla sit amet, volutpat dui. Fusce lorem purus, fringilla sed justo in, posuere ornare tellus. Suspendisse sed justo a augue bibendum dignissim. Quisque consequat mattis dolor, id pellentesque neque ultricies in. Nullam a massa ante. Aliquam erat volutpat. Suspendisse ac tempor metus. Vivamus sed sem non turpis semper euismod. Donec tincidunt eu enim id volutpat. Vivamus dictum ullamcorper pellentesque. Integer eget ipsum ut massa vestibulum eleifend id gravida lectus.
				</p>
	      	  </v-flex>
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
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		data() {
			return {
				tests: [],
				timeout: 0,
				message: '',
				response: []
			}
		},
		methods: {
            getTestData()
            {
            	Axios.get(`${TestingSystemAPI}/api/courses/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: { 'test_token' : $route.params.token}
		        }).then(({data}) => {
		          this.response = data
		        }).catch(error => {
		          this.snackbar = true
		          this.message = 'Не удалось получить данные теста'

		          console.log(error)
		        })
            }
		},
		mount(){
			this.getTestData()
		}
	}
</script>

<style>
</style>