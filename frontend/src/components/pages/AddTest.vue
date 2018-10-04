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
              		  box
		            ></v-text-field>
		        </v-flex>

  				<v-flex xs12 sm6>
		            <v-text-field
		              label="Ссылка на курс"
		              required
              		  clearable
              		  :rules="rules"
              		  box
		            ></v-text-field>
		        </v-flex>

				<v-flex xs12>
					<p>Всего отмечено: {{questionsChecks.length}}</p>
					<div class="content-wrapper">
						<added-question
						v-for="question in questions"
						:title="question.title"
						:text="question.body"
						:type="2"
						:withchecks="1"
						:questionsChecks="questionsChecks"
						></added-question>
						<p v-if="error">Не удалось загрузить список вопросов</p>
					</div>
				</v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество вопросов"
		            :rules="rules"
		            hint="Не более, чем число вопросов, выбранных выше"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

	     		<v-flex xs12 sm6>
		            <v-text-field
		              label="Автор курса"
              		  clearable
              		  box
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6>
		          <v-text-field
		            type="number"
		            label="Количество попыток"
		            :rules="rules"
		            box
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
		            :rules="rules"
		            hint="В процентах (%)"
		            value="75"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Хорошо'"
		            :rules="rules"
		            hint="В процентах (%)"
		            value="50"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4>
		          <v-text-field
		            type="number"
		            label="Оценка 'Удовлетворительно'"
		            :rules="rules"
		            hint="В процентах (%)"
		            value="25"
		            box
		            required
              		clearable
		          ></v-text-field>
		        </v-flex>	
				<v-flex xs12>
					<v-btn round color="success" dark large>
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
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

    export default {
        components: { FileInput, AddedQuestion },

		data () {
		    return {
        		rules: [ (value) => !!value || 'Это обязательное поле' ],

                image: '',
                imageTitle: '',
                imageDescription: '',
                imageLoadText: 'Изображение к тесту',

			    enabledImage: false,
			    questions: [],
			    questionsChecks: [],
			    error : false
		    }
		},
		methods: {
			getAddedQuestions() {
				//Axios.get(`${TestingSystemAPI}/api/questionslist/`, {
					Axios.get('https://jsonplaceholder.typicode.com/posts', {
		          //headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = data
		        }).catch(error => {
		          this.error = true
		          //this.message = 'Не удалось получить список вопросов'

		          console.log(error)
		        })
			}
		},
		mounted(){
			this.getAddedQuestions()
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