<template>
	<v-form ref="editQform">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
					<v-layout row wrap>
						<h4 class="display-1">Редактирование вопроса</h4>
					</v-layout>
				</v-flex>

				<v-flex xs12 mt-3>
					<v-label>Краткое название</v-label>
					<v-tooltip bottom v-model="showTitleTooltip">
				        <v-btn slot="activator" @click="showTitleTooltip = !showTitleTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Поле будет видно только вам в списке добавленных вопросов для удобства навигации по ним.</span>
		        	</v-tooltip>
		            <v-text-field
		              v-model="question.title"
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
			            v-model="question.text"
			            placeholder="Например, 'Найдите корень уравнения 2x - 5 = 14.'"
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
				            type="number"
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
    				<v-label>Изображение к вопросу</v-label>
    				<v-tooltip bottom v-model="showImageTooltip">
				        <v-btn slot="activator" @click="showImageTooltip = !showImageTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Необязательное поле. Будет отображаться вместе с формулировкой вопроса.</span>
		        	</v-tooltip>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledImage" hide-details class="shrink mr-2" ></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="image/*"
	                    ref="fileInput"
                        @input="getUploadedQImage($event)"
                        @update:deleteFile="deleteFile(0)"
			            :dis="!enabledImage"
			            :checked="enabledImage"
			            :label="imageLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>
<!--
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
-->
<!--
			      <v-flex xs12>
				      <v-label>Замена изображения и аудио:</v-label>
				      <v-tooltip bottom v-model="showMediaTooltip">
					    <v-btn slot="activator" @click="showMediaTooltip = !showMediaTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
					    <span>Если вы хотите оставить изображение или аудио без изменений, убедитесь, что галочки ниже не отмечены. Если же хотите удалить их, отметьте галочку, но не загружайте новый файл. Для изменения изображения или аудио загрузите новый файл.</span>
			          </v-tooltip>
			      </v-flex>
-->
		         
				<v-flex xs12 v-for="mode in modes">
				  <div class="divider"></div>
				  <v-layout row wrap>
						<v-flex xs12 sm6>
							<p class="title">{{modes.indexOf(mode) + 1}}) Режим: {{mode.name}}</p>
						</v-flex>
					</v-layout>

					<v-layout row wrap>
						<v-flex xs12 sm6 px-2>
			            <v-label>Видео к вопросу (id видео на Youtube)</v-label>
			              <v-text-field
			                type="text"
			                v-model="videos[modes.indexOf(mode)]"
			                placeholder="например, _5k9NMCQ088"
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
                        	@update:deleteFile="deleteFile(1, modes.indexOf(mode))"
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
			        v-model="question.difficulty"
	                :max="maxDifficulty"
	                :min="minDifficulty"
	                label="Сложность вопроса"
	              ></v-slider>
	            </v-flex>
	            <v-flex xs2>
	              <v-text-field
			        v-model="question.difficulty"
	                type="number"
	                :rules="[rules.difficulty]"
	                solo
	              ></v-text-field>
	            </v-flex>
<!--
				<v-flex xs12>
	    	  	  <v-label>Тип ответов</v-label>
	    	  	  <v-tooltip bottom v-model="showTypeTooltip">
				        <v-btn slot="activator" @click="showTypeTooltip = !showTypeTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Выберите один из трех типов ответов, которые должен дать пользователь на вопрос. Тип "ввод значения" означает, что пользователь должен ввести ответ сам. Тип "выбор одного варианта" означает, что у пользователя будет выбор из нескольких ответов, и он должен указать только один верный. Тип "выбор нескольких вариантов" означает, что у пользователя будет выбор из нескольких ответов, и он должен отметить среди них верные (должно быть от 1 верного варианта до количества, равного количеству вариантов ответов). </span>
		        	</v-tooltip>
		          <v-select
		            v-model="question.answer_type"
		            :items="answerTypes"
		            item-value="id"
		            item-text="val"
			        label="Тип ответа"
		            solo
		            required
		           ></v-select>
		        </v-flex>
-->
		        <v-flex xs12>
					<add-answers 
						:currentType="question.answer_type"
						:countAnswers="countAnswers"
						:answers="answers"
						:answersQty="answersQty"
						:edit="edit"
						:modes="modes"
  						@update:countAnswers="countAnswers = $event"
  						@update:answersQty="answersQty = $event"
  						@push="pushAnswer()"
  						@update:answersAudio="getUploadedAudio($event)"
  						@update:answersImage="getUploadedImage($event)"
  						@update:changeAudio="changeAudio($event)"
  						@update:changeImage="changeImage($event)"
  						@update:clickHintTooltip="clickHintTooltip($event)"
  						@update:clickVideoTooltip="clickVideoTooltip($event)"
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
					<v-btn :loading="isSubmitting" round color="success" @click.native="onSubmit()" dark large>
						 Сохранить вопрос
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
			    showMediaTooltip: false,
			    showTitleTooltip: false,
			    showTextTooltip: false,
			    showAttemptsTooltip: false,
			    showImageTooltip: false,
			    showTypeTooltip: false,
			    edit:true,

				maxDifficulty: 100,
        		minDifficulty: 1,
        		maxAttempts: 100,
        		minAttempts: 1,
        		videoLength:11,
        		minTimer: 10,
        		maxTimer: 3600,
        		maxTitleLength: 100,
        		minTitleLength: 6,
        		maxQuestionLength: 2000,
        		minQuestionLength: 12,
        		maxVideoLength: 150,
        		audioNotLoadedText: 'Аудиозапись не загружена',
        		audioLoadedText: 'Уже имеется загруженная аудиозапись',
        		imageNotLoadedText: 'Изображение не загружено',
        		imageLoadedText: 'Уже имеется загруженное изображение',

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
                	video: str => (str.length == 0 || str.length == this.videoLength) || 'Длина идентификатора видео на Youtube составляет '+ this.videoLength + ' символов',
                },
        		
				message: '',
				alert: false,
				successSet: false,
				getQError: false,
				attempts: null,
				timer: null,
				answersQty: null,
				enabledAudio:[],
				videos:[],
				audios:[],
				old_audios:[],
				audioLoadText:[],
				qMediaData:[],
				hints:[],
				modes:[],

				isSubmitting: false,
				answers: [],
				res_answers: [],
				question: null,
				image: null,
				imageLoadText:''
		    }
		  },
		methods: {
			async getResAnswers() {
				for (let i = 0; i < this.res_answers.length; i++)
				{		
					//this.res_answers[i].showMediaTooltip = false
					console.log('!')
       				await axios.get(`${TestingSystemAPI}/api/answers_hint/`, {
			            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			            params: { 'answer' : this.res_answers[i].id }
			        }).then((response) => {
			        	if (i == this.res_answers.length - 1)
			        	{
			        		let temp_arr = []
			        		for(let j = 0; j < this.qMediaData.length; j++)
			        			for (let k = 0; k < response.data.length; k++)
			        				if (response.data[k].mode == this.qMediaData[j].mode)
			        				{
			        					temp_arr.push(response.data[k])
			        					break
			        				}
				        	this.hints.push(temp_arr)
				        	
				        	console.log('this.hints')
				        	console.log(this.hints)

							console.log('this.res_answers:')
							console.log(this.res_answers)
							for (let j = 0; j < this.res_answers.length; j++)
								this.pushAnswer(j)

			        	}
			        	else {
			        		let temp_arr = []
			        		for(let j = 0; j < this.qMediaData.length; j++)
			        			for (let k = 0; k < response.data.length; k++)
			        				if (response.data[k].mode == this.qMediaData[j].mode)
			        				{
			        					temp_arr.push(response.data[k])
			        					break
			        				}

        					this.hints.push(temp_arr)
        					console.log('this.hints')
        					console.log(this.hints)
			        	}
		        	}).catch(error => {
	                    this.alert = true
	                    this.message = 'Не удалось получить данные об ответах. Проверьте подключение к сети.'
	                })
				}
			},
			getQuestion() {
				axios.get(`${TestingSystemAPI}/api/questions/`, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: { 'id' : this.$route.params.id }
		        }).then((qdata) => {
					this.question = qdata.data[0]
					this.enabledAttempts = !!this.question.attempts_number
					this.enabledTimer = !!this.question.timer
					this.enabledImage = false
       				this.answersQty = this.question.answers_number
					if (this.question.image)
						this.imageLoadText = this.imageLoadedText
					else this.imageLoadText = this.imageNotLoadedText
					this.question.old_image = this.question.image
					this.question.image = null
					this.attempts = this.question.attempts_number
					this.timer = this.question.timer

					axios.get(`${TestingSystemAPI}/api/questions_media/`, {
			            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			            params: { 'question' : this.$route.params.id }
			        }).then((response) => {
			        	this.qMediaData = response.data
			        	console.log('this.qMediaData')
			        	console.log(this.qMediaData)
			        	for (let k = 0; k < this.qMediaData.length; k++)
			        	{
			        		this.enabledAudio[k] = false
			        		this.audios[k] = null
			        		this.videos[k] = !!this.qMediaData[k].video ? this.qMediaData[k].video : ''
			        		if (this.qMediaData[k].audio && this.qMediaData[k].audio.substring(this.qMediaData[k].audio.length - 4) == "null")
				    			this.qMediaData[k].audio = null
			        		if (this.qMediaData[k].audio)
			        			this.audioLoadText[k] = this.audioLoadedText
			        		else this.audioLoadText[k] = this.audioNotLoadedText
			        		this.old_audios[k] = this.qMediaData[k].audio
			        	}

			        	axios.get(`${TestingSystemAPI}/api/answers/`, {
				            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
				            params: { 'id' : this.$route.params.id }
				        }).then((adata) => {
							this.res_answers = adata.data
							this.getResAnswers()
							
				        }).catch(error => {
		                    this.alert = true
		                    this.message = 'Не удалось получить данные об ответах. Проверьте подключение к сети.'
		                })
		        	})
	               .catch(error => {
	               		this.successSet = false
	                    this.alert = true
	                    this.message = 'Не удалось добавить вопрос. Проверьте подключение к сети.'
	                })

					
		        }).catch(error => {
                    this.alert = true
                    this.message = 'Не удалось получить данные о вопросе. Проверьте подключение к сети.'
                })
			},
            getUploadedQImage(e) {
                this.question.image = e
            },
            getUploadedQAudio(e, mode) {
                this.audios[mode] = e
            },
            changeQAudio(mode){
            	if (!this.enabledAudio[mode])
       				this.audios[mode] = null
            },
            getUploadedAudio(obj) {
    			this.answers[obj.index].audio = obj.audio
    			this.answers.push(null)
    			this.answers.pop()
            },
            getUploadedImage(obj) {
    			this.answers[obj.index].image = obj.image
    			this.answers.push(null)
    			this.answers.pop()
            },
            changeAudio(obj){
				if (!this.answers[obj.index].enabledAudio[obj.mode]){
					this.answers[obj.index].audios[obj.mode] = null
        			if (this.answers[obj.index].old_audios[obj.mode])
						this.answers[obj.index].audioLoadText[obj.mode] = this.audioLoadedText
					else this.answers[obj.index].audioLoadText[obj.mode] = this.audioNotLoadedText
				}
				else this.answers[obj.index].audioLoadText[obj.mode] = this.audioNotLoadedText
            },
            changeImage(i){
				if (!this.answers[i].enabledImage){
					this.answers[i].image = null
        			if (this.answers[i].old_image)
						this.answers[i].imageLoadText = this.imageLoadedText
					else this.answers[i].imageLoadText = this.imageNotLoadedText
				}
				else this.answers[i].imageLoadText = this.imageNotLoadedText
            },
        	async patchAnswersHint(i){
				for (let j = 0; j < this.qMediaData.length; j++)
       			{
       				console.log('start of end'+this.qMediaData.length)
        			let AHintData = new FormData()
	                AHintData.set('answer', this.answers[i].id)
	                AHintData.set('mode', this.qMediaData[j].mode)
	                AHintData.set('video', this.answers[i].videos[j])
	                AHintData.set('text', this.answers[i].hints[j])

	                if (this.answers[i].old_audios[j] && !this.answers[i].enabledAudio[j])
	                 	AHintData.set('audio', "stay")
	                else if (this.answers[i].old_audios[j] && !this.answers[i].audios[j])
	                 	AHintData.set('audio', null)
	                else AHintData.set('audio', this.answers[i].audios[j])

	                console.log('answers_hint ' + this.answers[i].id + ' ' + this.qMediaData[j].mode)
					let object = {};
					AHintData.forEach(function(value, key){
					    object[key] = value;
					});
					let json = JSON.stringify(object);
	                console.log(json)

           			await axios.patch(TestingSystemAPI+'/api/answers_hint/'+this.hints[i][j].id+'/', AHintData, { 
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        })
			        .then((response) => {
			        	console.log(this.answers[i].id + ' ' + this.qMediaData[j].mode + ' success answers_hint')
			        	if (i == this.answers.length - 1 && j == this.qMediaData.length - 1)
			        	{
		               		this.successSet = true
		                    this.alert = true
		                    this.message = 'Вопрос успешно изменен.'
							this.isSubmitting = false
                			setTimeout(this.goBack, 1200)
			        	}
			        })
	               .catch(error => {
	               		this.successSet = false
	                    this.alert = true
	                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
						this.isSubmitting = false
	                    return
	                })
	           }
        	},
        	async patchAnswers(){
         		let answersData = new FormData()
                for (let i = 0; i < this.answers.length; i++)
                {
	                if (this.answers[i].old_image && !this.answers[i].enabledImage)
	                 	answersData.set('image', "stay")
	                else if (this.answers[i].old_image && !this.answers[i].image)
	                 	answersData.set('image', null)
	                else answersData.set('image', this.answers[i].image)

                 	if (this.currentType != 2 )
                 		answersData.append('priority', this.answers[i].priority)
                 	else 
                 	{
                 		if (this.answers[i].correct)
                 			answersData.append('priority', this.answers.length)
                 		else answersData.append('priority', i + 1)
                 	}
                 	answersData.append('text', this.answers[i].text)
                 	answersData.append('correct', this.answers[i].correct)
                 	if (this.currentType == 2 && !this.answers[i].correct)
                 		answersData.append('weight', 0)
                 	else answersData.append('weight', this.answers[i].weight)
                 	answersData.append('question', this.$route.params.id)

					console.log('answers'+(i+1)+':')
	                 let object = {};
					answersData.forEach(function(value, key){
					    object[key] = value;
					});
					let json = JSON.stringify(object);
	                console.log(json)

           			await axios.patch(TestingSystemAPI+'/api/answers/'+this.answers[i].id+'/', answersData, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        })
	               .then(response => {

	               		this.patchAnswersHint(i)
	                })
	               .catch(error => {
	               		this.successSet = false
	                    this.alert = true
	                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
    					this.isSubmitting = false
	                })
                }
        	},
        	async patchQuestionsMedia(){
				for (let i = 0; i < this.qMediaData.length; i++)
           		{
           			console.log('im here')
        			let QMediaData = new FormData()
	                QMediaData.set('question', this.qMediaData[i].question)
	                QMediaData.set('mode', this.qMediaData[i].mode)
	                QMediaData.set('video', this.videos[i])

	                 if (this.old_audios[i] && !this.enabledAudio[i])
	                 	QMediaData.set('audio', "stay")
	                 else if (this.old_audios[i] && !this.audios[i])
	                 	QMediaData.set('audio', null)
	                 else QMediaData.set('audio', this.audios[i])

		            console.log('qMediaData:')
					let object = {};
					QMediaData.forEach(function(value, key){
					    object[key] = value;
					});
					let json = JSON.stringify(object);
	                 console.log(json)

					await axios.patch(TestingSystemAPI+'/api/questions_media/'+this.qMediaData[i].id+'/', QMediaData,{
				          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
				          params: {}
				    })
			        .then((response) => {
			        	console.log(this.$route.params.id + ' ' + this.qMediaData[i].mode + ' success questions_media')
			        	if (i != this.qMediaData.length - 1)
			        		return
			        	this.patchAnswers()
			        	
			        })
	                .catch(error => {
	               		this.successSet = false
	                    this.alert = true
	                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
        				this.isSubmitting = false
	                    return
	                })
	            }
        	},
            onSubmit() {
	        	if (!this.$refs.editQform.validate())
	        	{
               		this.successSet = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successSet)
	        		return

	        	 this.isSubmitting = true
                 let questionData = new FormData()

                questionData.set('text', this.question.text)
                questionData.set('title', this.question.title)
                questionData.set('attempts_number', this.attempts)
                questionData.set('timer', this.timer)
                questionData.set('answer_type', this.question.answer_type)
                questionData.set('answers_number', this.answersQty)
                questionData.set('difficulty', this.question.difficulty)
                let comment = null
                if (this.question.answer_type == 1)
					comment = this.answers[0].comment
                questionData.set('comment', comment)

                 if (this.question.old_image && !this.enabledImage)
                 	questionData.set('image', "stay")
                 else if (this.question.old_image && !this.question.image)
                 	questionData.set('image', null)
                 else questionData.set('image', this.question.image)

				console.log('question:')
				let object = {};
				questionData.forEach(function(value, key){
				    object[key] = value;
				});
				let json = JSON.stringify(object);
                 console.log(json)



                axios.patch(TestingSystemAPI+'/api/questions/'+this.$route.params.id+'/', questionData, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        })
               .then((response) => {
               		this.patchQuestionsMedia()
                })
               .catch(error => {
	               	this.successSet = false
                    this.alert = true
                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
        			this.isSubmitting = false
                })
            },
			reloadPage() {
				window.location.reload(true)
			},
			goBack(){
            	router.push('/questions')
			},				
			deleteFile(isAudio, i){
				if (isAudio)
					this.audios[i] = null
				else this.question.image = null
			},
			pushAnswer(ind=null) {
				if (ind == null)
				{
					var isTrue = this.currentType == 1 ? true : false
					this.answers.push({
	                	image: null,
	                	old_image: null,
	                	text: null,
	                	priority: this.answers.length+1,
	                	correct: isTrue,
	                	weight: 256,
	                	comment: null,
	                	question: this.$route.params.id,
						enabledImage: false,
						imageLoadText: this.imageNotLoadedText,
						enabledAudio:[],
						audioLoadText:[],
						showHintTooltip:[],
						showVideoTooltip:[],
						audios:[],
						hints:[],
						videos:[],
						old_audios:[]
					})

					for (let i = 0; i < this.qMediaData.length; i++){
						this.answers[this.answers.length - 1].audios.push(null)
						this.answers[this.answers.length - 1].old_audios.push(null)
						this.answers[this.answers.length - 1].enabledAudio.push(false)
						this.answers[this.answers.length - 1].showHintTooltip.push(false)
						this.answers[this.answers.length - 1].showVideoTooltip.push(false)
						this.answers[this.answers.length - 1].videos.push('')
						this.answers[this.answers.length - 1].audioLoadText.push(this.audioNotLoadedText)
						this.answers[this.answers.length - 1].hints.push('')
					}
				}
				else
				{
					let imageText = !!this.res_answers[ind].image ? this.imageLoadedText : this.imageNotLoadedText
					this.answers.push({
						id: this.res_answers[ind].id,
	                	image: null,
	                	old_image: this.res_answers[ind].image,
	                	text: this.res_answers[ind].text,
	                	priority: this.res_answers[ind].priority,
	                	correct: this.res_answers[ind].correct,
	                	weight: this.res_answers[ind].weight,
	                	comment: this.res_answers[ind].comment,
	                	question: this.$route.params.id,
						imageLoadText: imageText,
						enabledImage: false,
						enabledAudio:[],
						audioLoadText:[],
						showHintTooltip:[],
						showVideoTooltip:[],
						audios:[],
						hints:[],
						videos:[],
						old_audios:[]
					})

					for (let i = 0; i < this.modes.length; i++){
						console.log('im here!')
						let old_audio = (this.hints[ind][i].audio && this.hints[ind][i].audio.substring(this.hints[ind][i].audio.length - 4) != "null") ? this.hints[ind][i].audio : null
						this.answers[this.answers.length - 1].audios.push(null)
						this.answers[this.answers.length - 1].old_audios.push(old_audio)
						this.answers[this.answers.length - 1].enabledAudio.push(false)
						this.answers[this.answers.length - 1].showHintTooltip.push(false)
						this.answers[this.answers.length - 1].showVideoTooltip.push(false)
						this.answers[this.answers.length - 1].videos.push(this.hints[ind][i].video)
						this.answers[this.answers.length - 1].audioLoadText.push(!!old_audio ? this.audioLoadedText : this.audioNotLoadedText)
						this.answers[this.answers.length - 1].hints.push(this.hints[ind][i].text)
						
					}
					console.log('answers: ')
					console.log(this.answers)
				}

			},
			getModeData(){				
				axios.get(`${TestingSystemAPI}/api/strict_modes/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.modes = data

       			  //this.pushAnswer()

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
       computed: {
       		countAnswers: function(val) {
       			return this.answers.length
       		},
       },
       mounted() {
   		this.getModeData()
   		this.getQuestion()
   		
       }
	}
</script>

<style>
</style>