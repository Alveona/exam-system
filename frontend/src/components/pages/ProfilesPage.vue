<template>
	<v-layout>
		<v-layout row wrap>
			<v-flex xs12>
				<v-label>Всего отмечено: {{usersChecks.length}}</v-label>
				<added-user
				:collection="users"
				:withchecks="1"
				:usersChecks="usersChecks"
				@update:usersChecks="subscribe($event)"
				@update:group="changeGroup($event)"
				@update:collection="toggleShow($event)"
				></added-user>
				<v-label v-if="error">Не удалось получить список профилей. Проверьте подключение к сети.</v-label>
			</v-flex>
		</v-layout>
	</v-layout>
</template>

<script>
    import Axios from 'axios'
    import FileInput from '@/components/other/FileLoader'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'
    import AddedUser from '@/components/boxes/AddedUser'

	const TestingSystemAPI = connection.server
	
	export default {
		components: { AddedUser },
		data(){
			return {
				users: [],
				successLoad: false,
				alert: false,
				error: false,
				alert_message: '',
			    usersChecks: [],
			}
		},
		methods:
		{
			async getProfiles() {
				await Axios.get(`${TestingSystemAPI}/profiles/`, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.users = data
		          this.users.reverse()
		          for (var i = 0; i < this.users.length; ++i)
		          {
		          	this.users[i].show = false
		          	if (this.users[i].subscribed)
		          	  this.usersChecks.push(this.users[i].id)
		          }
		        }).catch(error => {
		        	this.error = true
		          console.log(error)
		        })
			},
			toggleShow(id) {
				for (var i = 0; i < this.users.length; ++i)
					if (this.users[i].id == id)
					{
						this.users[i].show = !this.users[i].show
						this.users.push(null)
						this.users.pop()
						return
					}
			},
			async subscribe(pkg){
				await Axios.post(`${TestingSystemAPI}/subscribe`, {'subscription' : pkg.id}, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {

					this.usersChecks = pkg.checks
		        }).catch(error => {
		        	this.error = true
		          console.log(error)
		        })
			},
			async changeGroup(pkg){
				await Axios.post(`${TestingSystemAPI}/promote`, {'user' : pkg.id}, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		        	this.users[pkg.idx].group = data.group
		        }).catch(error => {
		        	this.error = true
		          console.log(error)
		        })
			}
		},
		mounted() {
			this.getProfiles()
		}
	}
</script>

<style>
	
</style>