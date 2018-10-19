<template>
	<v-form @submit.prevent="onSubmit">
		<v-container>
			<v-layout row wrap>
				<v-flex xs12>
					<p class="display-1">Создание нового теста</p>
				</v-flex>

				<v-flex xs12 sm6>
		            <v-text-field
		              label="Название"
		              required
              		  clearable
              		  :rules="rules"
              		  v-model="title"
		            ></v-text-field>
		        </v-flex>

  				<v-flex xs12 sm6>
		            <v-text-field
		              label="Ссылка на курс"
		              placeholder="your-test"
		              required
              		  clearable
            		  prefix="/"
              		  v-model="token"
              		  :rules="rules"
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
          		  		:rules="rules"
			            required
              			clearable
              			box
			          ></v-textarea>
		        </v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество вопросов"
		            :rules="rules"
		            v-model="questions_number"
		            hint="Не более, чем число вопросов, выбранных выше"
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

	     		<v-flex xs12 sm6>
		            <v-text-field
		              label="Автор курса"
		              v-model="author"
		              required
		              :rules="rules"
              		  clearable
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество попыток"
		            :rules="rulesAttempts"
		            v-model="attempts"
		            required
              		clearable
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
		            :rules="rulesPercents"
		            hint="В процентах (%)"
		            v-model="perfect_mark"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Хорошо'"
		            :rules="rulesPercents"
		            v-model="good_mark"
		            hint="В процентах (%)"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Удовлетворительно'"
		            v-model="satisfactory_mark"
		            :rules="rulesPercents"
		            hint="В процентах (%)"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>	

				<v-flex xs12>
					<v-btn round color="success" @click.native="onSubmit()" dark large>
						 Создать тест
					</v-btn>
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

                image: '',
                imageLoadText: 'Изображение к тесту',

                rulesPercents: [(value)=> (value >= this.min_percent && value <= this.max_percent) || 'Введите значение от ' + this.min_percent + ' до ' + this.max_percent],
        		rulesAttempts: [ (value) => (value >= this.minAttempts && value <= this.maxAttempts) || 'Введите значение в диапазоне от '+this.minAttempts+' до '+this.maxAttempts ],

			    enabledImage: false,
			    questions: [],
			    questionsChecks: [],
			    error : false,
			    successSet: false,
			    alert: false,
			    message: '',

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
        		minAttempts: 1,
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
	               		console.log(response)
	               		this.questionId = response.data.id
	               		console.log(this.questionId)
	               		console.log(this.answers.length)
	               		console.log(this.answers)
	               		for (var i = 0; i < this.answers.length; ++i)
	               			this.answers[i].question = this.questionId
	               			axios.post(`${TestingSystemAPI}/api/answers/`, this.answers, {
					          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
					          params: {}
					        })
			               .then(response => {
			               		this.successSet = true
			                    this.alert = true
			                    this.message = 'Тест успешно добавлен.'
			                })
			               .catch(error => {
			               		this.successSet = false
			                    this.alert = true
			                    this.message = 'Не удалось добавить тест. Проверьте подключение к сети.'
			                })
						
	                })
	               .catch(error => {
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
			}
		},
		mounted(){
			this.getAddedQuestions()
		},
		watch: {
			title: function(val) {
				this.token = this.textToTranslit(val)
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