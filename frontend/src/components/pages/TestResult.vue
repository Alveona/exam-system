<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="title text-md-center">Результаты</p>
		</v-flex>

		<v-layout row justify-space-around v-if="response.video">
			<iframe width="720" height="406" :src="response.video" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
		</v-layout>
		<v-layout row justify-space-around v-if="!response.video">
			<v-flex xs12 class="mb-4"> 
				<vue-audio :file="audio" :autoPlay="true"/>
			</v-flex>
		</v-layout>
		<v-flex xs12>
			<v-data-table 
		      :headers="headers"
		      :items="q_items"
		      class="elevation-1"
		    >
		      <template slot="items" slot-scope="props">
		        <td>{{ props.item.order_number }}</td>
		        <td class="text-xs-center">{{ props.item.result }}</td>
		        <td class="text-xs-center">{{ props.item.weight_sum }}</td>
		      </template>
		      <template slot="footer" v-if="mark == 5" >
		        <td colspan="100%" class="light-green accent-4">
		          <strong>Оценка: </strong> 
		          <span >Отлично</span>
		        </td>
		      </template>
		       <template slot="footer" v-else-if="mark == 4" >
		        <td colspan="100%" class="yellow lighten-1">
		          <strong>Оценка: </strong> 
		          <span>Хорошо</span>
		        </td>
		      </template>
		       <template slot="footer" v-else-if="mark == 3">
		        <td colspan="100%"  class="orange lighten-1">
		          <strong>Оценка: </strong> 
		          <span>Удовлетворительно</span>
		        </td>
		      </template>
		       <template slot="footer" v-else >
		        <td colspan="100%" class="red lighten-1">
		          <strong >Оценка: </strong> 
		          <span>Неудовлетворительно</span>
		        </td>
		      </template>
		    </v-data-table>
		</v-flex>

		<v-flex xs12 sm6 offset-sm3 class="px-2">
			<v-btn round color="primary" to="/" dark block large>
				 На главную
			</v-btn>
		</v-flex>
		
		<!--
		<v-flex xs12 sm6 class="px-2">
			<v-btn round color="success" to="/stats" dark block large>
				 Статистика прохождений
			</v-btn>
		</v-flex>		
		-->

	</v-layout>
</template>

<script>
    import Axios from 'axios'
	import router from '@/router'
	import Authentication from '@/components/pages/Authentication'
	import connection from '@/router/connection'
	import VueAudio from 'vue-audio'

	const TestingSystemAPI = connection.server

	export default {
		components: { VueAudio },
		data() {
			return {
		      headers: [
		        {
		          text: 'Вопрос',
		          align: 'left',
		          sortable: false,
		          value: 'number'
		        },
		        { text: 'Набранный балл', value: 'score',
		          align: 'center',
		          sortable: false },
		        { text: 'Максимум', value: 'max',
		          sortable: false, 
		          align: 'center'}
		      ],
		      response: [],
		      q_items: [],
		      mark:0,
		      audio:null
			}
		},
		methods: {
			getResult() {
				Axios.get(`${TestingSystemAPI}/api/stats-session/`, {
		            headers: { 'Authorization': Authentication.getAuthenticationHeader(this) },
		            params: { 'token' : this.$route.params.token }
		        }).then((data) => {
		        	console.log(data)
	                this.response = data.data[0]
	                this.q_items = this.response.session_q
	                if (this.response.video)
	                	this.response.video += '?autoplay=1'
					this.q_items.push({ 'order_number' : "Всего", 'result' : 0, 'weight_sum' : 0})
					this.q_items[this.q_items.length - 1].result = this.getSumScore()
					this.q_items[this.q_items.length - 1].weight_sum = this.getSumMax()
					if (this.getPercent() >= this.response.perfect_mark){
						this.mark = 5
						this.audio = this.response.perfect_audio
					}
					else if (this.getPercent() >= this.response.good_mark){
						this.mark = 4
						this.audio = this.response.good_audio
					}
					else if (this.getPercent() >= this.response.satisfactory_mark){
						this.mark = 3
						this.audio = this.response.satisfactory_audio
					}
					else {
						this.mark = 2
						this.audio = this.response.bad_audio
					}

		        }).catch(error => {

		          console.log(error)
		        })
			},
			getSumScore(){
				var result = 0
				for (var i = 0; i < this.q_items.length - 1; ++i)
					result += this.q_items[i].result
				return result
			},
			getSumMax(){
				var result = 0
				for (var i = 0; i < this.q_items.length - 1; ++i)
					result += this.q_items[i].weight_sum
				return result
			},
			getPercent() {
				return this.getSumScore() / this.getSumMax() * 100
			}
		},
		mounted() {
			this.getResult()
		}
	}
</script>

<style>
</style>