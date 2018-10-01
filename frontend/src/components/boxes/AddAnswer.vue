<template>
	<v-container>
		<v-layout row wrap>

			<v-flex xs12>
			  <div class="ansPrefix title">{{curNumber}}.</div>
	          <v-text-field
	            type="text"
	            label="Текст ответа"
	            :rules="rules"
	            required
	  			clearable
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 v-if="currentType==3">
	          <v-text-field
	            type="number"
	            label="Максимальный балл"
	            :rules="rules"
	            required
	  			clearable
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 >
	          <v-text-field
	            type="number"
	            label="Приоритет проверки"
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4> 
	          <v-text-field
	            type="text"
	            label="Подсказка"
	          ></v-text-field>
			</v-flex>

			<v-flex xs12 sm4 >
	          <v-switch 
	            v-if="currentType==3"
		        :label="isTrueText"
		      ></v-switch>
		      <v-radio 
		        v-if="currentType==2"
		        class="mx-3 my-3"
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
		props: ['currentType', 'curNumber'],
		components: { FileInput },
		data() {
			return {
				isTrueText: 'Ответ верен',
				image: '',
				audio: '',
				enabledAudio: false,
				enabledImage: false,
                imageLoadText: 'Изображение к ответу',
                audioLoadText: 'Аудиоподсказка'
			}
		},
		methods: {
            getUploadedImage(e) {
                this.image = e
            },
            getUploadedAudio(e) {
                this.audio = e
            },
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