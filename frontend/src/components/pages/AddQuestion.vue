<template>
	<v-form ref="addQform" v-model="valid">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
					<v-layout row wrap>
						<h4 class="display-1">Создание нового вопроса</h4>
						<v-tooltip bottom v-model="showQuestionTooltip">
					        <v-btn slot="activator" @click="showQuestionTooltip = !showQuestionTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
					        <span>Сейчас вы создаете новый вопрос, который впоследствие может быть добавлен в ваши курсы. В процессе прохождения теста пользователь сможет отвечать в один момент времени только на один вопрос.</span>
						</v-tooltip>
					</v-layout>
				</v-flex>

				<v-flex xs12>
					<v-label>Краткое название вопроса</v-label>
					<v-tooltip bottom v-model="showTitleTooltip">
				        <v-btn slot="activator" @click="showTitleTooltip = !showTitleTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Поле будет видно только вам в списке добавленных вопросов для удобства навигации по ним.</span>
		        	</v-tooltip>
		            <v-text-field
		              v-model="title"
		              placeholder="Например, 'Задание по линейным уравнениям'"
		              required
              		  clearable
              		  :rules="[rules.title]"
              		  solo
		            ></v-text-field>
		        </v-flex>
		        <v-flex xs12>
					<v-label>Формулировка вопроса</v-label>
					<v-tooltip bottom v-model="showTextTooltip">
				        <v-btn slot="activator" @click="showTextTooltip = !showTextTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Поле формулировки вопроса должно содержать полную постановку задачи.</span>
		        	</v-tooltip>
			        <v-textarea
			            placeholder="Например, 'Найдите корень уравнения 2x - 5 = 14.'"
			            v-model="text"
          		  		:rules="[rules.question]"
			            required
              			clearable
              			solo
			          ></v-textarea>
		        </v-flex>
		          <v-flex xs12 sm6 xl3>
	        	  	  <v-layout align-center>
	        	  	  	<v-label>Количество попыток</v-label>
						<v-tooltip bottom v-model="showAttemptsTooltip">
					        <v-btn slot="activator" @click="showAttemptsTooltip = !showAttemptsTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
					        <span>Необязательное поле. Если не указать количество попыток, то они закончатся, когда обнулятся баллы.</span>
			        	</v-tooltip>
			          </v-layout>
	        	  	  <v-layout align-center>
			          	<v-checkbox v-model="enabledAttempts" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field 
				            type='number' 
				            :disabled="!enabledAttempts"
	          		  		:rules="[rules.attempts]"
				            v-model="attempts"
	              			clearable
	              			solo
	              			persistent-hint
			            ></v-text-field>
				      </v-layout>
		          </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
	        	  	  	<v-label>Таймер на вопрос</v-label>
						<v-tooltip bottom v-model="showTimerTooltip">
					        <v-btn slot="activator" @click="showTimerTooltip = !showTimerTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
					        <span>Необязательное поле. Если не указать таймер - время на ответ будет неограниченно. Значение указывается в секундах</span>
			        	</v-tooltip>
			          </v-layout>
	        	  	  <v-layout align-center>
			          	<v-checkbox v-model="enabledTimer" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type='number' 
			            :disabled="!enabledTimer"
			            :rules="[rules.timer]"
			            v-model="timer"
              			clearable
              			solo
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
	                :rules="[rules.difficulty]"
	                solo
	              ></v-text-field>
	            </v-flex>

				<v-flex xs12>
	    	  	  	<v-label>Тип ответов</v-label>
					<v-tooltip bottom v-model="showTypeTooltip">
				        <v-btn slot="activator" @click="showTypeTooltip = !showTypeTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Выберите один из трех типов ответов, которые должен дать пользователь на вопрос. Тип "ввод значения" означает, что пользователь должен ввести ответ сам. Тип "выбор одного варианта" означает, что у пользователя будет выбор из нескольких ответов, и он должен указать только один верный. Тип "выбор нескольких вариантов" означает, что у пользователя будет выбор из нескольких ответов, и он должен отметить среди них верные (должно быть от 1 верного варианта до количества, равного количеству вариантов ответов). </span>
		        	</v-tooltip>
		            <v-select
			            v-model="currentType"
			            :items="answerTypes"
			            item-value="id"
			            item-text="val"
				        label="Тип ответа"
			            solo
			            required
		            ></v-select>
		        </v-flex>

		        <v-flex xs12>
					<add-answers 
						:currentType="currentType"
						:countAnswers="countAnswers"
						:answers="answers"
						:answersQty="answersQty"
  						@update:countAnswers="countAnswers = $event"
  						@update:answersQty="answersQty = $event"
  						@push="pushAnswer()"
  						@update:answersAudio="getUploadedAudio($event)"
  						@update:answersImage="getUploadedImage($event)"
  						@update:changeAudio="changeAudio($event)"
  						@update:changeImage="changeImage($event)"
					></add-answers>
				</v-flex>
							    
				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="successSet ? 'success' : 'error'"
        			transition="scale-transition"
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
				answersQty: 1,
				showTitleTooltip: false,
				showTextTooltip: false,
				showAttemptsTooltip:false,
				showTimerTooltip:false,
				showQuestionTooltip:false,
				showTypeTooltip:false,

      			selectedType: [],
      			answerTypes: [
	      			{ id: 1, val: 'Ввод значения'}, 
	      			{ id: 2, val : 'Выбор одного варианта'}, 
	      			{ id: 3, val : 'Выбор нескольких вариантов'}
      			],

                rules: {
                	required: value => !!value || 'Это необходимое поле',
                	title: str => (str.length >= this.minTitleLength && str.length <= this.maxTitleLength) || 'Допустимая длина: от '+this.minTitleLength + ' до ' + this.maxTitleLength + ' символов',
                	question: str => (str.length >= this.minQuestionLength && str.length <= this.maxQuestionLength) || 'Допустимая длина: от '+this.minQuestionLength + ' до ' + this.maxQuestionLength + ' символов',
                	difficulty: value => (value >= this.minDifficulty && value <= this.maxDifficulty) || 'Введите значение от '+this.minDifficulty+' до '+this.maxDifficulty,
                	attempts: value => (!this.enabledAttempts || value >= this.minAttempts && value <= this.maxAttempts) || 'Введите значение в диапазоне от '+this.minAttempts+' до '+this.maxAttempts,
                	timer: value => (!this.enabledTimer || value >= this.minTimer && value <= this.maxTimer) || 'Введите значение в диапазоне от '+this.minTimer+' до '+this.maxTimer,
                },
        		
				message: '',
				alert: false,
				successSet: false,
				valid: false,

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
            changeAudio(ind){
            },
            changeImage(ind){
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

	        	if (!this.$refs.addQform.validate())
	        	{
               		this.successSet = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successSet)
	        		return
                let formData = new FormData()

                formData.set('text', this.text)
                formData.set('title', this.title)
                formData.set('attempts_number', this.attempts)
                formData.set('timer', this.timer)
                formData.set('answer_type', this.currentType)
                formData.set('answers_number', this.answersQty)
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
		                 	if (this.currentType != 2 )
		                 		answersData.append('priority', this.answers[i].priority)
		                 	else 
		                 	{
		                 		if (this.answers[i].correct)
		                 			answersData.append('priority', this.answers.length)
		                 		else answersData.append('priority', i + 1)
		                 	}
		                 	answersData.append('correct', this.answers[i].correct)
		                 	if (this.currentType == 2 && !this.answers[i].correct)
		                 		answersData.append('weight', 0)
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
		                    setTimeout(this.goBack, 1200)

		                })
		               .catch(error => {
		               		this.successSet = false
		                    this.alert = true
		                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
		                })
						
	                })
	               .catch(error => {
	                    this.alert = true
		               	this.successSet = false
	                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
	                })
            },
			reloadPage() {
				window.location.reload(true)
			},
			goBack() {
				router.push('/questions')
			},
			pushAnswer() {
				var isTrue = false
				var weight = 256
				if (this.currentType == 1)
					isTrue = true
				if (this.currentType == 3)
					weight = 0
				this.answers.push({
                	image: null,
                	audio: null,
                	text: null,
                	priority: this.answers.length+1,
                	correct: isTrue,
                	weight: weight,
                	hint: null,
                	comment: null,
                	question: 0,
					enabledAudio: false,
					enabledImage: false,
					show: false,
				})
				console.log('countAnswers: '+ this.countAnswers)
            	console.log('array len: ' + this.answers.length)

            	console.log(this.answers)
			},
			hideAlert() {
				this.alert = false
			},
			startTimer() {
				setTimeout(this.hideAlert, 4000)
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
       		enabledAttempts: function(val) {
       			if (val)
       				this.attempts = 3
       			else this.attempts = ''
       		},
       		enabledTimer: function(val) {
       			if (val)
       				this.timer = 60
       			else this.timer = ''
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
       		},
			alert: function(val) {
				if (val)
					this.startTimer()
			}
       },
       mounted() {
       		this.pushAnswer()
       }
	}
</script>

<style>
</style>