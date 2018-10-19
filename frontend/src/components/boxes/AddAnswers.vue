<template>
	<v-flex xs12>

		<v-layout row wrap v-if="currentType == 2 || currentType == 3">
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
	    </v-layout>

		<v-radio-group v-model="oneAnswerRadios">

		<v-layout row wrap v-for="answer in answers">

			<v-layout row wrap v-if="currentType==1">


				<v-flex xs12>
					<h4 class="title mb-2">Ответ: </h4>
				</v-flex>
				<v-flex xs12 sm6>
		          <v-text-field
		            class="mr-2"
		            type="text"
		            label="Правильный ответ"
		            v-model="answer.text"
		            :rules="rules"
		            required
		  			clearable
		          ></v-text-field>
		        </v-flex>

				<v-flex xs12 sm6>
		          <v-text-field
		            class="ml-2"
		            type="text"
		            v-model="answer.comment"
		            label="Комментарий к формату ответа"
		            hint="Например, 'Округлить до двух знаков после запятой'"
		  			clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6>
	              <v-text-field
	                type="number"
	                class="mr-2"
	                label="Максимальный балл за ответ"
	                v-model="answer.weight"
		            :rules="rules"
	                required
	              ></v-text-field>
	            </v-flex>

	            <v-flex xs12 sm6>
	              <v-text-field
	                type="text"
	                class="ml-2"
	                label="Текстовая подсказка"
	                v-model="answer.hint"
	                clearable
	              ></v-text-field>
	            </v-flex>

	            <v-flex xs12 sm6 xl3>
	    			<v-layout align-center>
			          	<v-checkbox v-model="answer.enabledAudio" hide-details class="shrink mr-2"></v-checkbox>
			            <file-input 
		                    accept="audio/*"
		                    ref="fileInput"
                        	@input="getUploadedAudio($event, answers.indexOf(answer))"
				            :dis="!answer.enabledAudio"
				            :checked="answer.enabledAudio"
				            :label="audioLoadText"
			            ></file-input>
			        </v-layout>
			    </v-flex>

			</v-layout>

			<v-layout row wrap v-else-if="currentType == 2 || currentType == 3">

				<v-flex xs12>
				  <div class="ansPrefix title">{{answers.indexOf(answer) + 1}}.</div>
		          <v-text-field
		            type="text"
		            label="Текст ответа"
		            v-model="answer.text"
		            :rules="rules"
		            required
		  			clearable
		          ></v-text-field>
				</v-flex>

				<v-flex xs12 sm4 v-if="currentType==3" >
		          <v-text-field :disabled="answer.correct == 0"
		            type="number"
		            label="Максимальный балл"
		            v-model="answer.weight"
		            required
		  			clearable
		          ></v-text-field>
				</v-flex>

				<v-flex xs12 sm4 >
		          <v-text-field
		            type="number"
		            label="Приоритет проверки"
		            v-model="answer.priority"
		            :rules="rulesDuplicatePriority"
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
			        @change="changeCheck(answers.indexOf(answer))"
			      ></v-switch>
			      <v-radio 
			        v-if="currentType==2"
			        class="mx-3 my-3"
			        v-model="answers.indexOf(answer)"
			        @change="checkRadios()"
			      	:label="isTrueText" 
			      ></v-radio>
				</v-flex>

				  <v-flex xs12 sm4 xl3>
	    			<v-layout align-center>
			          	<v-checkbox v-model="answer.enabledAudio" hide-details class="shrink mr-2"></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="audio/*"
	                    ref="fileInput"
                        @input="getUploadedAudio($event, answers.indexOf(answer))"
                        :checked="answer.enabledAudio"
			            :dis="!answer.enabledAudio"
			            :label="audioLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>
		          <v-flex xs12 sm4 xl3>
	    			<v-layout align-center>
			          	<v-checkbox v-model="answer.enabledImage" hide-details class="shrink mr-2" ></v-checkbox>
			            <file-input 
			            class="fileBtn"
	                    accept="image/*"
	                    ref="fileInput"
                        @input="getUploadedImage($event, answers.indexOf(answer))"
                        :checked="answer.enabledImage"
			            :dis="!answer.enabledImage"
			            :label="imageLoadText"
			            ></file-input>
			        </v-layout>
			      </v-flex>

			</v-layout>
		</v-layout>

		</v-radio-group>

		<v-layout row wrap v-if="currentType == 2 || currentType == 3">

				<v-layout column align-center justify-center>
					<v-flex xs12 class="mb-3" >
						<v-btn 
						v-if="localCountAnswers < maxAnswers" 
						icon 
						color="success" 
						@click="incLCA()" 
						dark
						large
						><v-icon size="32px">
								plus_one
							</v-icon>
						 </v-btn>

						 <v-btn 
						 v-if="localCountAnswers > minAnswers" 
						 icon 
						 color="error" 
						 @click="decLCA()" 
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
		            label="Количество ответов, включаемых в вопрос"
		            :rules="rulesMaxAns"
		            :value="countAnswers"
		            hint="Из добавленных выше"
		            required
		            box
		          ></v-text-field>
		        </v-flex>
		</v-layout>
	</v-flex>
