<template>
	<v-form @submit.prevent="onSubmit">
		<v-container>
			<v-layout row wrap>
				<h4 class="display-1">Редактирование вопроса</h4>
				<v-flex xs12>
		            <v-text-field
		              label="Краткое название (будет видно только вам)"
		              required
              		  clearable
              		  :rules="rules"
              		  box
		            ></v-text-field>
		        </v-flex>
		        <v-flex xs12>
			        <v-textarea
			            name="input-7-1"
			            label="Формулировка вопроса"
			            hint="Не более 2000 символов"
          		  		:rules="rules"
			            required
              			clearable
              			box
			          ></v-textarea>
		        </v-flex>

		          <v-flex xs12 sm6 xl3>
	        			<v-layout align-center>
			          	<v-checkbox v-model="enabledAttempts" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type='number' 
			            :disabled="!enabledAttempts"
			            label="Количество попыток"
              			clearable
              			box
			            ></v-text-field>
				      </v-layout>
		          </v-flex>

		          <v-flex xs12 sm6 xl3>
        			<v-layout align-center>
			          	<v-checkbox v-model="enabledTimer" hide-details class="shrink mr-2"></v-checkbox>
			            <v-text-field type='number' 
			            :disabled="!enabledTimer"
			            label="Таймер на вопрос"
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
                        @input="getUploadedImage"
			            :dis="!enabledImage"
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
                        @input="getUploadedAudio"
			            :dis="!enabledAudio"
			            :label="audioLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

				<v-flex xs10>
	              <v-slider
	                v-model="difficulty"
	                :max="100"
	                label="Сложность вопроса"
	              ></v-slider>
	            </v-flex>
	            <v-flex xs2>
	              <v-text-field
	                v-model="difficulty"
	                type="number"
	                box
	              ></v-text-field>
	            </v-flex>

				<v-flex xs12>
		          <v-select
		            v-model="currentType"
		          	@change="changeAnswerType"
		            :items="answerTypes"
		            item-value="id"
		            item-text="val"
			        label="Тип ответа"
      		  		:rules="rules"
		            box
		            required
		           ></v-select>
		        </v-flex>
				<add-answers 
					:currentType="currentType"
					:countAnswers="countAnswers"
				></add-answers>
				<v-flex xs12>
					<v-btn round color="success" dark large>
						 Сохранить вопрос
					</v-btn>
				</v-flex>
			</v-layout>
		</v-container>
	</v-form>
</template>

<script>
    import axios from 'axios'
    import FileInput from '@/components/other/FileLoader.vue'
    import AddAnswers from '@/components/boxes/AddAnswers.vue'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
        components: {FileInput, AddAnswers},

		data () {
		    return {
		    	enabledAttempts: false,
			    enabledTimer: false,
			    enabledImage: false,
			    enabledAudio: false,

      			difficulty: 0,
      			selectedType: [],
      			currentType: 1,
				countAnswers: 1,
      			answerTypes: [
	      			{ id: 1, val: 'Ввод значения'}, 
	      			{ id: 2, val : 'Выбор одного варианта'}, 
	      			{ id: 3, val : 'Выбор нескольких вариантов'}
      			],
        		rules: [ (value) => !!value || 'Это обязательное поле' ],

                image: '',
                imageTitle: '',
                imageDescription: '',
                imageLoadText: 'Изображение к вопросу',

                audio: '',
                audioTitle: '',
                audioDescription: '',
                audioLoadText: 'Голосовое воспроизведение',
		    }
		  },
		methods: {
            getUploadedImage(e) {
                this.image = e
            },
            getUploadedAudio(e) {
                this.audio = e
            },
            onSubmit() {
                 let formData = new FormData()
                 formData.set('image', this.image)
                 formData.set('imageTitle', this.imageTitle)
                 formData.set('imageDescription', this.imageDescription)

                 formData.set('audio', this.audio)
                 formData.set('audioTitle', this.audioTitle)
                 formData.set('audioDescription', this.audioDescription)

                 axios.post(`${TestingSystemAPI}/api/questions/`, formData)
	               .then(response => {
	                    // Any Code
	                })
	               .catch(error => {
	                    // Any Code
	                })
            },
            getQuestionData()
            {
            	Axios.get(`${TestingSystemAPI}/api/questions/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.tests = data
		        }).catch(error => {
		          this.snackbar = true
		          this.message = 'Не удалось получить список тестов'

		          console.log(error)
		        })
            }
       },
       watch: {
       		currentType: function(val){
       			if (val == 1)
       				this.countAnswers = 1
       			else if (val == 2 || val == 3)
       				this.countAnswers = 2
       		}
       },
       mounted() {
       		this.getQuestionData()
       }
	}
</script>

<style>
</style>