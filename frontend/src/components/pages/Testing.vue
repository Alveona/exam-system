<template>
	<v-layout row wrap>

		<v-flex xs12>
			<p class="title text-md-center">Вопрос {{question.order_number}}.</p>
		</v-flex>

		<v-flex v-if="!question.question.image" xs12 class="my-3">
			<p class="font-weight-regular subheading">{{question.question.text}}</p>
		</v-flex>

		<v-layout v-else row wrap class="my-3">
			<v-flex xs12 sm6 offset-sm3>
	        	<v-img 
	        	class="mb-3"
	        	:aspect-ratio="16/9" 
	            :src="question.question.image"
	            position="center center"
	            ></v-img>
	        </v-flex>
	        <v-flex xs12>
				<p class="font-weight-regular subheading">{{question.question.text}}</p>
			</v-flex>
		</v-layout>

		<v-flex xs12 class="mb-4" > 
			<vue-audio :file="question.question.audio" :autoPlay="question.audio_hint != null ? false : true"/>
		</v-flex>

		<v-flex v-if="question.question.answer_type == 1" xs12>
            <v-text-field 
              label="Ответ"
              v-model="fullAnswer"
              required
      		  clearable
      		  :rules="rules"
      		  box
            ></v-text-field>
		</v-flex>

		<v-flex v-else-if="question.question.answer_type == 2" xs12>
			<v-radio-group>
				<v-radio
		          v-for="answer in resAnswers"
		          :label="answer.answer.text"
		          :value="answer.id"
		          @change="changeRadio(answer.id)"
		        ></v-radio>
		    </v-radio-group>
		</v-flex>

		<v-flex v-else-if="question.question.answer_type == 3" xs12>
			<v-checkbox 
			  v-for="answer in resAnswers"
			  :label="answer.answer.text" 
			  :value="answer.id"
			  @change="changeCheck(answer.id)"
			></v-checkbox>
		</v-flex>


		<v-flex xs12 v-if="question.audio_hint != null" class="mb-4"> 
			<vue-audio :file="question.audio_hint" :autoPlay="true"/>
		</v-flex>

		<v-flex xs12 v-if="question.hint != '' && question.hint != 'null'"> 
		  <v-alert 
	        :value="true"
	        type="warning"
	      >
	        {{question.hint}}
	      </v-alert>
		</v-flex>

		<v-layout row wrap>

			<v-flex xs12 sm6 class="px-3">
				<v-btn round color="success" @click.native="setAnswer()" dark block large>
					 Ответить
				</v-btn>
			</v-flex>
			<v-flex xs12 sm3 class="px-3">
				<v-btn round color="primary" @click.native="skipAnswer()" dark block large>
					 Пропустить
				</v-btn>
			</v-flex>
			<v-flex xs12 sm3 class="px-3">
				<v-btn round color="error" @click.native="stopTest()" dark block large>
					 Прервать тест
				</v-btn>
			</v-flex>

		</v-layout>

	</v-layout>
</template>

<script>
	import VueAudio from 'vue-audio'
    import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default{
		components: { VueAudio },
		data() {
			return {
				question: [],
				resAnswers: [],
				reqAnswers: [],
				fullAnswer: null,
				alert: false
			}
		},
		methods: {
            getQuestion()
            {
            	var token = { 'token' : this.$route.params.token }
	        	Axios.post(`${TestingSystemAPI}/api/session/`, token, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: {}
		        }).then((data) => {

					Axios.get(`${TestingSystemAPI}/api/session-q/`, {
			            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			            params: { 'token' : this.$route.params.token }
			        }).then((qdata) => {

			        	if (!qdata.data[0])
			        		router.push('/tests/'+this.$route.params.token+'/result')

				        this.question = qdata.data[0]

			        	Axios.get(`${TestingSystemAPI}/api/session-a/`, {
				            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
				            params: { 'id' : this.question.id }
				        }).then((adata) => {

				        	this.resAnswers.splice(0)
				        	this.reqAnswers.splice(0)
				            this.resAnswers = adata.data
				            console.log(this.resAnswers)

				            if (this.question.question.answer_type != 1)
					            for (var i = 0; i < this.resAnswers.length; ++i)
					          	    this.reqAnswers.push({
						          		id: this.resAnswers[i].id,
						          		chosen: false
						          	})

				        }).catch(error => {

				          console.log(error)
				        })
			        }).catch(error => {

			          console.log(error)
			        })
		        }).catch(error => {
		        	// ОБРАБОТАТЬ ОКОНЧАНИЕ ПОПЫТОК ТЕСТА
		        	console.log(error)
		        })
            	
            },
            changeCheck(id) {
				for (var i = 0; i < this.reqAnswers.length; ++i)
					if (this.reqAnswers[i].id == id )
						this.reqAnswers[i].chosen = !this.reqAnswers[i].chosen 
            },
            changeRadio(id) {
				for (var i = 0; i < this.reqAnswers.length; ++i) {
					if (this.reqAnswers[i].id == id )
						this.reqAnswers[i].chosen = true
					else this.reqAnswers[i].chosen = false
				}
            },
            setAnswer(){
            	var request = { 'id': this.question.id, 'status': 1, 'answers': this.reqAnswers}
            	console.log(request)
				Axios.post(`${TestingSystemAPI}/api/session-a/`, request, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        }).then(({data}) => {
						window.location.reload(true) 
			        }).catch(error => {
			        	console.log(error)
			        })
            },
            skipAnswer(){
				var request = {'id': this.question.id, 'status': 2}
				Axios.post(`${TestingSystemAPI}/api/session-a/`, request, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        }).then(({data}) => {
						window.location.reload(true) 
			        }).catch(error => {
						window.location.reload(true) 
			        })
            },
            stopTest(){
				var request = {'id': this.question.id, 'status': 3}
				Axios.post(`${TestingSystemAPI}/api/session-a/`, request, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        }).then(({data}) => {
						window.location.reload(true) 
			        }).catch(error => {
						window.location.reload(true) 
			        })
            }
		},
		mounted(){
			this.getQuestion()
		},
		watch: {
			fullAnswer: function(val) {
				this.reqAnswers.splice(0)
				this.reqAnswers.push(this.fullAnswer)
				console.log(this.reqAnswers)
			}
		}
	}
</script>

<style>
	
</style>