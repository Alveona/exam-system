<template>
	<v-layout row wrap>
      <v-flex xs12>
        <v-card class="testItem px-2 py-2">  
        	<v-layout row wrap>
	        	<v-flex xs12 sm4>
		        	<v-img
		        	class="mb-2"
		        	:aspect-ratio="16/9" 
		            :src="path"
		            position="center center"
		          >
		          </v-img>
		      </v-flex>

				<v-flex xs12 sm8>
		          <v-card-title primary-title>
		            <div>
		              <div class="headline">{{title}}
		              </div>
		              <div>Автор: {{author}}</div>
		            </div>
		          </v-card-title>
		      </v-flex>

			</v-layout>
				<v-divider light></v-divider>

				<v-flex xs12>
		          <v-card-actions>
		            <v-btn icon @click="show = !show">
		              <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
		            </v-btn>
		            <v-btn icon><v-icon>edit</v-icon></v-btn>
		            <v-btn icon><v-icon>delete</v-icon></v-btn>
		          </v-card-actions>
		      </v-flex>

				<v-flex xs12 >
		          <v-slide-y-transition>
		            <v-card-text v-show="show">
		              {{description}}
		            </v-card-text>
		          </v-slide-y-transition>
		      </v-flex>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
	import connection from '@/router/connection'

	const TestingSystemAPI = connection.server

	export default {
		props: ['title', 'id', 'author', 'image', 'description'],
		data() {
			return {
				show: false
			}
		},
		computed: {
			path: function() {
				//return TestingSystemAPI + '/' + this.image
				return this.image
			}
		}
	}
</script>

<style>
	.testItem{
		margin-top: 10px
	}
</style>