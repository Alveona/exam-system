<template>	
	<div>
		<v-btn round color="success" @click.native="changePage('/questions/add')" dark>
			<v-icon size="32px">
				add
			</v-icon>
		 Добавить новый вопрос</v-btn>
		<added-question
		v-for="question in questions"
			:title="question.title"
			:text="question.text"
			:type="question.answer_type"
		></added-question>
    <v-snackbar :timeout="timeout"
                bottom="bottom"
                color="red lighten-1"
                v-model="snackbar">
      {{ message }}
    </v-snackbar>
	</div>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
  	import AddedQuestion from '@/components/boxes/AddedQuestion'
	import Authentication from '@/components/pages/Authentication'

	const TestingSystemAPI = 'http://10.0.1.5:8000'
	export default{
		data() {
			return {
				questions: [],
				snackbar: false,
				message: '',
				timeout: 0
			}
		},
		methods: {
			getAddedQuestions() {
				Axios.get(`${TestingSystemAPI}/api/questions/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.questions = this.dataParser(data, 'id', 'title', 'text', 'answer_type')
		        }).catch(error => {
		          this.snackbar = true
		          this.message = 'Не удалось получить список вопросов'

		          console.log(error)
		        })
			},

		      dataParser (targetedArray, ...options) {
		        let parsedData = []
		        targetedArray.forEach(item => {
		          let parsedItem = {}
		          options.forEach(option => (parsedItem[option] = item[option]))
		          parsedData.push(parsedItem)
		        })
		        return parsedData
		      },
			changePage(link){
				router.push(link)
			}
		},
	    mounted () {
	      this.getAddedQuestions()
	    },
	}
</script>

<style>
	
</style>