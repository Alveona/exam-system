<template>	
	<div>
		<p>Zalupa</p>
		<p>{{text}}</p>
		<v-btn @click.native="getAddedTests">
			<v-icon>
				search
			</v-icon>
		</v-btn>
	</div>
</template>

<script>
  import Axios from 'axios'

	export default{
		data() {
			return {
				tests: [],
				text: 'some text'
			}
		},
		methods: {
			getAddedTests() {
				this.text = 'another text'
				/*
				Axios.get(`${BudgetManagerAPI}/api/v1/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: { user_id: this.$cookie.get('user_id') }
		        }).then(({data}) => {
		          this.courses = this.dataParser(data, 'id', '')
		        }).catch(error => {
		          this.errorHandler(error)
		        })
		        */
			}
		}
	}
</script>

<style>
	
</style>