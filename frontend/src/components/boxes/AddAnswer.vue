<template>
	<v-container>
		<v-layout row wrap>

			<v-flex xs12>
			  <div class="ansPrefix title">{{curNumber}}.</div>
	          <v-text-field
	            type="text"
	            label="Текст ответа"
	            v-model="answer.text"
	            :rules="rules"
	            required
	  			clearable
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 v-if="currentType==3">
	          <v-text-field
	            type="number"
	            label="Максимальный балл"
	            v-model="answer.weight"
	            :rules="rules"
	            required
	  			clearable
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 >
	          <v-text-field
	            type="number"
	            label="Приоритет проверки"
	            v-model="answer.priority"
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4> 
	          <v-text-field
	            type="text"
	            label="Подсказка"
	            v-model="answer.hint"
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 >
	          <v-switch 
	            v-if="currentType==3"
		        :label="isTrueText"
		        v-model="answer.correct"
		      ></v-switch>
		      <v-radio 
		        v-if="currentType==2"
		        class="mx-3 my-3"
		        v-model="answer.correct"
		      	:label="isTrueText" 
		      	:value="curNumber"
		      ></v-radio>
			</v-flex>

			  <v-flex xs12 sm4 xl3>
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
	          <v-flex xs12 sm4 xl3>
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


		</v-layout>
	</v-container>
</template>

<script>
    import FileInput from '@/components/other/FileLoader'
	export default {
		props: ['currentType', 'curNumber', 'answers', 'countAnswers'],
		components: { FileInput },
		data() {
			return {
				isTrueText: 'Ответ верен',
				enabledAudio: false,
				enabledImage: false,
                imageLoadText: 'Изображение к ответу',
                audioLoadText: 'Аудиоподсказка',
        		rules: [ (value) => !!value || 'Это обязательное поле' ],
                answer: {
                	image: '',
                	audio: '',
                	text: '',
                	priority: '',
                	correct: false,
                	weight: 256,
                	hint: '',
                	comment: '',
                	question: ''
                }
			}
		},
		methods: {
            getUploadedImage(e) {
                this.answer.image = e
            },
            getUploadedAudio(e) {
                this.answer.audio = e
            }
		},
		watch: {
			answer: function() {
				alert('hi')
				this.answers[this.curNumber-1] = this.answer
            	for (var i = 0; i < this.answers.length; ++i)
            		console.log(this.answers[i])
			}
		}
	}
</script>

<style>
	.ansPrefix{
		position: relative;
		left:-10px;
		top: 20px;
		float:left;
	}
</style>