<template>
	<v-form ref="addTform">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
				<v-layout row wrap>
					<h4 class="display-1">Создание нового теста</h4>
					<v-tooltip bottom v-model="showTestTooltip">
				        <v-btn slot="activator" @click="showTestTooltip = !showTestTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Сейчас вы создаете новый тест. В него потребуется добавить из списка уже созданные вами вопросы, которые будут встречаться при прохождении в случайном порядке. </span>
					</v-tooltip>
				</v-layout>
			</v-flex>

				<v-flex xs12 sm6>
					<v-label>Название теста</v-label>
					<v-tooltip bottom v-model="showTitleTooltip">
				        <v-btn slot="activator" @click="showTitleTooltip = !showTitleTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Например, 'Концепции современного естествознания'</span>
		        	</v-tooltip>
		            <v-text-field
		              required
              		  :rules="[rules.required, rules.title]"
              		  v-model="title"
              		  solo
		            ></v-text-field>
		        </v-flex>

  				<v-flex xs12 sm6>
  					<v-label>Ссылка на курс</v-label>
					<v-tooltip bottom v-model="showLinkTooltip">
				        <v-btn slot="activator" @click="showLinkTooltip = !showLinkTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>По введенной ссылке любой желающий сможет подписаться на тест и начать проходить его. Если вам не нравится автоматически сгенерированный вариант на основе названия курса, вы можете изменить его.</span>
		        	</v-tooltip>
		            <v-text-field
		              placeholder="your-test"
		              required
            		  prefix="/"
            		  solo
              		  v-model="token"
              		  :hint="validToken ? '' : 'Такая ссылка уже существует! Выберите другой вариант.'"
              		  :rules="[rules.tokenValid, rules.token]"
              		  :append-icon="validToken ? 'done' : 'block'"
              		  :error="!validToken"
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
				        <v-btn slot="activator" @click="showDescriptionTooltip = !showDescriptionTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Дайте развернутое пояснение содержимого курса. Например, какие темы отражены в вопросах, на кого он расчитан, по каким ресурсам можно подготовиться к нему и т.д.</span>
		        	</v-tooltip>
			        <v-textarea
			            v-model="description"
          		  		:rules="[rules.required, rules.description]"
			            required
              			solo
			          ></v-textarea>
		        </v-flex>

		        <v-flex xs12 sm6>
  					<v-label>Количество вопросов</v-label>
					<v-tooltip bottom v-model="showQNumTooltip">
				        <v-btn slot="activator" @click="showQNumTooltip = !showQNumTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Данное значение отражает реальное количество вопросов, которые будут включены в тест при прохождении. Если это значение ниже, чем количество вопросов, выбранных из списка выше, то в прохождение будут случайным выбором включены не все вопросы, выбранные из списка выше.</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.q_number_min, rules.q_number_max]"
		            v-model="questions_number"
		            required
		            solo
		          ></v-text-field>
		        </v-flex>

	     		<v-flex xs12 sm6>
  					<v-label>Автор курса</v-label>
					<v-tooltip bottom v-model="showAuthorTooltip">
				        <v-btn slot="activator" @click="showAuthorTooltip = !showAuthorTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Например, Иванов Иван Иванович</span>
		        	</v-tooltip>
		            <v-text-field
		              v-model="author"
		              required
		              :rules="[rules.required, rules.author]"
		              solo
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6>
  					<v-label>Количество попыток</v-label>
					<v-tooltip bottom v-model="showAttemptsTooltip">
				        <v-btn slot="activator" @click="showAttemptsTooltip = !showAttemptsTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Опциональное поле. Если оставить пустым - попытки неограниченны.</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.attempts]"
		            v-model="attempts"
		            required
		            solo
		          ></v-text-field>
		        </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledImage" hide-details class="shrink mr-2" ></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="image/*"
	                    ref="fileInput"
                        @input="getUploadedImage"
                        :checked="enabledImage"
			            :dis="!enabledImage"
			            :label="imageLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				  <v-flex xs12>
				      <h4 class="title" d-block>Оценки за курс (в процентах):</h4>
				  </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Отлично</v-label>
					<v-tooltip bottom v-model="showPerfectTooltip">
				        <v-btn slot="activator" @click="showPerfectTooltip = !showPerfectTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Отлично'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.percents, rules.perfect]"
		            v-model="perfect_mark"
		            solo
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Хорошо</v-label>
					<v-tooltip bottom v-model="showGoodTooltip">
				        <v-btn slot="activator" @click="showGoodTooltip = !showGoodTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Хорошо'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            :rules="[rules.percents, rules.good]"
		            v-model="good_mark"
		            solo
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
  					<v-label>Удовлетворительно</v-label>
					<v-tooltip bottom v-model="showSatisTooltip">
				        <v-btn slot="activator" @click="showSatisTooltip = !showSatisTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Нижний порог, с которого начинается 'Удовлетворительно'</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            v-model="satisfactory_mark"
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
	import router from '@/router'
    import FileInput from '@/components/other/FileLoader'
    import AddedQuestion from '@/components/boxes/AddedQuestion'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

    export default {
        components: { FileInput, AddedQuestion },

		data () {
		    return {
        		valid: false,
                image: '',
                imageLoadText: 'Изображение к тесту',

			    enabledImage: false,
			    questions: [],
			    questionsChecks: [],
			    error : false,
			    successSet: false,
			    alert: false,
			    message: '',
			    checkTokenObserver: false,

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

			    title: '',
			    token: '',
			    attempts: '',
			    questions_number: '',
			    author: '',
			    description: '',
			    perfect_mark: 75,
			    good_mark: 50,
			    satisfactory_mark: 25,
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
        		minTokenLen: 8,
        		maxTokenLen: 50,
        		validToken: true,

                rules: {
                	required: value => !!value || 'Это необходимое поле',
                	percents: value => (value >= this.min_percent && value <= this.max_percent) || 'Введите значение от ' + this.min_percent + ' до ' + this.max_percent,
                	perfect: value => (value > this.good_mark && value > this.satisfactory_mark) || 'Значение должно быть выше, чем значение оценки "Хорошо"',
                	good: value => (value < this.perfect_mark && value > this.satisfactory_mark) || 'Значение должно быть между значениями оценок "Отлично" и "Удовлетворительно"',
                	satisfactory: value => (value < this.good_mark && value < this.perfect_mark) || 'Значение должно быть ниже, чем значение оценки "Хорошо"',
                	attempts: value => (value >= this.minAttempts && value <= this.maxAttempts) || 'Введите значение в диапазоне от '+this.minAttempts+' до '+this.maxAttempts,
                	author: value => (value.length >= this.minAuthorLen && value.length <= this.maxAuthorLen) || 'Длина поля должна быть в диапазоне от '+this.minAuthorLen +' до '+this.maxAuthorLen + ' символов',
                	q_number_min: val => val > 0 || 'Значение должно быть больше 0',
                	q_number_max: val => val <= this.questionsChecks.length || 'Должно быть не более, чем число вопросов, выбранных выше',
                	description: val => (val.length >= this.minDescrLen && val.length <= this.maxDescrLen) || 'Длина текста должна быть в диапазоне от '+this.minDescrLen+' до '+this.maxDescrLen + ' символов',
                	title: val => (val.length >= this.minTitleLen && val.length <= this.maxTitleLen) || 'Длина названия должна быть в диапазоне от '+this.minTitleLen+' до '+this.maxTitleLen + ' символов',
                	tokenValid: async (val) => await this.getTokenAnswer() || '',
                	token: val => (val.length >= this.minTokenLen && val.length <= this.maxTokenLen) || 'Длина ссылки должна быть в диапазоне от '+this.minTokenLen+' до '+this.maxTokenLen + ' символов'
                },

		    }
		},
		methods: {
			async getTokenAnswer(){
				var ans = false
				await this.checkToken()
				.then(
					res=>{
						ans = res
						if (ans == 'true')
							this.validToken = true
						else this.validToken = false
					}, 
					err => {
						console.log(err)
					}
				)
				return this.validToken
			},
			getAddedQuestions() {
				Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = data
		          this.questions.reverse()
		          for (var i = 0; i < this.questions.length; ++i)
		          	this.questions[i].show = false
		        }).catch(error => {
		          this.error = true

		          console.log(error)
		        })
			},
            getUploadedImage(e) {
                this.image = e
            },
            goBack() {
            	router.push('/tests')
            },
            onSubmit() {
	        	if (!this.$refs.addTform.validate() || !this.validToken)
	        	{
               		this.successSet = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successSet)
	        		return
                 let formData = new FormData()

                 formData.set('name', this.title)
                 formData.set('token', this.token)
                 formData.set('attempts', this.attempts)
                 formData.set('questions_number', this.questions_number)
                 formData.set('author', this.author)
                 formData.set('description', this.description)
                 formData.set('image', this.image)
                 formData.set('perfect_mark', this.perfect_mark)
                 formData.set('good_mark', this.good_mark)
                 formData.set('satisfactory_mark', this.satisfactory_mark)
                 for (var i = 0; i < this.questionsChecks.length; i++)
                 	formData.append('questions', this.questionsChecks[i])

                 console.log(formData)

                 Axios.post(`${TestingSystemAPI}/api/courses/`, formData, {
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
            textToTranslit(text) {
            	var transl = []
				transl['а']='a'
				transl['б']='b'
				transl['в']='v'
				transl['г']='g'
				transl['д']='d'
				transl['е']='e'
				transl['ё']='yo'
				transl['ж']='zh'
				transl['з']='z'
				transl['и']='i'
				transl['й']='j'
				transl['к']='k'
				transl['л']='l'
				transl['м']='m'
				transl['н']='n'
				transl['о']='o'
				transl['п']='p'
				transl['р']='r'
				transl['с']='s'
				transl['т']='t'
				transl['у']='u'
				transl['ф']='f'
				transl['х']='kh'
				transl['ц']='c'
				transl['ч']='ch'
				transl['ш']='sh'
				transl['щ']='shch'
				transl['ъ']=''
				transl['ы']='i'
				transl['ь']=''
				transl['э']='e'
				transl['ю']='yu'
				transl['я']='ya'
				transl[' ']='_'
				transl['А']='a'
				transl['Б']='b'
				transl['В']='v'
				transl['Г']='g'
				transl['Д']='d'
				transl['Е']='e'
				transl['Ё']='yo'
				transl['Ж']='zh'
				transl['З']='z'
				transl['И']='i'
				transl['Й']='j'
				transl['К']='k'
				transl['Л']='l'
				transl['М']='m'
				transl['Н']='n'
				transl['О']='o'
				transl['П']='p'
				transl['Р']='r'
				transl['С']='s'
				transl['Т']='t'
				transl['У']='u'
				transl['Ф']='f'
				transl['Х']='kh'
				transl['Ц']='c'
				transl['Ч']='ch'
				transl['Ш']='sh'
				transl['Щ']='shch'
				transl['Ъ']=''
				transl['Ы']='i'
				transl['Ь']=''
				transl['Э']='e'
				transl['Ю']='yu'
				transl['Я']='ya'
				transl['/']=''
				transl['\\']=''


				var result=''
			    for (var i=0; i < text.length; i++) {
			        if(transl[text[i]]!=undefined)  
			        	result += transl[text[i]]
			        else 
			        	result += text[i]
    			}
			    return result
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
			async checkToken() {
				const data = { 'token' : this.token}
				const req = await Axios.post(`${TestingSystemAPI}/api/token-check/`, data, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			    })
                .then((response) => {
					this.checkTokenObserver = false;
                	return response.data.avaliable
                })
                .catch((error) => {
					this.checkTokenObserver = false;
					return false
                })
                return req
			}
		},
		mounted(){
			this.getAddedQuestions()
		},
		watch: {
			title: function(val) {
				this.token = this.textToTranslit(val)
			},
			satisfactory_mark: function(val) {
				console.log('s: '+val + ' g: ' + this.good_mark + ' p: ' + this.perfect_mark)
			},
			good_mark: function(val) {
				console.log('s: '+this.satisfactory_mark + ' g: ' + val + ' p: ' + this.perfect_mark)
			},
			perfect_mark: function(val) {
				console.log('s: '+ this.satisfactory_mark + ' g: ' + this.good_mark + ' p: ' + val)
			},
			questionsChecks: function(val) {
				this.questions_number = val.length
			}
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