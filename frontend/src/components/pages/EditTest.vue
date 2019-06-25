<template>
	<v-form ref="editTform">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
				<v-layout row wrap>
					<h4 class="display-1">Редактирование теста</h4>
					<v-tooltip bottom v-model="showTestTooltip">
				        <v-btn slot="activator" @click.native="showTestTooltip = !showTestTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Сейчас вы создаете новый тест. В него потребуется добавить из списка уже созданные вами вопросы, которые будут встречаться при прохождении в случайном порядке. </span>
					</v-tooltip>
				</v-layout>
			</v-flex>

				<v-flex xs12>
					<v-label>Название теста</v-label>
					<v-tooltip bottom v-model="showTitleTooltip">
				        <v-btn slot="activator" @click.native="showTitleTooltip = !showTitleTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Например, 'Концепции современного естествознания'</span>
		        	</v-tooltip>
		            <v-text-field
		              required
              		  :rules="[rules.required, rules.title]"
              		  v-model="test.name"
              		  solo
		            ></v-text-field>
		        </v-flex>

				<v-flex xs12>
					<v-label>Всего отмечено: {{questionsChecks.length}}</v-label>
					<div class="content-wrapper">
						<added-question
						:collection="questions"
						:withchecks="1"
						:questionsChecks="questionsChecks"
						@update:questionsChecks="questionsChecks = $event"
						@update:collection="toggleShow($event)"
						></added-question>
						<v-label v-if="error">Не удалось получить список вопросов. Проверьте подключение к сети.</v-label>
					</div>
				</v-flex>

				<v-flex xs12>
  					<v-label>Описание</v-label>
					<v-tooltip bottom v-model="showDescriptionTooltip">
				        <v-btn slot="activator" @click.native="showDescriptionTooltip = !showDescriptionTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Дайте развернутое пояснение содержимого курса. Например, какие темы отражены в вопросах, на кого он расчитан, по каким ресурсам можно подготовиться к нему и т.д.</span>
		        	</v-tooltip>
			        <v-textarea
			            v-model="test.description"
          		  		:rules="[rules.required, rules.description]"
			            required
              			solo
			          ></v-textarea>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Количество вопросов</v-label>
					<v-tooltip bottom v-model="showQNumTooltip">
				        <v-btn slot="activator" @click.native="showQNumTooltip = !showQNumTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Данное значение отражает реальное количество вопросов, которые будут включены в тест при прохождении. Если это значение ниже, чем количество вопросов, выбранных из списка выше, то в прохождение будут случайным выбором включены не все вопросы, выбранные из списка выше.</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.q_number_min, rules.q_number_max]"
		            v-model="test.questions_number"
		            required
		            solo
		          ></v-text-field>
		        </v-flex>

	     		<v-flex xs12 sm4>
  					<v-label>Автор курса</v-label>
					<v-tooltip bottom v-model="showAuthorTooltip">
				        <v-btn slot="activator" @click.native="showAuthorTooltip = !showAuthorTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Например, Иванов Иван Иванович</span>
		        	</v-tooltip>
		            <v-text-field
		              v-model="test.author"
		              required
		              :rules="[rules.required, rules.author]"
		              solo
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Количество попыток</v-label>
					<v-tooltip bottom v-model="showAttemptsTooltip">
				        <v-btn slot="activator" @click.native="showAttemptsTooltip = !showAttemptsTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Опциональное поле. Если оставить пустым - попытки неограниченны.</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.attempts]"
		            v-model="test.attempts"
		            required
		            solo
		          ></v-text-field>
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
                        @input="getUploadedImage"
                        @update:deleteFile="deleteImage()"
                        :checked="enabledImage"
			            :dis="!enabledImage"
			            :label="imageLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				  <v-flex xs12>
				      <h4 class="title" style="padding-top:15px" d-block>Оценки за курс (в процентах):</h4>
				  </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Отлично</v-label>
					<v-tooltip bottom v-model="showPerfectTooltip">
				        <v-btn slot="activator" @click.native="showPerfectTooltip = !showPerfectTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Отлично'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.percents, rules.perfect]"
		            v-model="test.perfect_mark"
		            solo
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Хорошо</v-label>
					<v-tooltip bottom v-model="showGoodTooltip">
				        <v-btn slot="activator" @click.native="showGoodTooltip = !showGoodTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Хорошо'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.percents, rules.good]"
		            v-model="test.good_mark"
		            solo
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Удовлетворительно</v-label>
					<v-tooltip bottom v-model="showSatisTooltip">
				        <v-btn slot="activator" @click.native="showSatisTooltip = !showSatisTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Удовлетворительно'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            v-model="test.satisfactory_mark"
		            :rules="[rules.percents, rules.satisfactory]"
		            solo
		            required
		          ></v-text-field>
		        </v-flex>	

				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="successSet ? 'success' : 'error'"
			      	>
			        {{message}}

				    <v-btn v-if="successSet" to="/tests" flat>Вернутьcя к тестам</v-btn>
				    <v-btn v-if="!successSet" @click.native="onSubmit()" flat>Попробовать еще раз</v-btn>
			      </v-alert>
		      </v-flex>	

				<v-flex xs12>
					<v-btn round color="success" @click.native="onSubmit()" dark large>
						 Создать тест
					</v-btn>
				</v-flex>	        		        
			    
			</v-layout>
		</v-container>
	</v-form>
