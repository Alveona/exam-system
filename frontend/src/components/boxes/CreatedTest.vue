<template>
	<v-layout row wrap>
      <v-flex xs12>
        <v-card class="testItem px-2 py-2" >  
        	<router-link tag="div" :to="{ name: 'testpage', params: { token: token }}">
	        	<v-layout row wrap class="pointerBlock">
		        	<v-flex xs12 sm4>
			        	<v-img
			        	class="mb-2"
			        	:aspect-ratio="16/9" 
			            :src="image"
			            position="center center"
			          >
			          </v-img>
			      </v-flex>

					<v-flex xs12 sm8>
			          <v-card-title primary-title>
			            <div>
			              <div class="headline">{{title}}</div>
			              <div v-if="added">Автор: {{author}}</div>
			            </div>
			          </v-card-title>
			      </v-flex>

				</v-layout>
			</router-link>
				<v-divider light></v-divider>

				<v-flex xs12>
		          <v-card-actions>
				  <v-tooltip bottom>
		            <v-btn slot="activator" icon @click="show = !show">
		              <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
		            </v-btn>
		            <span>{{show ? 'Скрыть описание' : 'Показать описание'}}</span>
		          </v-tooltip>

		          <!--<v-tooltip bottom>
		            <v-btn slot="activator" v-if="!added" :to="{ name: 'edittest', params: { token: token }}" icon><v-icon>edit</v-icon></v-btn>
		            <span>Редактировать тест</span>
		          </v-tooltip>-->

				  <v-tooltip bottom>
		            <v-btn slot="activator" v-if="!added" @click.native="deleteTest(token)" icon><v-icon>delete</v-icon></v-btn>
		            <span>Удалить тест</span>
		          </v-tooltip>
		          <v-tooltip bottom>
		            <v-btn slot="activator" v-if="!added" @click.native="dialog = true" icon><v-icon>share</v-icon></v-btn>
		            <v-dialog
			          v-model="dialog"
			          max-width="500px"
			        >
			          <v-card>
			            <v-card-title>
			            	<p class="title">
				              {{title}}
				          </p>
			            </v-card-title>
			            <v-card-text>
			            	<v-layout row wrap>
			            	<v-flex xs11>
			              <v-text-field
			                  v-model="test_token"
				              label="Ссылка на тест"
				              readonly
				            ></v-text-field>
				        </v-flex>
			            	<v-flex xs1 pt-2>
			            <v-tooltip bottom>
				            <v-btn slot="activator" v-if="!added" @click.native="copy()" icon><v-icon>link</v-icon></v-btn>
				            <span>Скопировать ссылку</span>
				          </v-tooltip>
				      </v-flex>
				  </v-layout>
			            </v-card-text>
			            <v-card-actions>
			              <v-switch
			                v-model="demo_allowed"
			                @click.native="change_demo_access()"
					        label="Разрешить демо-режим"
					      ></v-switch>
			              <v-spacer>
			              </v-spacer>
			              <v-btn
			                color="primary"
			                text
			                @click="dialog = false"
			              >
			                Ок
			              </v-btn>
			            </v-card-actions>
			          </v-card>
			        </v-dialog>
		            <span>Поделиться тестом</span>
		          </v-tooltip>
		        </v-card-actions>
		      </v-flex>

				<v-flex xs12>
					<v-alert
			          :value="alert"
			          :type="successDelete ? 'success' : 'error'"
			        >
			        {{message}}

				      	<v-tooltip v-if="!successDelete" top>
					        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
					        <span>Обновить</span>
					    </v-tooltip>
				    </v-alert>
		        </v-flex>	

				<v-flex xs12 >
		          <v-slide-y-transition>
		            <v-card-text v-show="show">
		              {{description}}
		            </v-card-text>
		          </v-slide-y-transition>
		      </v-flex>
		      <v-snackbar
			        v-model="snackbar"
			        :color="successDelete ? 'green lighten-1' : 'red lighten-1'"
			      >
			        {{message}}

		      	<v-tooltip v-if="!successDelete" top>
			        <v-btn  @click.native="reloadPage()" slot="activator" icon dark> <v-icon>autorenew</v-icon></v-btn>
			        <span>Обновить</span>
			    </v-tooltip>
		      </v-snackbar>
        </v-card>
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
		props: ['title', 'dialog', 'token', 'author', 'image', 'description', 'added', 'demo_allowed', 'element', 'collection'],
		data() {
			return {
				show: false,
				successDelete: false,
				alert: false,
				snackbar: false,
				message: '',
				frontAddress: connection.front
			}
		},
		computed: {
			test_token: function(){
				return this.frontAddress + '/tests/' + this.token
			}
		},
		methods: {
			async deleteTest(token) {
				await Axios.delete(TestingSystemAPI+'/courses/'+token+'/', {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		          this.collection.splice(this.element, 1)
		          this.alert = true
		          this.successDelete = true
		          this.message = 'Тест успешно удален.'
		        }).catch(error => {
		          this.alert = true
		          this.successDelete = false
		          this.message = 'Не удалось удалить тест. Проверьте подключение к сети.'
		        })
		    },
		    async change_demo_access() {
				await Axios.post(TestingSystemAPI+'/course_demo_allow', {'course' : this.token}, {
		          headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		          params: {}
		        }).then(({data}) => {
		        }).catch(error => {
		          this.alert = true
		          this.successDelete = false
		          this.message = 'Не удалось изменить доступ к демо-режиму. Проверьте подключение к сети.'
		        })
		    },
		    copy(){
			  let tmp   = document.createElement('INPUT'), 
			      focus = document.activeElement

			  tmp.value = this.test_token

			  document.body.appendChild(tmp)
			  tmp.select()
			  document.execCommand('copy')
			  document.body.removeChild(tmp)
			  focus.focus()
			},
			reloadPage() {
				window.location.reload(true)
			},
			openDialog() {

			}
		}
	}
</script>

<style>
	.testItem{
		margin-top: 10px
	}
	.pointerBlock{
		cursor:pointer;
	}
</style>