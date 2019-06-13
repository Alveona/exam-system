<template>
	<div>
		<v-form ref="addMform">
			<v-layout row wrap>
				<v-flex xs12 sm4>
					<v-label>Название режима</v-label>
					<v-tooltip bottom v-model="showTitleTooltip">
				        <v-btn slot="activator" @click="showTitleTooltip = !showTitleTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Например, 'Покладистый добрый преподаватель'</span>
		        	</v-tooltip>
		            <v-text-field
		              required
              		  :rules="[rules.title, rules.required]"
              		  v-model="title"
              		  solo
		            ></v-text-field>
		        </v-flex>

		        <v-flex xs12 sm4 class="ml-3">
		        	<v-label>Изображение</v-label>
					<v-tooltip bottom v-model="showImageTooltip">
				        <v-btn slot="activator" @click="showImageTooltip = !showImageTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
				        <span>Будет отображаться при воспроизведении подсказок во время прохождения тестирования пользователями</span>
		        	</v-tooltip>
		            <file-input
		            class="fileBtn"
                    accept="image/*"
                    ref="fileInput"
                    @input="getUploadedImage"
		            :label="imageLoadText"
		            ></file-input>
			    </v-flex>

		        <v-flex xs12 sm3 class="pt-4">
		        	<v-btn :disabled="isSubmitting" @click="addMode()" round color="success"  dark>
			        	<v-icon size="24px" class="mr-2">
							add
						</v-icon>
					Добавить режим</v-btn>
		        </v-flex>

				<v-flex xs12>
					<v-alert
			        :value="alert"
			        :type="successLoad ? 'success' : 'error'"
					transition="scale-transition"
					outline
			        >
				        {{alert_message}}

				    </v-alert>
		        </v-flex>	
			</v-layout>
		</v-form>

		<v-layout row wrap v-if="successLoad">
			<v-flex xs12>

				<div class="content-wrapper">
					<v-layout row wrap>
		              <v-flex
		                v-for="mode in modes"
		                :key="mode.title"
		                v-bind="{ [`xs3`]: true }"
		                class="d-inline-block"
		                px-1
		                py-1
		              >
		                <v-card max-width="350" min-width="350">
		                  <v-img
		                    :src="mode.image"
		                    height="200px"
		                  >
		                  </v-img>
		  
		                  <v-card-actions>
		                  	<v-label>{{mode.name}}</v-label>
		                    <v-spacer></v-spacer>
		                    <v-tooltip bottom>
				              	<v-btn slot="activator" @click.native="deleteMode(mode.id)" icon><v-icon>delete</v-icon></v-btn>
				              	<span>Удалить режим</span>
					        </v-tooltip>
		                  </v-card-actions>
		                </v-card>
		              </v-flex>
		            </v-layout>
				</div>
				
			</v-flex>
		</v-layout>
	</div>
</template>

<script>
    import Axios from 'axios'
	import router from '@/router'
    import FileInput from '@/components/other/FileLoader'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'	

	const TestingSystemAPI = connection.server

	export default {
		components: { FileInput },
		data() {
			return {
				enabledImage: false,
				image: null,
				showImageTooltip: false,
				showTitleTooltip: false,
				alert: false,
				isSubmitting: false,
				successLoad: false,
				title: '',
				alert_message: '',
				imageLoadText: 'Изображение не загружено',
				rules: {
					title: val => (val.length >= this.minTitleLen && val.length <= this.maxTitleLen) || 'Длина названия должна быть в диапазоне от '+this.minTitleLen+' до '+this.maxTitleLen + ' символов',
					required: value => !!value || 'Это необходимое поле'
				},
        		minTitleLen: 3,
        		maxTitleLen: 100,
        		modes:[],
			}
		},
		methods: {
			getUploadedImage(e){
				this.image = e
			},
			reloadPage() {
				window.location.reload(true)
			},
			getModes(){
				Axios.get(`${TestingSystemAPI}/api/strict_modes/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.modes = data
		          this.successLoad = true
		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось получить список режимов. Проверьте подключение к сети.'
		        })
			},
			addMode(){
				/*
				if (!this.$refs.addMform.validate())
	        	{
               		this.successLoad = false
                    this.alert = true
                    this.alert_message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	*/
	        	/*
	        	if (this.successLoad)
	        	{
	        		alert('!')
	        		return
	        	}
	        	*/

	        	this.isSubmitting = true
                let formData = new FormData()
                formData.set('name', this.title)
                formData.set('image', this.image)

                Axios.post(`${TestingSystemAPI}/api/strict_modes/`, formData, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        })
               .then(({response}) => {
                    this.reloadPage()

                })
               .catch(error => {
               		this.successLoad = false
                    this.alert = true
	        		this.isSubmitting = false
                    this.alert_message = 'Не удалось добавить режим. Проверьте подключение к сети.'
                })
			},
			deleteMode(id){
				Axios.delete(TestingSystemAPI+'/api/strict_modes/'+id+'/', {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        })
               .then(response => {
                    this.reloadPage()
                })
               .catch(error => {
               		this.successLoad = false
                    this.alert = true
                    this.alert_message = 'Не удалось удалить режим. Проверьте подключение к сети.'
                })
			},
			hideAlert() {
				this.alert = false
			},
			startTimer() {
				setTimeout(this.hideAlert, 4000)
			}
		},
		mounted(){
			this.getModes()
		},
		watch: {
			alert: function(val) {
				if (val)
					this.startTimer()
			}
		}
	}
</script>

<style>
	.content-wrapper{
		overflow-y: auto;
		border-radius: 4px;
		border: 1px solid #919191;
		height: 350px;
		margin-bottom: 10px;
		background: #EBEBEB;
		padding: 15px;
	}
</style>