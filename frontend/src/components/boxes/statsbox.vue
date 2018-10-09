<template>
	<v-layout row wrap>
		<v-layout row wrap v-for="answer in answers">
			<v-flex xs6>
	            <v-text-field
	              label="1"
	              v-model="answer.title"
	              required
	      		  clearable
	      		  box
	            ></v-text-field>
	        </v-flex>
	        <v-flex xs6>
	            <v-text-field
	              label="2"
	              v-model="answer.text"
	              required
	      		  clearable
	      		  box
	            ></v-text-field>
	        </v-flex>
	    </v-layout >
	    <v-flex xs12>
	            <v-text-field
	              label="2"
	              type="number"
	              v-model="count"
	              required
	      		  clearable
	      		  box
	            ></v-text-field>
	            <v-btn @click.native="setSize()">tye</v-btn>
	        </v-flex>
	</v-layout>
</template>

<script>
	export default {
		props: ['answers', 'count'],
		data() {
			return 	{
			}
		},
		methods: {
			setSize() {
				this.answers.splice(0)
				for (var i = 0; i < this.count; ++i)
					this.answers.push({
						title:'', 
						text:''
					})
			}
		},
		mounted() {
			this.setSize()
		}
	}
</script>