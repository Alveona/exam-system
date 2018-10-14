<template>
	<v-layout row wrap>
		<v-flex xs12>
			<p class="title text-md-center">Результаты</p>
		</v-flex>
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
		      <template slot="footer">
		        <td colspan="100%">
		          <strong>Оценка: </strong> 
		          <span v-if="getPercent() >= this.response.perfect_mark">Отлично</span>
		          <span v-else-if="getPercent() >= this.response.good_mark">Хорошо</span>
		          <span v-else-if="getPercent() >= this.response.statisfactory_mark">Удовлетворительно</span>
		          <span v-else>Неудовлетворительно</span>
		        </td>
		      </template>
		    </v-data-table>
		</v-flex>

		<v-flex xs12 sm6 class="px-2">
			<v-btn round color="primary" to="/" dark block large>
				 На главную
			</v-btn>
		</v-flex>

		<v-flex xs12 sm6 class="px-2">
			<v-btn round color="success" to="/stats" dark block large>
				 Статистика прохождений
			</v-btn>
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
		      q_items: []
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
					this.q_items.push({ 'order_number' : "Всего", 'result' : 0, 'weight_sum' : 0})
					this.q_items[this.q_items.length - 1].result = this.getSumScore()
					this.q_items[this.q_items.length - 1].weight_sum = this.getSumMax()
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