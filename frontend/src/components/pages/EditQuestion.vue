<template>
	<v-form ref="editQform">
		<v-container>
			<v-layout row wrap>
				<h4 class="display-1">Редактирование вопроса</h4>
				<v-flex xs12>
		            <v-text-field
		              label="Краткое название (будет видно только вам)"
		              v-model="question.title"
		              required
              		  clearable
              		  :rules="rulesTitleLength"
              		  box
		            ></v-text-field>
		        </v-flex>
		        <v-flex xs12>
			        <v-textarea
			            label="Формулировка вопроса"
			            v-model="question.text"
          		  		:rules="rulesQuestionLength"
			            required
              			clearable
              			box
			          ></v-textarea>
		        </v-flex>

		          <v-flex xs12 sm6 xl3>
	        		<v-layout align-center>
			          	<v-checkbox v-model="enabledAttempts" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type="number"
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

			      <v-flex xs12>
				      <v-label>Замена изображения и аудио:</v-label>
				      <v-tooltip bottom v-model="showMediaTooltip">
					    <v-btn slot="activator" @click="showMediaTooltip = !showMediaTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
					    <span>Если вы хотите оставить изображение или аудио без изменений, убедитесь, что галочки ниже не отмечены. Если же хотите удалить их, отметьте галочку, но не загружайте новый файл. Для изменения изображения или аудио загрузите новый файл.</span>
			          </v-tooltip>
			      </v-flex>

		          <v-flex xs12 sm6 xl3>
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

				  <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledAudio" hide-details class="shrink mr-2"></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="audio/*"
	                    ref="fileInput"
                        @input="getUploadedQAudio($event)"
                        @update:deleteFile="deleteFile(1)"
			            :dis="!enabledAudio"
			            :checked="enabledAudio"
			            :label="audioLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

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
	                :rules="rulesDifficulty"
	                box
	              ></v-text-field>
	            </v-flex>

				<v-flex xs12>
		          <v-select
		            v-model="question.answer_type"
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
						:currentType="question.answer_type"
						:countAnswers="countAnswers"
						:answers="answers"
						:answersQty="answersQty"
						:edit="edit"
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
			      	>
			        {{message}}

				    <v-btn v-if="successSet" to="/questions" flat>Вернутьcя к вопросам</v-btn>
				    <v-btn v-if="!successSet" @click.native="onSubmit()" flat>Попробовать еще раз</v-btn>
			      </v-alert>
		      </v-flex>	

		      <v-flex xs12>
					<v-btn round color="success" @click.native="onSubmit()" dark large>
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
			    enabledAudio: false,
			    showMediaTooltip: false,
			    edit:true,

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
				getQError: false,
				attempts: null,
				timer: null,
				answersQty: null,

				questionId: '',
				answers: [],
				question: null,

                imageLoadText: 'Изображение еще не загружено',
                audioLoadText: 'Аудиозапись еще не загружена',
		    }
		  },
		methods: {
			getQuestion() {
				axios.get(`${TestingSystemAPI}/api/questions/`, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: { 'id' : this.$route.params.id }
		        }).then((qdata) => {
					this.question = qdata.data[0]
					this.enabledAttempts = !!this.question.attempts_number
					this.enabledTimer = !!this.question.timer
					this.enabledAudio = false
					this.enabledImage = false
       				this.answersQty = this.question.answers_number
					if (this.question.audio)
						this.audioLoadText = 'Уже имеется загруженная аудиозапись'
					if (this.question.image)
						this.imageLoadText = 'Уже имеется загруженное изображение'
					this.question.old_image = this.question.image
					this.question.old_audio = this.question.audio
					this.question.image = null
					this.question.audio = null
					this.attempts = this.question.attempts_number
					this.timer = this.question.timer

					axios.get(`${TestingSystemAPI}/api/answers/`, {
			            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			            params: { 'id' : this.$route.params.id }
			        }).then((adata) => {
						this.answers = adata.data
						for (var i = 0; i < this.answers.length; i++)
						{
							this.answers[i].enabledAudio = false
							if (this.answers[i].audio)
								this.answers[i].audioLoadText = 'Уже имеется загруженная аудиозапись'
							else this.answers[i].audioLoadText = 'Аудиозапись еще не загружена'

							this.answers[i].enabledImage = false
							if (this.answers[i].image)
								this.answers[i].imageLoadText = 'Уже имеется загруженное изображение'
							else this.answers[i].imageLoadText = 'Изображение еще не загружено'
							this.answers[i].showMediaTooltip = false
							this.answers[i].old_image = this.answers[i].image
							this.answers[i].old_audio = this.answers[i].audio
							this.answers[i].image = null
							this.answers[i].audio = null
						}

			        }).catch(error => {
	                    this.alert = true
	                    this.message = 'Не удалось получить данные об ответах. Проверьте подключение к сети.'
	                })
		        }).catch(error => {
                    this.alert = true
                    this.message = 'Не удалось получить данные о вопросе. Проверьте подключение к сети.'
                })
			},
            getUploadedQImage(e) {
                this.question.image = e
            },
            getUploadedQAudio(e) {
                this.question.audio = e
            },
            getUploadedAudio(obj) {
            	for (var i = 0; i < this.answers.length; ++i)
            		if (i == obj.index)
            		{
            			this.answers[i].audio = obj.audio
            			this.answers.push(null)
            			this.answers.pop()
            			return
            		}
            },
            getUploadedImage(obj) {
            	for (var i = 0; i < this.answers.length; ++i)
            		if (i == obj.index)
            		{
            			this.answers[i].image = obj.image
            			this.answers.push(null)
            			this.answers.pop()
            			return
            		}
            },
            changeAudio(ind){
				for (var i = 0; i < this.answers.length; ++i)
					if (i == ind)
					{
						if (!this.answers[i].enabledAudio){
	            			if (this.answers[i].audio)
								this.answers[i].audioLoadText = "Уже имеется загруженная аудиозапись"
							else 
							{
								this.audio = null
								this.answers[i].audioLoadText = "Аудиозапись еще не загружена"
							}
						}
						else this.answers[i].audioLoadText = "Аудиозапись еще не загружена"
					}

				this.answers.push(null)
				this.answers.pop()
            },
            changeImage(ind){
				for (var i = 0; i < this.answers.length; ++i)
					if (i == ind)
					{
						if (!this.answers[i].enabledImage){
	            			if (this.answers[i].image)
								this.answers[i].imageLoadText = "Уже имеется загруженное изображение"
							else 
							{
								this.image = null
								this.answers[i].imageLoadText = "Изображение еще не загружено"
							}
						}
						else this.answers[i].imageLoadText = "Изображение еще не загружено"
					}
				this.answers.push(null)
				this.answers.pop()
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

                 let formData = new FormData()

                 formData.set('text', this.question.text)
                 formData.set('title', this.question.title)
                 formData.set('attempts_number', this.attempts)
                 formData.set('timer', this.timer)
                 formData.set('answer_type', this.question.answer_type)
                 formData.set('answers_number', this.answersQty)
                 formData.set('difficulty', this.question.difficulty)

                 if (this.question.old_image && !this.enabledImage)
                 	formData.set('image', "stay")
                 else if (this.question.old_image && !this.question.image)
                 	formData.set('image', null)
                 else formData.set('image', this.question.image)

                 if (this.question.old_audio && !this.enabledAudio)
                 	formData.set('audio', "stay")
                 else if (this.question.old_audio && !this.question.audio)
                 	formData.set('audio', null)
                 else formData.set('audio', this.question.audio)

                 var comment = null
                 if (this.currentType == 1)
					comment = this.answers[0].comment
                 formData.set('comment', comment)
				/*
				var object = {};
				formData.forEach(function(value, key){
				    object[key] = value;
				});
				var json = JSON.stringify(object);
                 console.log(json)
				*/			

                 axios.patch(`${TestingSystemAPI}/api/questions/`, formData, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: { 'id' : this.$route.params.id }
			        })
	               .then((response) => {
	               		this.questionId = response.data.id
	               		for (var i = 0; i < this.answers.length; ++i)
	               			this.answers[i].question = this.questionId

                 		let answersData = new FormData()

		                for (var i = 0; i < this.answers.length; i++)
		                {

			                if (this.answers[i].old_image && !this.answers[i].enabledImage)
			                 	answersData.set('image', "stay")
			                else if (this.answers[i].old_image && !this.answers[i].image)
			                 	answersData.set('image', null)
			                else answersData.set('image', this.answers[i].image)

			                if (this.answers[i].old_audio && !this.answers[i].enabledAudio)
			                 	answersData.set('audio', "stay")
			                else if (this.answers[i].audio && !this.answers[i].audio)
			                 	answersData.set('audio', null)
			                else answersData.set('audio', this.answers[i].audio)

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
		                 	answersData.append('hint', this.answers[i].hint)
		                 	answersData.append('question', this.questionId)
		                 	/*
		                 	var object = {};
							answersData.forEach(function(value, key){
							    object[key] = value;
							});
							var json = JSON.stringify(object);
			                 console.log(json)
			                 */
		                 }

               			axios.patch(`${TestingSystemAPI}/api/answers/`, answersData, {
				          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
				          params: { 'id' : this.$route.params.id }
				        })
		               .then(response => {
		               		this.successSet = true
		                    this.alert = true
		                    this.message = 'Вопрос успешно изменен.'
	                    	setTimeout(this.goBack, 1200)
		                })
		               .catch(error => {
		                    this.alert = true
		                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
		                })
	                })
	               .catch(error => {
	                    this.alert = true
	                    this.message = 'Не удалось изменить вопрос. Проверьте подключение к сети.'
	                })
            },
			reloadPage() {
				window.location.reload(true)
			},
			goBack(){
            	router.push('/tests')
			},				
			deleteFile(isAudio){
				if (isAudio)
					this.question.audio = null
				else this.question.image = null
			},
			pushAnswer(ind=null) {
				if (!ind)
				{
					var isTrue = this.currentType == 1 ? true : false
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
				}
				else
				{
					var enAudio = true
					var enImage = true
					this.answers.push({
	                	image: this.answers[ind].image,
	                	audio: this.answers[ind].audio,
	                	text: this.answers[ind].text,
	                	priority: this.answers[ind].priority,
	                	correct: this.answers[ind].correct,
	                	weight: this.answers[ind].weight,
	                	hint: this.answers[ind].hint,
	                	comment: this.answers[ind].comment,
	                	question: this.$route.params.id,
						enabledAudio: true,
						enabledImage: true
					})
				}
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
       		enabledImage: function(val) {
       			if (!val)
       			{
       				this.question.image = null
       				if (this.question.old_image)
       					this.imageLoadText = 'Уже имеется загруженное изображение'
       				else this.imageLoadText = 'Изображение еще не загружено' 
       			}
       			else 
       				this.imageLoadText = 'Изображение еще не загружено' 

       		},
       		enabledAudio: function(val) {
       			if (!val)
       			{
       				this.question.audio = null
       				if (this.question.old_audio)
       					this.audioLoadText = 'Уже имеется загруженная аудиозапись'
       				else this.audioLoadText = 'Аудиозапись еще не загружена'
       			}
       			else 
       				this.audioLoadText = 'Аудиозапись еще не загружена'
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
       		this.getQuestion()
       		for (var i = 0; i < this.answers.length; i++)
       			this.pushAnswer(i)
       }
	}
</script>

<style>
</style>