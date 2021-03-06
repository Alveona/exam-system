<template>
	<v-layout row wrap>

		<v-flex xs12>
			<p class="display-1">Управление тестами
			</p>
		</v-flex>

		<div class="divider"></div>
		<h4 class="title pt-2">Созданные тесты</h4>
		<v-tooltip bottom v-model="showTestsTooltip">
	        <v-btn slot="activator" @click="showTestsTooltip = !showTestsTooltip" icon small> <v-icon color="light-blue darken-1">info</v-icon></v-btn>
	        <span>Выбирая режим, пользователь может выбрать вариант восприятия информации от преподавателя. Например, можно привязть к разным режимам разных преподавателей, или одного, но в разных стилях подачи (добрый, ехидный и т.д.) К каждому из режимов можно добавлять свои подсказки к ответам, аудио- и видеозаписи, а также изображение лица преподавателя, которое будет появляться при воспроизведении подсказок. </span>
		</v-tooltip>
		<div class="divider mt-2"></div>

		<v-flex xs12>
			<v-btn round color="success" to="add/test" class="mb-3" dark>
				<v-icon size="24px" class="mr-2">
					add
				</v-icon>
			Создать новый тест</v-btn>
		</v-flex>

		<v-flex xs12>
			<p v-if="successLoad">{{success_message}}</p>
			<created-test
				v-for="test in tests"
				:token="test.token"
				:dialog="test.dialog"
				:title="test.name"
				:description="test.description"
				:image="!!test.image ? test.image : emptyPic"
				:added="0"
				:demo_allowed="test.demo_allowed"
				:element="tests.indexOf(test)"
				:collection="tests"
			></created-test>
		</v-flex>

		 <v-flex xs12>
			<v-alert
	        :value="alert"
	        type="error"
	      >
	        {{alert_message}}

		      	<v-tooltip top>
			        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
			        <span>Обновить</span>
			    </v-tooltip>
		      </v-alert>
	      </v-flex>	

	</v-layout>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
  	import CreatedTest from '@/components/boxes/CreatedTest'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		components: { CreatedTest },
		data() {
			return {
				tests: [],
				alert_message: '',
				alert: false,
				successLoad: false,
				showTestsTooltip:false,
				emptyPic: require('@/assets/images/no_image.png')
			}
		},
		methods: {
			getCreatedTests() {
				Axios.get(`${TestingSystemAPI}/courses-created/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.tests = data

		          this.tests.map(test => test.dialog = false)
		          this.tests.reverse()
		          this.successLoad = true
		        }).catch(error => {
		          this.alert = true
		          this.alert_message = 'Не удалось получить список вопросов. Проверьте подключение к сети.'

		          console.log(error)
		        })
			},
			reloadPage() {
				window.location.reload(true)
			}
		},
		mounted() {
			this.getCreatedTests()
		},
	    computed: {
	    	success_message: function() {
	          if (!this.tests.length)
	          	return 'В вашем профиле нет созданных тестов.'
	          else return 'Добавлено ' + this.tests.length + ' тестов:'
	    	}
	    }
	}
</script>

<style>
	.divider{
		height:1px;
		width:100%;
		background: #bbb;
		margin-bottom:15px;
	}
</style>