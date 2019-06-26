<template>
<v-layout row wrap>

	<v-flex xs12>
		<p class="title text-md-center">Вопрос {{question.order_number}}.</p>
	</v-flex>

	<v-layout row justify-space-around v-if="question.media.video != ''">
		<iframe width="720" height="406" :src="question.media.video" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
	</v-layout>

	

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

	<v-flex xs12 v-if="!!question.media.audio && question.media.video == ''" class="mb-4" > 
		<vue-audio :file="question.media.audio" :autoPlay="!!question.audio_hint ? false : true"/>
	</v-flex>

	<v-flex v-if="question.question.answer_type == 1" xs12>
        <v-text-field 
          label="Ответ"
          v-model="fullAnswer"
          required
  		  clearable
  		  box
        ></v-text-field>
	</v-flex>

	<v-flex v-else-if="question.question.answer_type == 2" xs12>
		<v-radio-group>
			<v-layout wrap col>
				<v-flex xs12 sm6 md4 px-1 v-if="!!answer.answer.image" v-for="answer in resAnswers">
			        <v-img 
			        	:src="answer.answer.image"
		        		:aspect-ratio="16/9" 
			            position="center center"
			        ></v-img>
			        <p class="testingRadioLabel">
				    	<v-label>{{answer.answer.text}}</v-label>
				    </p>
					<v-radio
					  class="testingRadio"
			          :value="answer.id"
			          @change="changeRadio(answer.id)"
			        ></v-radio>
				</v-flex>
				<v-flex xs12 v-else>
					<v-radio
					  :label="answer.answer.text"
			          :value="answer.id"
			          @change="changeRadio(answer.id)"
			        ></v-radio>
			    </v-flex>
			</v-layout>
	    </v-radio-group>
	</v-flex>

	<v-flex v-else-if="question.question.answer_type == 3" xs12>
		<v-layout wrap col>
			<v-flex xs12 sm6 md4 px-1 v-for="answer in resAnswers" v-if="!!answer.answer.image">
		        <v-img 
		        	:src="answer.answer.image"
	        		:aspect-ratio="16/9" 
		            position="center center"
		        ></v-img>
		        <p class="testingRadioLabel">
			    	<v-label >{{answer.answer.text}}</v-label>
			    </p>
				<v-checkbox 
			 	  class="testingRadio"
				  :value="answer.id"
				  v-model="changedChecks"
				  @change="changeCheck(answer.id)"
				></v-checkbox>
			</v-flex>
			<v-flex xs12 v-else>
				<v-checkbox 
				  :label="answer.answer.text"
				  :value="answer.id"
				  v-model="changedChecks"
				  @change="changeCheck(answer.id)"
				></v-checkbox>
			</v-flex>
		</v-layout>
	</v-flex>

	<v-flex xs12 v-if="question.hint || question.audio_hint || question.video_hint">
	 	<p class="title">Комментарий к вашему ответу:</p>
	</v-flex>

	<v-layout row justify-space-around v-if="question.video_hint">
		<iframe width="720" height="406" :src="question.video_hint" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
	</v-layout>

	<v-flex xs12 v-if="question.audio_hint && !question.video_hint" class="mb-4"> 
		<vue-audio :file="question.audio_hint" :autoPlay="!!question.audio_hint ? true : false"/>
	</v-flex>

		<v-flex xs12 v-if="question.hint"> 
		  <v-alert 
	        :value="true"
	        type="warning"
	      >
		      <v-layout row wrap>
			    <v-flex xs3>
				    <v-img 
				    	:src="question.mode_image"
						:aspect-ratio="1/1" 
						width="100"
				        position="center center"
				    ></v-img>
				</v-flex>
			    <v-flex xs9 class="title">
			        {{question.hint}}
			    </v-flex>
			</v-layout>
	      </v-alert>
		</v-flex>

	<v-layout row justify-space-around>

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
			alert: false,
			changedChecks: []
		}
	},
	methods: {
        getQuestion(q, callback)
        {
        	console.log('getQuestion function: ')
        	var token_mode = { 'token' : this.$route.params.token, 'mode' :  this.$route.params.mode}
        	console.log(token_mode)
        	Axios.post(`${TestingSystemAPI}/api/session/`, token_mode, {
	            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
	            params: {}
	        }).then((data) => {
	        	console.log('getQuestion function 2: ')
				Axios.get(`${TestingSystemAPI}/api/session-q/`, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: { 'token' : this.$route.params.token }
		        }).then((qdata) => {
		        	console.log('getQuestion function 3: ')
		        	if (!qdata.data[0])
		        		router.push('/tests/'+this.$route.params.token+'/result')

			        this.question = qdata.data[0]
			        console.log('this.question')
			        console.log(this.question)
			        
				    if (this.question.media.video)
			        	this.question.media.video = 'https://youtube.com/embed/' + this.question.media.video + '?autoplay=1'
				    if (this.question.video_hint)
				        this.question.video_hint = 'https://youtube.com/embed/' + this.question.video_hint + '?autoplay=1'
				    
				    
				    if (this.question.audio_hint && this.question.audio_hint.substring(this.question.audio_hint.length - 4) == "null")
				    	this.question.audio_hint = null
				    if (this.question.media.audio && this.question.media.audio.substring(this.question.media.audio.length - 4) == "null")
				    	this.question.media.audio = null
				    else if (this.question.media.audio)
				    	this.question.media.audio = TestingSystemAPI + this.question.media.audio
				    console.log(this.question.media.audio)
				    

		        	Axios.get(`${TestingSystemAPI}/api/session-a/`, {
			            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			            params: { 'id' : this.question.id }
			        }).then((adata) => {

			        	this.resAnswers.splice(0)
			        	this.reqAnswers.splice(0)
			            this.resAnswers = adata.data
			            
			            console.log(this.resAnswers)
			            
						console.log('setting to default')
						console.log(this.reqAnswers)
			            if (this.question.question.answer_type != 1)
				            for (var i = 0; i < this.resAnswers.length; ++i)
				            {
				          	    this.reqAnswers.push({
					          		id: this.resAnswers[i].id,
					          		chosen: false
					          	})
				          	}
			          	if (this.question.id == q)
			          		callback(false)
			          	else
			          		callback(true)
			        }).catch(error => {

			          console.log(error)
			        })
		        }).catch(error => {

		          console.log(error)
		        })
	        }).catch(error => {
	        	router.push('/tests/'+this.$route.params.token+'/end')
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
					//window.location.reload(true)
					var arr = []
					console.log('req_ans: ') 
					console.log(this.reqAnswers)
					console.log(this.resAnswers)
					for (var i = 0; i < this.reqAnswers.length; ++i)
					{
						arr.push( this.reqAnswers[i])
						console.log(this.reqAnswers[i])
						console.log(arr[i])
					}
					console.log('arr: ')	
					for(var i =0; i < arr.length; i++)
						console.log(arr[i])
					console.log(arr)	
					
					this.getQuestion(this.question.id, (changed) => {
						console.log('after getQ:')
						console.log(this.reqAnswers)
						if(!changed){
							for(var i = 0; i<arr.length; i++)
							{
								this.reqAnswers[i] = arr[i]
								if (this.reqAnswers[i].chosen)
									this.changedChecks.push(this.reqAnswers[i].id)
								console.log(this.reqAnswers[i])	
							}
						}
						else this.changedChecks = []
						//this.reqAnswers = arr
						console.log(this.reqAnswers)
					})
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
		this.getQuestion(function(){})
	},
	watch: {
		fullAnswer: function(val) {
			this.reqAnswers.splice(0)
			this.reqAnswers.push(this.fullAnswer)
			console.log('full ans:')
			console.log(this.reqAnswers)
		}
	}
}
</script>

<style>

</style>