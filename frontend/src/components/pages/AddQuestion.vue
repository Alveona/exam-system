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
              		  :rules="rulesTitleLength"
              		  box
		            ></v-text-field>
		        </v-flex>
		        <v-flex xs12>
			        <v-textarea
			            label="Формулировка вопроса"
			            v-model="text"
          		  		:rules="rulesQuestionLength"
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
              			hint="Если не указать, то закончатся, когда обнулятся баллы"
			            ></v-text-field>
				      </v-layout>
		          </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledTimer" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type='number' 
			            :disabled="!enabledTimer"
			            :rules="rulesTimer"
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
                        @input="getUploadedQImage($event)"
			            :dis="!enabledImage"
			            :checked="enabledImage"
			            :label="imageLoadText"
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
                        @input="getUploadedQAudio($event)"
			            :dis="!enabledAudio"
			            :checked="enabledAudio"
			            :label="audioLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				<v-flex xs10>
	              <v-slider
			        v-model="difficulty"
	                :max="maxDifficulty"
	                :min="minDifficulty"
	                label="Сложность вопроса"
	              ></v-slider>
	            </v-flex>
	            <v-flex xs2>
	              <v-text-field
			        v-model="difficulty"
	                type="number"
	                :rules="rulesDifficulty"
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
		            box
		            required
		           ></v-select>
		        </v-flex>

		        <v-flex xs12>
					<add-answers 
						:currentType="currentType"
						:countAnswers="countAnswers"
						:answers="answers"
  						@update:countAnswers="countAnswers = $event"
  						@push="pushAnswer()"
  						@update:answersAudio="getUploadedAudio($event)"
  						@update:answersImage="getUploadedImage($event)"
					></add-answers>
				</v-flex>
							    
				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="successSet ? 'success' : 'error'"
			      	>
			        {{message}}

				    <v-btn v-if="successSet" to="/questions" flat>Вернутьcя к вопросам</v-btn>
				    <v-btn v-if="!successSet" @click.native="onSubmit()" flat>Попробовать еще раз</v-btn>
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

				maxDifficulty: 100,
        		minDifficulty: 1,
        		maxAttempts: 100,
        		minAttempts: 1,
        		minTimer: 10,
        		maxTimer: 3600,
        		maxTitleLength: 100,
        		minTitleLength: 6,
        		maxQuestionLength: 2000,
        		minQuestionLength: 12,
    			title: '',
    			text: '',
      			difficulty: 1,
      			currentType: 1,
				countAnswers: 1,
				attempts: '',
				timer: '',

      			selectedType: [],
      			answerTypes: [
	      			{ id: 1, val: 'Ввод значения'}, 
	      			{ id: 2, val : 'Выбор одного варианта'}, 
	      			{ id: 3, val : 'Выбор нескольких вариантов'}
      			],

        		rulesRequired: [ (value) => !!value || 'Это обязательное поле' ],
        		rulesTitleLength: [ (str) => (str.length >= this.minTitleLength && str.length <= this.maxTitleLength) || 'Допустимая длина: от '+this.minTitleLength + ' до ' + this.maxTitleLength + ' символов' ],
        		rulesQuestionLength: [ (str) => (str.length >= this.minQuestionLength && str.length <= this.maxQuestionLength) || 'Допустимая длина: от '+this.minQuestionLength + ' до ' + this.maxQuestionLength + ' символов' ],
        		rulesDifficulty: [ (value) => (value >= this.minDifficulty && value <= this.maxDifficulty) || 'Введите значение от '+this.minDifficulty+' до '+this.maxDifficulty ],
        		rulesAttempts: [ (value) => (!this.enabledAttempts || value >= this.minAttempts && value <= this.maxAttempts) || 'Введите значение в диапазоне от '+this.minAttempts+' до '+this.maxAttempts ],
        		rulesTimer: [ (value) => (!this.enabledTimer || value >= this.minTimer && value <= this.maxTimer) || 'Введите значение в диапазоне от '+this.minTimer+' до '+this.maxTimer ],
        		
				message: '',
				alert: false,
				successSet: false,

				questionId: '',
				answers: [],

                image: '',
                imageLoadText: 'Изображение к вопросу',

                audio: '',
                audioLoadText: 'Голосовое воспроизведение',
		    }
		  },
		methods: {
            getUploadedQImage(e) {
                this.image = e
            },
            getUploadedQAudio(e) {
                this.audio = e
            },
            getUploadedAudio(obj) {
            	for (var i = 0; i < this.answers.length; ++i)
            		if (i == obj.index)
            		{
            			this.answers[i].audio = obj.audio
            			this.answers[i].push(null)
            			this.answers[i].pop()
            			return
            		}
            },
            getUploadedImage(obj) {
            	for (var i = 0; i < this.answers.length; ++i)
            		if (i == obj.index)
            		{
            			this.answers[i].image = obj.image
            			this.answers[i].push(null)
            			this.answers[i].pop()
            			return
            		}
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
                 var comment = null
                 if (this.currentType == 1)
					comment = this.answers[0].comment
                 formData.set('comment', comment)

                 axios.post(`${TestingSystemAPI}/api/questions/`, formData, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        })
	               .then((response) => {
	               		console.log(response)
	               		this.questionId = response.data.id
	               		for (var i = 0; i < this.answers.length; ++i)
	               			this.answers[i].question = this.questionId


                 		let answersData = new FormData()

		                for (var i = 0; i < this.answers.length; i++)
		                {
		                 	answersData.append('image', this.answers[i].image)
		                 	answersData.append('audio', this.answers[i].audio)
		                 	answersData.append('text', this.answers[i].text)
		                 	answersData.append('priority', this.answers[i].priority)
		                 	answersData.append('correct', this.answers[i].correct)
		                 	if (this.currentType == 2 && !this.answers[i].correct)
		                 	{
		                 		answersData.append('weight', 0)
		                 		alert('hi')
		                 	}
		                 	else answersData.append('weight', this.answers[i].weight)
		                 	answersData.append('hint', this.answers[i].hint)
		                 	answersData.append('question', this.questionId)
		                 }

               			axios.post(`${TestingSystemAPI}/api/answers/`, answersData, {
				          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
				          params: {}
				        })
		               .then(response => {
		               		this.successSet = true
		                    this.alert = true
		                    this.message = 'Вопрос успешно добавлен.'

		                })
		               .catch(error => {
		                    this.alert = true
		                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
		                })
						
	                })
	               .catch(error => {
	                    this.alert = true
	                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
	                })
            },
			reloadPage() {
				window.location.reload(true)
			},
			pushAnswer() {
				var isTrue = false
				if (this.currentType == 1)
					isTrue = true
				this.answers.push({
                	image: null,
                	audio: null,
                	text: null,
                	priority: this.answers.length+1,
                	correct: isTrue,
                	weight: 256,
                	hint: null,
                	comment: null,
                	question: 0,
					enabledAudio: false,
					enabledImage: false
				})
				console.log('countAnswers: '+ this.countAnswers)
            	console.log('array len: ' + this.answers.length)

            	console.log(this.answers)
			}
       },
       watch: {
       		currentType: function(val){
       			if (val == 1)
       				this.countAnswers = 1
       			else if (val == 2 || val == 3)
       				this.countAnswers = 2

       			this.answers.splice(0)
       			while (this.answers.length < this.countAnswers)
       					this.pushAnswer()
				console.log('countAnswers: '+ this.countAnswers)
            	console.log('array len: ' + this.answers.length)
       		},
       		enabledImage: function(val) {
       			if (!val)
       				this.image = ''
       		},
       		enabledAudio: function(val) {
       			if (!val)
       				this.audio = ''
       		},
       		attempts: function(val) {
   				if (this.enabledAttempts)
       				this.attempts = val
       			else this.attempts = null
       		},
       		timer: function(val) {
   				if (this.enabledTimer)
       				this.timer = val
       			else this.timer = null
       		}
       },
       mounted() {
       		this.pushAnswer()
       }
	}
</script>

<style>
</style>