<template>
	<v-flex xs12>

		<v-layout row wrap v-if="currentType == 2 || currentType == 3">

			<v-flex v-if="currentType == 2" xs12>
        	  	<v-label>Максимальный балл за ответ</v-label>
				<v-tooltip bottom v-model="showWeight2typeTooltip">
			        <v-btn slot="activator" @click="showWeight2typeTooltip = !showWeight2typeTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
			        <span>Данная система тестирования такова, что она позволяет не только выполнить срез знаний пользователя, но и заставить его подумать и научиться, если он не очень качественно знает материал. Пользователю предоставляются дополнительные попытки на ответ в случае неверных ответов. Но с каждым неверным ответом количество возможных баллов, которые можно получить из каждого ответа, делятся пополам, если они не были отмечены верно.</span>
	        	</v-tooltip>
	          <v-text-field
                type="number"
                class="mr-2"
                value="256"
	            :rules="[rules.weight]"
                solo
                required
	          ></v-text-field>
	        </v-flex>

			<v-flex xs12>
				<div class="headline">
					<span v-if="currentType != 1">
						Ответы: 
					</span>
					<v-tooltip bottom v-model="showAnswersTooltip">
				        <v-btn slot="activator" @click="showAnswersTooltip = !showAnswersTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <p>Самым важным этапом является добавление вариантов ответов в вопрос. К каждому варианту ответа укажите текст ответа, отметьте, верен ли этот вариант ответа и обозначьте приоритет проверки. Вы можете добавить не более 15 вариантов ответа к одному вопросу. Нужно учитывать, что в процессе прохождения теста, тестируемому может быть показано только до 8 вариантов, которые будут выбраны случайно из всех добавленных. При этом гарантируется, что все правильные варианты будут показаны.</p>
		        	</v-tooltip>
				</div>
			</v-flex>
	    </v-layout>

		<v-radio-group v-model="oneAnswerRadios">

		<v-layout row wrap v-for="answer in answers">

			<v-layout row wrap v-if="currentType==1">

			<v-flex xs12>
				<h4 class="headline mb-2">Ответ: </h4>
			</v-flex>
				<v-flex xs12 sm6 xl4>
	        	  	<v-label>Правильный ответ</v-label>
					<v-tooltip bottom v-model="showAnswerTooltop">
				        <v-btn slot="activator" @click="showAnswerTooltop = !showAnswerTooltop" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Ответ может быть как числовым, так и текстовым. Ожидается, что ответ тестируемого должен полностью совпасть со значением, указанным в данном поле.</span>
		        	</v-tooltip>
		          <v-text-field
		            class="mr-2"
		            type="text"
		            solo
		            v-model="answer.text"
		            :rules="[rules.required, rules.answer]"
		            required
		  			clearable
		          ></v-text-field>
		        </v-flex>

				<v-flex xs12 sm6 xl4>
					<v-label>Комментарий к формату ответа</v-label>
					<v-tooltip bottom v-model="showCommentTooltip">
				        <v-btn slot="activator" @click="showCommentTooltip = !showCommentTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Опциональное поле. Помогает избежать неприятных ошибок, связанных с введением пользователем ответа в формате, не совпадающем с вашей задумкой. Например, можно указать здесь: "Ответ введите кириллицей с маленькой буквы, каждое новое слово через пробел".</span>
		        	</v-tooltip>
		          <v-text-field
		            class="ml-2"
		            type="text"
		            v-model="answer.comment"
		            :rules="[rules.comment]"
		            solo
		  			clearable
		          ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm6 xl4>
					<v-label>Максимальный балл за ответ</v-label>
					<v-tooltip bottom v-model="showWeightTooltip">
				        <v-btn slot="activator" @click="showWeightTooltip = !showWeightTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Данная система тестирования такова, что она позволяет не только выполнить срез знаний пользователя, но и заставить его подумать и научиться, если он не очень качественно знает материал. Пользователю предоставляются дополнительные попытки на ответ в случае неверных или неполных ответов. Но с каждым неверным ответом количество возможных баллов, которые можно получить из ответа, делятся пополам, если ответ не был введен верно.</span>
		        	</v-tooltip>
	              <v-text-field
	                type="number"
	                class="mr-2"
	                v-model="answer.weight"
	                value="0"
		            :rules="[rules.weight]"
	                required
	                solo
	              ></v-text-field>
	            </v-flex>

				<v-flex xs12 v-for="mode in modes">
					<v-layout row wrap>
						<v-flex xs12 sm6>
							<p class="title">{{modes.indexOf(mode) + 1}}. Режим: {{mode.name}}</p>
						</v-flex>
						<v-flex xs12 v-if="edit">
						      <v-label>Замена изображения и аудио:</v-label>
						      <v-tooltip bottom v-model="answer.showMediaTooltip">
							    <v-btn slot="activator" @click="answer.showMediaTooltip = !answer.showMediaTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
							    <span>Если вы хотите оставить изображение или аудио без изменений, убедитесь, что галочки ниже не отмечены. Если же хотите удалить их, отметьте галочку, но не загружайте новый файл. Для изменения изображения или аудио загрузите новый файл.</span>
					          </v-tooltip>
					      </v-flex>
			            <v-flex xs12 sm6 px-2>
							<v-label v-if="!edit">Аудиоподсказка</v-label>
			    			<v-layout align-center>
					          	<v-checkbox @click.native="changeAudio(answers.indexOf(answer), modes.indexOf(mode))" v-model="answer.enabledAudio[modes.indexOf(mode)]" hide-details class="shrink mr-2"></v-checkbox>
					            <file-input 
					            	class="fileBtn"
				                    accept="audio/*"
				                    ref="fileInput"
		                        	@input="getUploadedAudio($event, answers.indexOf(answer), modes.indexOf(mode))"
		                        	@update:deleteFile="deleteFile(1, answers.indexOf(answer), modes.indexOf(mode))"
						            :dis="!answer.enabledAudio[modes.indexOf(mode)]"
						            :checked="answer.enabledAudio[modes.indexOf(mode)]"
						            :label="answer.audioLoadText[modes.indexOf(mode)]"
					            ></file-input>
					        </v-layout>
					    </v-flex>
					</v-layout>

					<v-layout row wrap>
			            <v-flex xs12 sm6 px-2>
			            	<v-label>Текстовая подсказка</v-label>
							<v-tooltip bottom v-model="answer.showHintTooltip[modes.indexOf(mode)]">
						        <v-btn slot="activator" @click="clickHintTooltip(answers.indexOf(answer), modes.indexOf(mode))" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
						        <span>Опциональное поле. Если тестируемый ответит неверно, то всплывет подсказка, которая должна содержать намек на то, как правильно находить решение. В идеале постарайтесь, чтобы подсказка не слишком сильно облегчала задачу, но и позволяла тестируемому дать направление для размышлений. Также есть возможность загрузить аудиоподсказку, дополняющую или дублирующую текстовую.</span>
				        	</v-tooltip>
			              <v-text-field
			                type="text"
			                v-model="answer.hints[modes.indexOf(mode)]"
			                :rules="[rules.hint]"
			                clearable
			                solo
			              ></v-text-field>
			            </v-flex>

						<v-flex xs12 sm6 px-2>
			            	<v-label>Видеоподсказка (ссылка)</v-label>
			            	<v-tooltip bottom v-model="answer.showVideoTooltip[modes.indexOf(mode)]">
						        <v-btn slot="activator" @click="clickVideoTooltip(answers.indexOf(answer), modes.indexOf(mode))" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
						        <span>Опциональное поле. Вы можете добавить видеореакцию на ответ, содержащую намек на то, в чем может быть неправ учащийся. Если добавлена ссылка на видео, загруженное аудио воспроизводиться при прохождении не будет.</span>
				        	</v-tooltip>
			              <v-text-field
			                type="text"
			                v-model="answer.videos[modes.indexOf(mode)]"
			                clearable
			                solo
			              ></v-text-field>
			            </v-flex>
					</v-layout>
				</v-flex>

			</v-layout>

			<v-layout row wrap v-else-if="currentType == 2 || currentType == 3">
				<div class="divider"></div>

				<v-flex xs12>
					<v-label>Текст ответа</v-label>
				  <div class="ansPrefix title">{{answers.indexOf(answer) + 1}}.</div>
		          <v-text-field
		            type="text"
		            v-model="answer.text"
		            :rules="[rules.required, rules.answer]"
		            required
		            solo
		  			clearable
		          ></v-text-field>
				</v-flex>

				<v-flex xs12 sm6 px-1 v-if="currentType==3" >

					<v-label>Максимальный балл</v-label>
					<v-tooltip bottom >
				        <v-btn slot="activator"  icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Данная система тестирования такова, что она позволяет не только выполнить срез знаний пользователя, но и заставить его подумать и научиться, если он не очень качественно знает материал. Пользователю предоставляются дополнительные попытки на ответ в случае неверных или неполных ответов. Но с каждым неверным ответом количество возможных баллов, которые можно получить из каждого ответа, делятся пополам, если они не были отмечены верно.</span>
		        	</v-tooltip>
		          <v-text-field :disabled="!answer.correct"
		            type="number"
		            :rules="[rules.weight]"
		            v-model="answer.weight"
		            :value="0"
		            required
		            solo
		  			clearable
		          ></v-text-field>
				</v-flex>

				<v-flex xs12 sm6 px-1 v-if="currentType==3">
					<v-label>Приоритет проверки</v-label>
					<v-tooltip bottom >
				        <v-btn slot="activator" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Приоритет проверки означает, в каком порядке в случае неверного ответа будет воспроизводиться подсказка для пользователя. Приоритеты должна начинаться с 1 и идти по порядку. Этим значениям и будет соответствовать порядок проверки вариантов ответа на правильность. Например, пользователь указал как верные ответы, которым соответствуют приоритеты 2 и 4. Если ответ с приоритетом 1 являлся верным, а пользователь его не отметил - пользователю будет выведена подсказка, соответствующая ответу с приоритетом 1. А если этот ответ и был неверен, проверка перейдет к ответу с приоритетом 2 и проверит его. Если наш ответ с приоритетом 2, который отметил пользователь, был бы неверным - то пользователю была бы показана подсказка к ответу с приоритетом 2. А если этот ответ действительно верен, то проверка пойдет дальше. Таким образом, внимательно расставьте приоритеты к ответам (например, от самых простых вариантов ответа до самых сложных). Как правило, обычно бывает уместным первыми приоритетами указывать неверные ответы, так как за них не начисляются баллы, а последними приоритетами - верные, по мере увеличения баллов за ответ.</span>
		        	</v-tooltip>
		          <v-text-field
		            type="number"
		            v-model="answer.priority"
		            :rules="[rules.priority,rules.duplicatePriority]"
		            solo
		            required
		          ></v-text-field>
				</v-flex>

				<v-flex xs12 v-if="edit">
			      <v-label>Замена изображения и аудио:</v-label>
			      <v-tooltip bottom v-model="answer.showMediaTooltip">
				    <v-btn slot="activator" @click="answer.showMediaTooltip = !answer.showMediaTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				    <span>Если вы хотите оставить изображение или аудио без изменений, убедитесь, что галочки ниже не отмечены. Если же хотите удалить их, отметьте галочку, но не загружайте новый файл. Для изменения изображения или аудио загрузите новый файл.</span>
		          </v-tooltip>
		      </v-flex>

	          <v-flex xs12 sm6 mb-3>
				<v-label v-if="!edit">Изображение: </v-label>
    			<v-layout align-center>
		          	<v-checkbox @click.native="changeImage(answers.indexOf(answer))" v-model="answer.enabledImage" hide-details class="shrink mr-2" ></v-checkbox>

		            <file-input 
		            class="fileBtn"
                    accept="image/*"
                    ref="fileInput"
                    @update:deleteFile="deleteFile(0, answers.indexOf(answer))"
                    @input="getUploadedImage($event, answers.indexOf(answer))"
                    :checked="answer.enabledImage"
		            :dis="!answer.enabledImage"
		            :label="answer.imageLoadText"
		            ></file-input>
		        </v-layout>
		      </v-flex>

				<v-flex xs12 sm6>
		          <v-switch 
		            v-if="currentType==3"
			        :label="isTrueText"
			        v-model="answer.correct"
			        @change="changeCheck(answers.indexOf(answer), $event)"
			      ></v-switch>
			      <v-radio 
			        v-if="currentType==2"
			        class="ma-3"
			        v-model="answers.indexOf(answer)"
			        @change="checkRadios($event)"
			      	:label="isTrueText"
			      ></v-radio>
				</v-flex>

				<v-flex xs12 v-for="mode in modes">
					<v-layout row wrap>
						<v-flex xs12 sm6>
							<p class="title">{{modes.indexOf(mode) + 1}}. Режим: {{mode.name}}</p>
						</v-flex>
						<v-flex xs12 sm6 px-2>
							<v-label v-if="!edit">Аудиоподсказка: </v-label>
			    			<v-layout align-center>
					          	<v-checkbox @click.native="changeAudio(answers.indexOf(answer), modes.indexOf(mode))" v-model="answer.enabledAudio[modes.indexOf(mode)]" hide-details class="shrink mr-2"></v-checkbox>
					            <file-input 
					            class="fileBtn"
			                    accept="audio/*"
			                    ref="fileInput"
		                        @input="getUploadedAudio($event, answers.indexOf(answer), modes.indexOf(mode))"
		                        @update:deleteFile="deleteFile(1, answers.indexOf(answer), modes.indexOf(mode))"
		                        :checked="answer.enabledAudio[modes.indexOf(mode)]"
					            :dis="!answer.enabledAudio[modes.indexOf(mode)]"
					            :label="answer.audioLoadText[modes.indexOf(mode)]"
					            ></file-input>
					        </v-layout>
					      </v-flex>
					</v-layout>

					<v-layout row wrap>
						<v-flex xs12 sm6 px-2>
							<v-label>Текстовая подсказка</v-label>
							<v-tooltip bottom v-model="answer.showHintTooltip[modes.indexOf(mode)]">
						        <v-btn slot="activator" @click.native="clickHintTooltip(answers.indexOf(answer), modes.indexOf(mode))" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
						        <span>Опциональное поле. Если тестируемый ответит неверно, то всплывет подсказка, которая должна содержать намек на то, как правильно находить решение. В идеале постарайтесь, чтобы подсказка не слишком сильно облегчала задачу, но и позволяла тестируемому дать направление для размышлений. Также есть возможность загрузить аудиоподсказку, дополняющую или дублирующую текстовую.</span>
				        	</v-tooltip>
				          <v-text-field
				            type="text"
				            v-model="answer.hints[modes.indexOf(mode)]"
				            :rules="[rules.hint]"
				            solo
				          ></v-text-field>
						</v-flex>

						<v-flex xs12 sm6 px-2>
			            	<v-label>Видеоподсказка (ссылка)</v-label>
			            	<v-tooltip bottom v-model="answer.showVideoTooltip[modes.indexOf(mode)]">
						        <v-btn slot="activator" @click="clickVideoTooltip(answers.indexOf(answer), modes.indexOf(mode))" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
						        <span>Опциональное поле. Вы можете добавить видеореакцию на ответ, содержащую намек на то, в чем может быть неправ учащийся. Если добавлена ссылка на видео, загруженное аудио воспроизводиться при прохождении не будет.</span>
				        	</v-tooltip>
			              <v-text-field
			                type="text"
			                v-model="answer.videos[modes.indexOf(mode)]"
			                clearable
			                solo
			              ></v-text-field>
			            </v-flex>
						  
					  </v-layout>
				  </v-flex>

			</v-layout>
		</v-layout>

		</v-radio-group>

		<v-layout row wrap v-if="currentType == 2 || currentType == 3">

				<v-layout column align-center justify-center>
					<v-flex xs12 class="mb-3" >
						<v-tooltip bottom>
							<v-btn 
							slot="activator"
							v-if="localCountAnswers < maxAnswers" 
							fab
							color="success" 
							@click="incLCA()" 
							dark
							class="elevation-3"
							><v-icon size="32px">
								plus_one
							</v-icon>
							</v-btn>
							<span>Добавить вариант ответа</span>
						</v-tooltip>

						<v-tooltip bottom>
							<v-btn 
							slot="activator"
							v-if="localCountAnswers > minAnswers" 
							fab
							color="error" 
							@click="decLCA()" 
							dark
							class="elevation-3"
							><v-icon size="32px">
								close
							</v-icon>
							</v-btn>
							<span>Удалить последний вариант ответа</span>
						</v-tooltip>
					</v-flex>	
				</v-layout>

				<div class="divider"></div>
				<v-flex xs12>
					<v-label>Количество ответов, включаемых в вопрос</v-label>
					<v-tooltip bottom v-model="showQtyTooltip">
				        <v-btn slot="activator" @click="showQtyTooltip = !showQtyTooltip" icon small><v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Поле показывает, сколько вариантов ответов из добавленных выше (случайным выбором) будет предложено тестируемому для ответа. Максимально допустимое значение - 8.</span>
		        	</v-tooltip>
		          <v-text-field
		            v-model="answersQty"
		            type="number"
		            :rules="[rules.maxAns]"
		            :value="countAnswers"
		            required
		            solo
		          ></v-text-field>
		        </v-flex>
		</v-layout>
	</v-flex>
