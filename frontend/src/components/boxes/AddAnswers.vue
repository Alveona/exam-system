<template>
	<v-flex xs12>
		<v-layout row wrap v-if="currentType==1">

			<v-flex xs12 sm6>
	          <v-text-field
	            class="mr-2"
	            type="text"
	            label="Правильный ответ"
	            v-model="answers[0].text"
	            :rules="rules"
	            required
	  			clearable
	  			box
	          ></v-text-field>
	        </v-flex>

			<v-flex xs12 sm6>
	          <v-text-field
	            class="ml-2"
	            type="text"
	            v-model="answers[0].comment"
	            label="Комментарий к формату ответа"
	            hint="Например, 'Округлить до двух знаков после запятой'"
	  			clearable
	  			box
	          ></v-text-field>
	        </v-flex>

	        <v-flex xs12 sm6>
              <v-text-field
                type="number"
                class="mr-2"
                label="Максимальный балл за ответ"
                v-model="answers[0].weight"
                value="256"
	            :rules="rules"
                box
                required
              ></v-text-field>
            </v-flex>

            <v-flex xs12 sm6>
              <v-text-field
                type="text"
                class="ml-2"
                label="Текстовая подсказка"
                v-model="answers[0].hint"
                box
              ></v-text-field>
            </v-flex>

            <v-flex xs12 sm6 xl3>
    			<v-layout align-center>
		          	<v-checkbox v-model="enabledAudio" hide-details class="shrink mr-2"></v-checkbox>
		            <file-input 
	                    accept="audio/*"
	                    ref="fileInput"
	                    @input="getUploadedAudio"
			            :dis="!enabledAudio"
			            :label="audioLoadText"
		            ></file-input>
		        </v-layout>
		    </v-flex>

		</v-layout>

		<v-layout row wrap v-else-if="currentType == 2 || currentType == 3">

			<v-flex v-if="currentType == 2" xs12>
	          <v-text-field
                type="number"
                class="mr-2"
                label="Максимальный балл за ответ"
                value="256"
	            :rules="rules"
                box
                required
	          ></v-text-field>
	        </v-flex>
			
			<v-flex xs12>
				<h4 v-if="currentType != 1" class="title">Ответы: </h4>
			</v-flex>
			<v-radio-group v-model="oneAnswerRadios">

			<v-flex xs12>
				<add-answer 
					v-for="answer in countAnswers"
					:currentType="currentType"
					:curNumber="answer"
					:answers="answers"
				></add-answer>
			</v-flex>

			</v-radio-group>

			<v-layout column align-center justify-center>
				<v-flex xs12 class="mb-3" >
					<v-btn 
					v-if="countAnswers <= 15" 
					icon 
					color="success" 
					@click.native="countAnswers++" 
					dark
					large
					><v-icon size="32px">
							plus_one
						</v-icon>
					 </v-btn>

					 <v-btn 
					 v-if="countAnswers > 2" 
					 icon 
					 color="error" 
					 @click.native="countAnswers--" 
					 dark
					 large
					><v-icon size="32px">
							close
						</v-icon>
					 </v-btn>
				</v-flex>	
			</v-layout>

			<v-flex xs12>
	          <v-text-field
	            type="number"
	            label="Количество ответов, включаемых в вопрос (не больше добавленных выше и не больше 8)"
	            :rules="rules"
	            :value="countAnswers"
	            required
	            box
	          ></v-text-field>
	        </v-flex>

		</v-layout>

	</v-flex>
</template>

<script>
    import FileInput from '@/components/other/FileLoader'
    import AddAnswer from '@/components/boxes/AddAnswer'

	export default {
		props: ['currentType', 'countAnswers', 'answers'],
		components: { FileInput, AddAnswer },
		data() {
			return {
				enabledAudio: false,
				audioLoadText: 'Голосовое воспроизведение подсказки',
				audio: '',
        		rules: [ (value) => !!value || 'Это обязательное поле' ],
        		oneAnswerRadios: 1
			}
		},
		methods: {
			getUploadedAudio(e){
                this.answers[0].audio = e
			}

		}
	}
</script>

<style>
	
</style>