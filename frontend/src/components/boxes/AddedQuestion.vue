<template>
	<v-layout row>
      <v-flex xs12>
        <v-card class="questionItem">  
          <v-card-title primary-title>
            <div>
              <div class="headline">{{title}}
				<span v-if="type==1">(ввод значения)</span>
				<span v-else-if="type==2">(выбор одного правильного)</span>
				<span v-else-if="type==3">(выбор нескольких правильных)</span>
              </div>
            </div>
          </v-card-title>
  
          <v-card-actions>
            <v-btn icon @click="show = !show">
              <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
            </v-btn>
            <v-btn flat><v-icon>edit</v-icon></v-btn>
            <v-btn flat><v-icon>delete</v-icon></v-btn>
          </v-card-actions>
  
          <v-slide-y-transition>
            <v-card-text v-show="show">
              {{text}}
            </v-card-text>
          </v-slide-y-transition>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
	export default {
		props: ['title', 'text', 'type'],
		data() {
			return {
				show: false
			}
		}
	}
</script>

<style>
	.questionItem{
		margin-top: 10px
	}
</style>