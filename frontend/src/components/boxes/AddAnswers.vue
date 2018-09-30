<template>
	<v-layout row wrap v-if="currentType==1">
		<v-flex xs12 sm6>
          <v-text-field
            class="m-2"
            type="text"
            label="Правильный ответ"
            required
  			clearable
          ></v-text-field>
        </v-flex>
		<v-flex xs12 sm6>
          <v-text-field
            class="ml-2"
            type="text"
            label="Комментарий к формату ответа"
            hint="Например, 'Округлить до двух знаков после запятой'"
  			clearable
          ></v-text-field>
        </v-flex>
	</v-layout>
	<v-layout row wrap v-else-if="currentType==2">
		<v-flex xs12>
          <v-text-field
            class="m-2"
            type="number"
            label="Количество ответов, включаемых в тест*"
            required
  			clearable
          ></v-text-field>
        </v-flex>
	</v-layout>
	<v-layout row wrap v-else-if="currentType==3">
		<v-flex xs12>
          <v-text-field
            class="m-2"
            type="number"
            label="Количество ответов, включаемых в тест*"
            required
  			clearable
          ></v-text-field>
        </v-flex>
	</v-layout>
</template>

<script>
	export default {
		props: ['currentType'],
		data() {
			return {

			}
		}
	}
</script>

<style>
	
</style>