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

			      <v-flex xs12 v-for="mode in modes">
					<div class="divider"></div>
					<v-layout row wrap>
						<v-flex xs12 sm6>
							<p class="title">{{modes.indexOf(mode) + 1}}. Режим: {{mode.name}}</p>
						</v-flex>
					</v-layout>

					<v-layout row wrap>
						<v-flex xs12 sm6 px-2>
			            <v-label>Видео к вопросу</v-label>
			              <v-text-field
			                type="text"
			                v-model="videos[modes.indexOf(mode)]"
			                :rules="[rules.video]"
			                clearable
			                solo
			              ></v-text-field>
			            </v-flex>

					  <v-flex xs12 sm6 px-4>
			            <v-label>Голосовое воспроизведение</v-label>
	        			<v-layout align-center>
				          	<v-checkbox @click.native="changeQAudio(modes.indexOf(mode))" v-model="enabledAudio[modes.indexOf(mode)]" hide-details class="shrink mr-2"></v-checkbox>
				            <file-input 
				            class="fileBtn"
		                    accept="audio/*"
		                    ref="fileInput"
	                        @input="getUploadedQAudio($event, modes.indexOf(mode))"
				            :dis="!enabledAudio[modes.indexOf(mode)]"
				            :checked="enabledAudio[modes.indexOf(mode)]"
				            :label="audioLoadText[modes.indexOf(mode)]"
				            ></file-input>
				        </v-layout>
				      </v-flex>
					</v-layout>

				      
			        </v-flex>
				<div class="divider"></div>

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
						:modes="modes"
  						@update:countAnswers="countAnswers = $event"
  						@update:answersQty="answersQty = $event"
  						@push="pushAnswer()"
  						@update:answersAudio="getUploadedAudio($event)"
  						@update:answersImage="getUploadedImage($event)"
  						@update:clickHintTooltip="clickHintTooltip($event)"
  						@update:clickVideoTooltip="clickVideoTooltip($event)"
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
        		maxVideoLength: 150,
    			title: '',
    			text: '',
      			difficulty: 1,
      			currentType: 1,
				countAnswers: 1,
				attempts: null,
				timer: null,
				answersQty: 1,
				showTitleTooltip: false,
				showTextTooltip: false,
				showAttemptsTooltip:false,
				showTimerTooltip:false,
				showQuestionTooltip:false,
				showTypeTooltip:false,

				modes: [],
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
                	video: str => (str.length <= this.maxVideoLength) || 'Допустимая длина не более '+this.maxVideoLength + ' символов',
                },
        		
				message: '',
				alert: false,
				successSet: false,
				valid: false,

				questionId: '',
				answers: [],
				enabledAudio:[],
				videos:[],
				audios:[],
				audioLoadText:[],

                image: '',
                imageLoadText: 'Изображение к вопросу',
		    }
		  },
		methods: {
            getUploadedQImage(e) {
                this.image = e
            },
            getUploadedQAudio(e, mode) {
                this.audios[mode] = e
            },
            getUploadedAudio(obj) {
    			this.answers[obj.index].audios[obj.mode] = obj.audio
            },
            getUploadedImage(obj) {
    			this.answers[obj.index].image = obj.image
            },
            clickHintTooltip(obj){
				this.answers[obj.answer].showHintTooltip[obj.mode] = !this.answers[obj.answer].showHintTooltip[obj.mode]
				this.answers[obj.answer].showHintTooltip.push(null)
				this.answers[obj.answer].showHintTooltip.pop()
            },
            clickVideoTooltip(obj){
				this.answers[obj.answer].showVideoTooltip[obj.mode] = !this.answers[obj.answer].showVideoTooltip[obj.mode]
				this.answers[obj.answer].showVideoTooltip.push(null)
				this.answers[obj.answer].showVideoTooltip.pop()
            },
            changeQAudio(mode){
            	if (!this.enabledAudio[mode])
       				this.audios[mode] = null
            },
            onSubmit() {
            	/*
            	let hintQuestionData = new FormData()
                 	for (var j = 0; j < this.modes.length; j++)
                 	{
                 		hintQuestionData.append('audio', this.audios[j])
                 		hintQuestionData.append('video', this.videos[j])
                 		var object = {};
						hintQuestionData.forEach(function(value, key){
						    object[key] = value;
						});
						var json = JSON.stringify(object);
		                 console.log(json)
                 	}
            	for (var i = 0; i < this.answers.length; i++)
		        {
		        	let hintAnsData = new FormData()
                 	for (var j = 0; j < this.modes.length; j++)
                 	{
                 		hintAnsData.append('id', this.modes[j].id)
                 		hintAnsData.append('hint', this.answers[i].hints[j])
                 		hintAnsData.append('enabledAudio', this.answers[i].enabledAudio[j])
                 		hintAnsData.append('audio', this.answers[i].audios[j])
                 		var object = {};
						hintAnsData.forEach(function(value, key){
						    object[key] = value;
						});
						var json = JSON.stringify(object);
		                 console.log(json)
                 	}
		        }
		        */
	        	if (!this.$refs.addQform.validate())
	        	{
               		this.successSet = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successSet)
	        		return
                let questionData = new FormData()

                questionData.set('text', this.text)
                questionData.set('title', this.title)
                questionData.set('attempts_number', this.attempts)
                questionData.set('timer', this.timer)
                questionData.set('answer_type', this.currentType)
                questionData.set('answers_number', this.answersQty)
                questionData.set('difficulty', this.difficulty)
                questionData.set('image', this.image)
                let comment = null
                if (this.currentType == 1)
					comment = this.answers[0].comment
                questionData.set('comment', comment)

                axios.post(`${TestingSystemAPI}/api/questions/`, questionData, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        })
                .then((response) => {
               		this.questionId = response.data.id

               		for (let i = 0; i < this.modes.length; i++)
               		{
               			console.log('im here')
            			let QMediaData = new FormData()
		                QMediaData.set('question', this.questionId)
		                QMediaData.set('mode', this.modes[i].id)
		                QMediaData.set('audio', this.audios[i])
		                QMediaData.set('video', this.videos[i])

						let object = {};
						QMediaData.forEach(function(value, key){
						    object[key] = value;
						});
						let json = JSON.stringify(object);
		                 console.log(json)

						axios.post(`${TestingSystemAPI}/api/questions_media/`, QMediaData, {
					          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
					          params: {}
					        })
				        .then((response) => {
				        	console.log(this.questionId + ' ' + this.modes[i].id + ' success questions_media')
				        	if (i != this.modes.length - 1)
				        		return
			           		for (let j = 0; j < this.answers.length; ++j)
			           			this.answers[j].question = this.questionId

			         		let answersData = new FormData()
			                for (let j = 0; j < this.answers.length; j++)
			                {
			                 	answersData.append('image', this.answers[j].image)
			                 	answersData.append('text', this.answers[j].text)
			                 	if (this.currentType != 2 )
			                 		answersData.append('priority', this.answers[j].priority)
			                 	else 
			                 	{
			                 		if (this.answers[j].correct)
			                 			answersData.append('priority', this.answers.length)
			                 		else answersData.append('priority', j + 1)
			                 	}
			                 	answersData.append('correct', this.answers[j].correct)
			                 	if (this.currentType == 2 && !this.answers[j].correct)
			                 		answersData.append('weight', 0)
			                 	else answersData.append('weight', this.answers[j].weight)
			                 	answersData.append('question', this.questionId)

			         			
			                 }

	               			axios.post(`${TestingSystemAPI}/api/answers/`, answersData, {
					          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
					          params: {}
					        })
			               .then(response => {
			               		let ans = response.data.answers
			               		console.log(ans)
			               		if (ans.length != this.answers.length)
			               		{
			               			console.log('server response length error')
				               		this.successSet = false
				                    this.alert = true
				                    this.message = 'Не удалось добавить вопрос. Произошла ошибка.'
			               			return
			               		}

			               		for (let i = 0; i < ans.length; i++)
			               		{
			               			for (let j = 0; j < this.modes.length; j++)
			               			{
			               				console.log('start of end'+this.modes.length)
			                			let AHintData = new FormData()
						                AHintData.set('answer', ans[i])
						                AHintData.set('mode', this.modes[j].id)
						                AHintData.set('audio', this.answers[i].audios[j])
						                AHintData.set('video', this.answers[i].videos[j])
						                AHintData.set('text', this.answers[i].hints[j])

										let object = {};
										AHintData.forEach(function(value, key){
										    object[key] = value;
										});
										let json = JSON.stringify(object);
						                console.log(json)

				               			axios.post(`${TestingSystemAPI}/api/answers_hint/`, AHintData, { 
								          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
								          params: {}
								        })
								        .then((response) => {
								        	console.log(ans[i] + ' ' + this.modes[j].id + ' success answers_hint')
								        	if (i == ans.length - 1 && j == this.modes.length - 1)
								        	{
							               		this.successSet = true
							                    this.alert = true
							                    this.message = 'Вопрос успешно добавлен.'
								        	}
								        })
						               .catch(error => {
						               		this.successSet = false
						                    this.alert = true
						                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
						                    return
						                })
						           }
			               		}
			                })
			               .catch(error => {
			               		this.successSet = false
			                    this.alert = true
			                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
			                })



				        	
				        })
		                .catch(error => {
		               		this.successSet = false
		                    this.alert = true
		                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.111'
		                    return
		                })
		            }

				
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
					audios:[],
					hints:[],
					videos:[],
					enabledAudio:[],
					audioLoadText:[],
					showHintTooltip:[],
					showVideoTooltip:[],
                	image: null,
                	text: null,
                	priority: this.answers.length+1,
                	correct: isTrue,
                	weight: weight,
                	comment: null,
                	question: 0,
					enabledImage: false,
					imageLoadText: 'Изображение не загружено',
					show: false,
				})
				for (var i = 0; i < this.modes.length; i++){
					this.answers[this.answers.length - 1].audios.push(null)
					this.answers[this.answers.length - 1].enabledAudio.push(false)
					this.answers[this.answers.length - 1].showHintTooltip.push(false)
					this.answers[this.answers.length - 1].showVideoTooltip.push(false)
					this.answers[this.answers.length - 1].videos.push('')
					this.answers[this.answers.length - 1].audioLoadText.push('Аудио не загружено')
					this.answers[this.answers.length - 1].hints.push('')
				}
			},
			hideAlert() {
				this.alert = false
			},
			startTimer() {
				setTimeout(this.hideAlert, 4000)
			},
			getModeData(){				
				axios.get(`${TestingSystemAPI}/api/strict_modes/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.modes = data
		          this.successLoad = true

		          for (var i = 0; i < this.modes.length; i++)
		          {
		          	this.enabledAudio[i] = false
		          	this.videos[i] = ''
		          	this.audios[i] = null
		          	this.audioLoadText[i] = 'Аудиозапись не загружена'
		          }

       			  this.pushAnswer()

		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось получить список режимов. Проверьте подключение к сети.'
		        })
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
       		this.getModeData()
       }
	}
</script>

<style>
	.divider{
		height:1px;
		width:100%;
		background: #bbb;
		margin-bottom:15px;
	}
</style>