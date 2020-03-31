<template>
	<v-form ref="addUform">
		<v-layout row wrap>
			<v-flex xs12 class="mb-3">
				<h4 class="display-1">Настройки профиля</h4>
			</v-flex>

			<v-flex xs12 sm6 class="px-2">
				<v-label>Имя</v-label>
	            <v-text-field
	              required
          		  :rules="[rules.required, rules.FirstName]"
          		  v-model="userdata.name"
          		  solo
	            ></v-text-field>
	        </v-flex>

	        <v-flex xs12 sm6 class="px-2">
				<v-label>Фамилия</v-label>
	            <v-text-field
	              required
          		  :rules="[rules.required, rules.SurName]"
          		  v-model="userdata.surname"
          		  solo
	            ></v-text-field>
	        </v-flex>

	        <v-flex xs12 sm6 class="px-2">
				<v-label>Место учебы\работы</v-label>
	            <v-text-field
	              required
          		  :rules="[rules.required, rules.Activity]"
          		  v-model="userdata.activity"
          		  solo
	            ></v-text-field>
	        </v-flex>

	        <v-flex xs12 sm6 class="px-2">
				<v-label>Телефон</v-label>
	            <v-text-field
	              required
          		  :mask="mask"
          		  v-model="userdata.phone"
          		  solo
	            ></v-text-field>
	        </v-flex>
	        <!--
        	<v-flex xs12 sm5 class="ml-3">
	        	<v-label>Аватар профиля</v-label>
	            <file-input 
	            class="fileBtn"
                accept="image/*"
                ref="fileInput"
                @input="getUploadedImage"
	            :label="imageLoadText"
	            ></file-input>
		    </v-flex>
			-->
		    <v-flex xs12>
				<v-btn round color="success" @click.native="onSubmit()" dark large>
					 Сохранить изменения
				</v-btn>
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
</template>

<script>
    import Axios from 'axios'
    import FileInput from '@/components/other/FileLoader'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'	

	const TestingSystemAPI = connection.server
	
	export default {
		components: { FileInput },
		data(){
			return {
				userdata:[],
				successLoad: false,
				alert: false,
				alert_message: false,
				image: null,
				showImageTooltip:false,
				minNameLen:2,
				maxNameLen:40,
				minSurnameLen:2,
				maxSurnameLen:50,
				minActivityLen:3,
				maxActivityLen:70,
				minPhoneLen:10,
				maxPhoneLen:15,
				minGroupLen:2,
				maxGroupLen:20,
				mask: 'phone',
				rules: {
					FirstName: val => (val.length >= this.minNameLen && val.length <= this.maxNameLen) || 'Длина названия должна быть в диапазоне от '+this.minNameLen+' до '+this.maxNameLen + ' символов',
					SurName: val => (val.length >= this.minSurnameLen && val.length <= this.maxSurnameLen) || 'Длина названия должна быть в диапазоне от '+this.minSurnameLen+' до '+this.maxSurnameLen + ' символов',
					Activity: val => (val.length >= this.minActivityLen && val.length <= this.maxActivityLen) || 'Длина названия должна быть в диапазоне от '+this.minActivityLen+' до '+this.maxActivityLen + ' символов',
					required: value => !!value || 'Это необходимое поле',
				}
			}
		},
		methods:
		{
			getUserData(){
				Axios.get(`${TestingSystemAPI}/my`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.userdata = data
		          this.successLoad = true
		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось получить список режимов. Проверьте подключение к сети.'
		        })
			},
			onSubmit() {
				if (!this.$refs.addUform.validate())
	        	{
               		this.successLoad = false
                    this.alert = true
                    this.message = 'Не все обязательные поля были заполнены.'
	        		return
	        	}
	        	if (this.successLoad)
	        		return
                let formData = new FormData()

                formData.set('name', this.userdata.name)
                formData.set('surname', this.userdata.surname)
                formData.set('activity', this.userdata.activity)
                formData.set('phone', this.userdata.phone)
                formData.set('group', this.userdata.group)
                formData.set('image', this.image)

                console.log(formData)

                Axios.put(`${TestingSystemAPI}/profile/${userdata.id}/`, formData, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: {}
		        })
               .then((response) => {
               		this.successLoad = true
                    this.alert = true
                    this.alert_message = 'Изменения успешно сохранены!'
                    setTimeout(this.goBack, 1200)
                })
               .catch((error) => {
               		this.successLoad = false
                    this.alert = true
                    this.alert_message = 'Не удалось сохранить изменения. Проверьте подключение к сети.'
                })
			},
			getUploadedImage(e){
				this.image = e
			},
			goBack(){
            	router.push('/')
			}
		},
		mounted() {
			this.getUserData()
		}
	}
</script>

<style>
	
</style>