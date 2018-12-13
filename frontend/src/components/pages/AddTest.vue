<template>
	<v-form ref="addTform">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
					<p class="display-1">Создание нового теста</p>
				</v-flex>

				<v-flex xs12 sm6>
		            <v-text-field
		              label="Название"
		              required
              		  :rules="[rules.required, rules.title]"
              		  v-model="title"
		            ></v-text-field>
		        </v-flex>

  				<v-flex xs12 sm6>
		            <v-text-field
		              label="Ссылка на курс"
		              placeholder="your-test"
		              required
            		  prefix="/"
              		  v-model="token"
              		  :rules="[rules.required, rules.token]"
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
			        <v-textarea
			            label="Описание теста"
			            v-model="description"
          		  		:rules="[rules.required, rules.description]"
			            required
              			box
			          ></v-textarea>
		        </v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество вопросов"
		            :rules="[rules.q_number_min, rules.q_number_max]"
		            v-model="questions_number"
		            required
		          ></v-text-field>
		        </v-flex>

	     		<v-flex xs12 sm6>
		            <v-text-field
		              label="Автор курса"
		              v-model="author"
		              required
		              :rules="[rules.required, rules.author]"
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество попыток"
		            :rules="[rules.attempts]"
		            v-model="attempts"
		            required
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
				      <h4 class="title" d-block>Оценки за курс:</h4>
				  </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Отлично'"
		            :rules="[rules.percents, rules.perfect]"
		            hint="В процентах (%)"
		            v-model="perfect_mark"
		            box
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Хорошо'"
		            :rules="[rules.percents, rules.good]"
		            v-model="good_mark"
		            hint="В процентах (%)"
		            box
		            required
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Удовлетворительно'"
		            v-model="satisfactory_mark"
		            :rules="[rules.percents, rules.satisfactory]"
		            hint="В процентах (%)"
		            box
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

	const TestingSystemAPI = connection.server

    export default {
        components: { FileInput, AddedQuestion },

		data () {
		    return {
        		rules: [ (value) => !!value || 'Это обязательное поле' ],
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
			    checkTokenDelay: 1000,

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
        		maxAuthorLen: 50,
        		minAuthorLen: 10,
        		minDescrLen: 50,
        		maxDescrLen: 2000,
        		minTitleLen: 8,
        		maxTitleLen: 100,
        		minTokenLen: 8,
        		maxTokenLen: 50,


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
                	token: val => (val.length >= this.minTokenLen && val.length <= this.maxTokenLen) || 'Длина токена должна быть в диапазоне от '+this.minTokenLen+' до '+this.maxTokenLen + ' символов',
                },

		    }
		},
		methods: {
			getAddedQuestions() {
				Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
					//Axios.get('https://jsonplaceholder.typicode.com/posts', {
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
            onSubmit() {
	        	if (!this.$refs.addTform.validate())
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
            goBack() {
            	router.push('/tests')
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
			checkToken(token) {
				const data = { 'token' : token}
				Axios.post(`${TestingSystemAPI}/api/token-check/`, data, {
			          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
			          params: {}
			    })
                .then((response) => {
                	console.log(response)
                })
                .catch((error) => {
               		
                })
				this.checkTokenObserver = true;

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
			},
			token: function(val) {
				if (!this.checkTokenObserver)
				{
					setTimeout(this.checkToken(val), this.checkTokenDelay)
					this.checkTokenObserver = true;
				}
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