</template>

<script>
    import FileInput from '@/components/other/FileLoader'

	export default {
		props: ['currentType', 'countAnswers', 'answers', 'answersQty', 'edit', 'modes'],
		components: { FileInput },
		data() {
			return {
				isTrueText: 'Ответ верен',
                imageLoadText: 'Изображение к ответу',
				audio: '',

                rules: {
                	required: value => !!value || 'Это необходимое поле',
                	maxAns: value => ((value >= 2) && (value <= this.localCountAnswers) && (value <= this.maxIncludedAnswers))  || 'Введите значение не больше количества элементов, добавленных выше, и также не превышающее '+ this.maxIncludedAnswers,
                	weight: value => (value >= this.minWeight && value <= this.maxWeight) || 'Введите значение в диапазоне от '+this.minWeight+' до '+this.maxWeight,
                	priority: value => (value >= this.minPriority && value <= this.maxPriority) || 'Введите значение в диапазоне от '+this.minPriority+' до '+ this.maxPriority,
                	duplicatePriority: value => !this.findDuplicates(value) || 'Такое значение уже есть у другого ответа',
                	answer: value => (!value || (!!value && value.length <= this.maxAnswerLength)) || 'Максимальная длина поля '+this.maxAnswerLength+' символов',
                	comment: value => (!value || (!!value && value.length <= this.maxCommentLength)) || 'Максимальная длина поля '+this.maxCommentLength+' символов',
                	hint: value => (!value || (!!value && value.length <= this.maxHintLength)) || 'Максимальная длина поля '+this.maxHintLength+' символов'
                },
        		oneAnswerRadios: 0,
        		maxAnswers:15,
        		minAnswers: 2,
        		maxAnswerLength:250,
        		maxCommentLength: 150,
        		maxHintLength: 300,
        		minWeight: 0,
        		maxWeight: 1000,
        		minPriority: 1,
        		maxPriority: 15,
        		maxVideoLength: 150,
        		maxIncludedAnswers: 8,
        		showAnswerTooltop: false,
        		showCommentTooltip: false,
        		showWeightTooltip: false,
				showMediaTooltip: false,
        		showHintTooltip: false,
        		showWeight2typeTooltip: false,
        		showAnswersTooltip: false,
        		showQtyTooltip: false,
			}
		},
		methods: {
			incLCA() {
				this.localCountAnswers++
				this.$emit('push')
			},
			decLCA() {
				this.localCountAnswers--
				this.answers.pop()
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
			checkRadios(arg) {
				if (this.currentType != 2)
					return
				for (var i = 0; i < this.answers.length; ++i)
					if (i == arg)
						this.answers[i].correct = true
					else this.answers[i].correct = false
			},
			getUploadedAudio(e, index, mode) {
				this.$emit('update:answersAudio', {'audio' : e, 'index': index, 'mode' : mode})
			},
			getUploadedImage(e, index) {
				this.$emit('update:answersImage', {'image' : e, 'index': index})
			},
			changeCheck(i, e){
				this.answers[i].weight = this.answers[i].correct ? 256 : 0
			},
			changeAudio(ind, mode){
				this.$emit('update:changeAudio', {'index' : ind, 'mode': mode})
			},
			changeImage(ind){
				this.$emit('update:changeImage', ind)
			},
			deleteFile(isAudio, i, mode){
				if (isAudio)
					this.answers[i].audios[mode] = null
				else this.answers[i].image = null
			},
			clickHintTooltip(ans, mode){
				this.$emit('update:clickHintTooltip', {'answer' : ans, 'mode': mode})
			},
			clickVideoTooltip(ans, mode){
				this.$emit('update:clickVideoTooltip', {'answer' : ans, 'mode': mode})
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
			},
			countAnswers: function(val) {
				if (this.edit)
					return
				this.answersQty = val
				this.$emit('update:answersQty', this.answersQty)
			},
			answersQty: function(val) {
				this.$emit('update:answersQty', val)
			}
		}
	}
</script>

<style>
	.ansPrefix{
		position: relative;
		left:-20px;
		float:left;
	}
	.divider{
		height:1px;
		width:100%;
		background: #bbb;
		margin-bottom:15px;
	}
</style>