</template>

<script>
    import Axios from 'axios'
    import FileInput from '@/components/other/FileLoader'
    import AddedQuestion from '@/components/boxes/AddedQuestion'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'
	import router from '@/router'

	const TestingSystemAPI = connection.server

    export default {
        components: { FileInput, AddedQuestion  },

		data () {
		    return {
                imageLoadText: 'Изображение еще не загружено',
                successSet: false,
                message: '',
                alert: false,

			    enabledImage: false,
			    questions: [],
			    questionsChecks: [],
			    questions_number: null,
			    error : false,
			    test: [],
                rules: {
                	required: value => !!value || 'Это необходимое поле',
                	percents: value => (value >= this.min_percent && value <= this.max_percent) || 'Введите значение от ' + this.min_percent + ' до ' + this.max_percent,
                	//perfect: value => (value > this.test.good_mark && value > this.test.satisfactory_mark) || 'Значение должно быть выше, чем значение оценки "Хорошо"',
                	//good: value => (value < this.test.perfect_mark && value > this.test.satisfactory_mark) || 'Значение должно быть между значениями оценок "Отлично" и "Удовлетворительно"',
                	//satisfactory: value => (value < this.test.good_mark && value < this.test.perfect_mark) || 'Значение должно быть ниже, чем значение оценки "Хорошо"',
                	attempts: value => (value >= this.minAttempts && value <= this.maxAttempts) || 'Введите значение в диапазоне от '+this.minAttempts+' до '+this.maxAttempts,
                	author: value => (value.length >= this.minAuthorLen && value.length <= this.maxAuthorLen) || 'Длина поля должна быть в диапазоне от '+this.minAuthorLen +' до '+this.maxAuthorLen + ' символов',
                	q_number_min: val => val > 0 || 'Значение должно быть больше 0',
                	q_number_max: val => val <= this.questionsChecks.length || 'Должно быть не более, чем число вопросов, выбранных выше',
                	description: val => (val.length >= this.minDescrLen && val.length <= this.maxDescrLen) || 'Длина текста должна быть в диапазоне от '+this.minDescrLen+' до '+this.maxDescrLen + ' символов',
                	title: val => (val.length >= this.minTitleLen && val.length <= this.maxTitleLen) || 'Длина названия должна быть в диапазоне от '+this.minTitleLen+' до '+this.maxTitleLen + ' символов',
                	video: str => (str.length == 0 || str.length == this.videoLength) || 'Длина идентификатора видео на Youtube составляет '+ this.videoLength + ' символов',
                },

			    showTestTooltip: false,
			    showTitleTooltip: false,
			    showSatisTooltip: false,
			    showGoodTooltip: false,
			    showPerfectTooltip: false,
			    showAttemptsTooltip: false,
			    showAuthorTooltip: false,
			    showQNumTooltip: false,
			    showLinkTooltip: false,
			    showDescriptionTooltip: false,
			    showMediaTooltip: false,

			    max_percent: 100,
			    min_percent: 0,
        		maxAttempts: 100,
        		minAttempts: 0,
        		maxAuthorLen: 70,
        		minAuthorLen: 10,
        		minDescrLen: 50,
        		maxDescrLen: 2000,
        		minTitleLen: 8,
        		maxTitleLen: 100,
        		videoLength: 11
		    }
		},
		methods: {
			getQuestionsList() {
				Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = data
		          this.questions.reverse()

		          //for (var i = 0; i < this.questions.length; ++i)
		          	//	this.questions[i].show = false
		        }).catch(error => {
		          this.error = true
		          this.message = 'Не удалось получить список вопросов'

		          console.log(error)
		        })
			},
			getTestData(){
				Axios.get(`${TestingSystemAPI}/api/courses/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {'token' : this.$route.params.token}
		        }).then(({data}) => {
		          this.test = data[0]
		          this.questionsChecks = this.test.questions

				  if (this.test.image)
					this.imageLoadText = 'Уже имеется загруженное изображение'
				  this.test.old_image = this.test.image
				  this.test.image = null
				  this.getQuestionsList()

		        }).catch(error => {
		          this.error = true
		          this.message = 'Не удалось получить данные о тесте'

		          console.log(error)
		        })
			},
            onSubmit() {
	        	if (!this.$refs.editTform.validate())
	        	{
               		this.successSet = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successSet)
	        		return
                 let formData = new FormData()

                 formData.set('name', this.test.name)
                 formData.set('attempts', this.test.attempts)
                 formData.set('questions_number', this.test.questions_number)
                 formData.set('author', this.test.author)
                 formData.set('description', this.test.description)

                 if (this.test.old_image && !this.enabledImage)
                 	formData.set('image', "stay")
                 else if (this.test.old_image && !this.test.image)
                 	formData.set('image', null)
                 else formData.set('image', this.test.image)

                 formData.set('perfect_mark', this.test.perfect_mark)
                 formData.set('good_mark', this.test.good_mark)
                 formData.set('satisfactory_mark', this.test.satisfactory_mark)
                 for (var i = 0; i < this.questionsChecks.length; i++)
                 {
                 	formData.append('questions', this.questionsChecks[i])
                 	/*
                 	var object = {};
					formData.forEach(function(value, key){
					    object[key] = value;
					});
					var json = JSON.stringify(object);
	                 console.log(json)
	                 */
                 }

				

                 Axios.patch(`${TestingSystemAPI}/api/courses/`+this.$route.params.token, formData, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			        })
	               .then((response) => {
	               		this.successSet = true
	                    this.alert = true
	                    this.message = 'Тест успешно добавлен.'
	                    setTimeout(this.goBack, 1200)
	                })
	               .catch((error) => {
	               		this.successSet = false
	                    this.alert = true
	                    this.message = 'Не удалось добавить тест. Проверьте подключение к сети.'
	                })
            },
            getUploadedImage(e) {
                this.test.image = e
            },
			toggleShow(id) {
				for (var i = 0; i < this.questions.length; ++i)
					if (this.questions[i].id == id)
					{
						this.questions[i].show = !this.questions[i].show
						this.questions.push(null)
						this.questions.pop()
						return
					}
			},
			goBack(){
            	router.push('/tests')
			},				
			deleteImage(){
				this.test.image = null
			}		
		},
		watch: {
			satisfactory_mark: function(val) {
				console.log('s: '+val + ' g: ' + this.test.good_mark + ' p: ' + this.test.perfect_mark)
			},
			good_mark: function(val) {
				console.log('s: '+this.test.satisfactory_mark + ' g: ' + val + ' p: ' + this.test.perfect_mark)
			},
			perfect_mark: function(val) {
				console.log('s: '+ this.test.satisfactory_mark + ' g: ' + this.test.good_mark + ' p: ' + val)
			},
			questionsChecks: function(val) {
				this.questions_number = val.length
			},
			enabledImage: function(val){
       			if (!val)
       			{
       				this.test.image = null
       				if (this.test.old_image)
       					this.imageLoadText = 'Уже имеется загруженное изображение'
       				else this.imageLoadText = 'Изображение еще не загружено' 
       			}
       			else 
       				this.imageLoadText = 'Изображение еще не загружено' 
			}
		},
		mounted(){
			this.getTestData()
		}
	}
	
</script>

<style>
	.content-wrapper{
		overflow-y: auto;
		border-radius: 4px;
		border: 1px solid #919191;
		height: 400px;
		margin-bottom: 10px;
		background: #EBEBEB;
		padding: 15px;
	}
</style>