</template>

<script>
    import FileInput from '@/components/other/FileLoader'

	export default {
		props: ['currentType', 'countAnswers', 'answers'],
		components: { FileInput },
		data() {
			return {
				audioLoadText: 'Аудиоподсказка',
				isTrueText: 'Ответ верен',
                imageLoadText: 'Изображение к ответу',
				audio: '',
        		rules: [ (value) => !!value || 'Это обязательное поле' ],
        		rulesMaxAns: [ (value) => ((value >= 2) && (value <= this.localCountAnswers) && (value <= this.maxIncludedAnswers))  || 'Должно быть не больше количества элементов, добавленных выше, и не превышать '+ this.maxIncludedAnswers],
        		rulesDuplicatePriority: [(value) => !this.findDuplicates(value) || 'Такое значение уже есть у другого ответа'],
        		oneAnswerRadios: 0,
        		maxAnswers:15,
        		minAnswers: 2,
        		maxIncludedAnswers: 8
			}
		},
		methods: {
			incLCA() {
				this.localCountAnswers++
				this.$emit('push')

				console.log('countAnswers: '+ this.countAnswers)
				console.log('localCountAnswers: '+ this.localCountAnswers)
            	console.log('array len: ' + this.answers.length)

            	console.log(this.answers)
			},
			decLCA() {
				this.localCountAnswers--
				this.answers.pop()

				console.log('countAnswers: '+ this.countAnswers)
				console.log('localCountAnswers: '+ this.localCountAnswers)
            	console.log('array len: ' + this.answers.length)

            	console.log(this.answers)
			},
			findDuplicates(value) {
				var found = false
				for (var i = 0; i < this.answers.length; ++i)
					if (this.answers[i].priority == value)
						if (found)
							return true
						else found = true
				return false
			},
			checkRadios() {
				if (this.currentType != 2)
					return
				for (var i = 0; i < this.answers.length; ++i)
					if (i == this.oneAnswerRadios)
						this.answers[i].correct = true
					else this.answers[i].correct = false
			},
			getUploadedAudio(e, index) {
				this.$emit('update:answersAudio', {'audio' : e, 'index': index})
			},
			getUploadedImage(e, index) {
				this.$emit('update:answersImage', {'image' : e, 'index': index})
			},
			changeCheck(index){
				for (var i = 0; i < this.answers.length; ++i)
					if (i == index)
					{
						this.answers[i].weight = this.answers[i].correct ? 256 : 0
						return
					}
			}
		},
		computed: {
			localCountAnswers: {
				get() {
					return this.countAnswers
				},
				set(v){
					this.$emit('update:countAnswers', v)
				}
			}
		},
		watch: {
			currentType: function(val) {
				if (val == 2)
					this.checkRadios()
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