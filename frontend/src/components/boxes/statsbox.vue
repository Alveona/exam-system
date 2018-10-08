<template>
	<v-layout>
		<v-flex xs12>
            <v-text-field
              label="Краткое название (будет видно только вам)"
              v-model="answers.title"
              required
      		  clearable
      		  :rules="rules"
      		  box
            ></v-text-field>
        </v-flex>
	</v-layout>
</template>

<script>
	export default {
		props: ['answers'],
		data() {

		}
	}
</script>