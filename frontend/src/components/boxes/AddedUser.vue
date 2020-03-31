<template>
	<v-layout row wrap>
		<v-flex xs12>
		  <v-layout row wrap v-for="user in collection">
		    <v-flex xs12>
		        <v-card class="userItem">  
		          <v-card-title primary-title>
		          	<v-flex xs1 v-if="withchecks">
		          		<v-checkbox v-model="usersChecks" :value="user.id" @change="emitChecks(usersChecks, user.id)" hide-details class="mt-0 mb-2 shrink mr-2"></v-checkbox>
		            </v-flex>
			          <v-flex v-if="withchecks ? 'xs11' : 'xs12'">
			            <span class="title">{{!!user.surname ? user.surname : '-'}} {{!!user.name ? user.name : '-'}} ({{user.group != 'admin' ? user.group == 'teacher' ? 'Преподаватель' : 'Студент' : 'Администратор'}})</span>
			          </v-flex>
					  <v-spacer></v-spacer>
					  	<v-btn v-if="user.group == 'student'" color="primary" @click.native="emitGroup(user.id, collection.indexOf(user))" dark>Сделать преподавателем</v-btn>
				    	<v-btn v-if="user.group == 'teacher'" color="success" @click.native="emitGroup(user.id, collection.indexOf(user))" dark>Сделать студентом</v-btn>
					  <v-tooltip bottom>
			            <v-btn slot="activator" icon @click="$emit('update:collection', user.id)">
			              <v-icon>{{ user.show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
			            </v-btn>
		              	<span>{{ user.show ? 'Скрыть подробности' : 'Показать подробности'}}</span>
			          </v-tooltip>
		          </v-card-title>
		  

		          <v-slide-y-transition>
		            <v-card-text v-show="user.show">
		              <p class="wrappedText">
		            	  Login: {{user.user.username}}
			          </p>
		              <p class="wrappedText">
			              Учреждение: {{!!user.activity ? user.activity : '-'}}
			          </p>
		              <p class="wrappedText">
			              Должность: {{!!user.group ? user.group : '-'}}
			          </p>
		              <p class="wrappedText">
			              Телефон: {{!!user.phone ? user.phone : '-'}}
			          </p>
		            </v-card-text>
		          </v-slide-y-transition>


		        </v-card>
		    </v-flex>
		  </v-layout>
		</v-flex>
    </v-layout>
</template>

<script>
  	import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		props: ['withchecks', 'usersChecks', 'collection'],
		data() {
			return {
				alert: false,
				alert_message: '',
				snackbar: false,
				snackbar_message: '',
				successDelete: false
			}
		},
		methods: {
			reloadPage() {
				window.location.reload(true)
			},
			emitChecks(checks, id){
				this.$emit('update:usersChecks', {'checks' : checks, 'id' : id})
			},
			emitGroup(id, idx){
				this.$emit('update:group', {'id' : id, 'idx' : idx })
			}
		}
	}
</script>

<style>
	.userItem{
		margin-top: 10px
	}
	.wrappedText{
		word-wrap:break-word;
	}
</style>