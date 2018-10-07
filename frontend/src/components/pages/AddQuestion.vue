<template>
	<v-form>
		<v-container>
			<v-layout row wrap>
				<h4 class="display-1">Добавление нового вопроса</h4>
				<v-flex xs12>
		            <v-text-field
		              label="Краткое название (будет видно только вам)"
		              v-model="title"
		              required
              		  clearable
              		  :rules="rules"
              		  box
		            ></v-text-field>
		        </v-flex>
		        <v-flex xs12>
			        <v-textarea
			            name="input-7-1"
			            label="Формулировка вопроса"
			            v-model="text"
			            hint="Не более 2000 символов"
          		  		:rules="rules"
			            required
              			clearable
              			box
			          ></v-textarea>
		        </v-flex>

		          <v-flex xs12 sm6 xl3>
	        			<v-layout align-center>
			          	<v-checkbox v-model="enabledAttempts" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field 
			            type='number' 
			            :disabled="!enabledAttempts"
			            label="Количество попыток"
			            v-model="attempts"
              			clearable
              			box
			            ></v-text-field>
				      </v-layout>
		          </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledTimer" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type='number' 
			            :disabled="!enabledTimer"
			            label="Таймер на вопрос"
			            v-model="timer"
              			clearable
              			box
			            hint="В секундах"
			            ></v-text-field>
			        </v-layout>
			      </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledImage" hide-details class="shrink mr-2" ></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="image/*"
	                    ref="fileInput"
                        @input="getUploadedImage"
			            :dis="!enabledImage"
			            :label="imageLoadText"
			            v-model="image"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				  <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledAudio" hide-details class="shrink mr-2"></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="audio/*"
	                    ref="fileInput"
                        @input="getUploadedAudio"
			            :dis="!enabledAudio"
			            :label="audioLoadText"
			            v-model="audio"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				<v-flex xs10>
	              <v-slider
			        v-model="difficulty"
	                :max="100"
	                label="Сложность вопроса"
	              ></v-slider>
	            </v-flex>
	            <v-flex xs2>
	              <v-text-field
			        v-model="difficulty"
	                type="number"
	                box
	              ></v-text-field>
	            </v-flex>

				<v-flex xs12>
		          <v-select
		            v-model="currentType"
		            :items="answerTypes"
		            item-value="id"
		            item-text="val"
			        label="Тип ответа"
      		  		:rules="rules"
		            box
		            required
		           ></v-select>
		        </v-flex>

		        <v-flex xs12>
					<add-answers 
						:currentType="currentType"
						:countAnswers="countAnswers"
						:answers="answers"
					></add-answers>
				</v-flex>
							    
				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="success ? success : error"
			      	>
			        {{message}}

				    <v-btn v-if="success" to="/questions" flat>Вернутьcя к вопросам</v-btn>
				    <v-btn v-if="!success" @click.native="onSubmit()" flat>Попробовать еще раз</v-btn>
			      </v-alert>
		      </v-flex>	

		      <v-flex xs12>
					<v-btn round color="success" @click.native="onSubmit()" dark large>
						 Добавить вопрос
					</v-btn>
				</v-flex>

			</v-layout>
		</v-container>
	</v-form>
</template>

<script>
    import axios from 'axios'
	import router from '@/router'
    import FileInput from '@/components/other/FileLoader.vue'
    import AddAnswers from '@/components/boxes/AddAnswers.vue'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
        components: { FileInput, AddAnswers },

		data () {
		    return {
		    	enabledAttempts: false,
			    enabledTimer: false,
			    enabledImage: false,
			    enabledAudio: false,

      			selectedType: [],
      			answerTypes: [
	      			{ id: 1, val: 'Ввод значения'}, 
	      			{ id: 2, val : 'Выбор одного варианта'}, 
	      			{ id: 3, val : 'Выбор нескольких вариантов'}
      			],
        		rules: [ (value) => !!value || 'Это обязательное поле' ],
    			title: '',
    			text: '',
    			attempts: '',
    			timer: '',
      			difficulty: 0,
      			currentType: 1,
				countAnswers: 1,

				message: '',
				alert: false,
				success: false,

				questionId: '',
				answers: [{
				'0' : {
                	image: '',
                	audio: '',
                	text: '',
                	priority: 1,
                	correct: true,
                	weight: 256,
                	hint: '',
                	comment: ''
				}}],

                image: '',
                imageLoadText: 'Изображение к вопросу',

                audio: '',
                audioLoadText: 'Голосовое воспроизведение',
		    }
		  },
		methods: {
            getUploadedImage(e) {
                this.image = e
            },
            getUploadedAudio(e) {
                this.audio = e
            },
            onSubmit() {
                 let formData = new FormData()

                 formData.set('text', this.text)
                 formData.set('title', this.title)
                 formData.set('attempts_number', this.attempts)
                 formData.set('timer', this.timer)
                 formData.set('answer_type', this.currentType)
                 formData.set('answers_number', this.countAnswers)
                 formData.set('difficulty', this.difficulty)
                 formData.set('image', this.image)
                 formData.set('audio', this.audio)

                 axios.post(`${TestingSystemAPI}/api/questions/`, formData, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        })
	               .then((response) => {
	               		console.log(response)
	               		this.questionId = response.data.id
	               		console.log(this.questionId)
	               		console.log(this.answers.length)
	               		console.log(this.answers)
	               		//for (var i = 0; i < this.answers.length; ++i)
	               		//{
	               			//this.answers.question = this.questionId
	               			axios.post(`${TestingSystemAPI}/api/answers/`, this.answers, {
					          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
					          params: {}
					        })
			               .then(response => {
			               		this.success = true
			                    this.alert = true
			                    this.message = 'Вопрос успешно добавлен.'
			                })
			               .catch(error => {
			               		this.success = false
			                    this.alert = true
			                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
			                })
	               		//}
						
	                })
	               .catch(error => {
	               		this.success = false
	                    this.alert = true
	                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
	                })
            },
			reloadPage() {
				window.location.reload(true)
			}
       },
       watch: {
       		currentType: function(val){
       			if (val == 1)
       				this.countAnswers = 1
       			else if (val == 2 || val == 3)
       				this.countAnswers = 2
       		}
       }
	}
</script>

<style>
</style>