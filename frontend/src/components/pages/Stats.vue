<template>
	<v-layout>
		<stats-box
		:answers="arr"></stats-box>
		<v-btn @click.native="inc()"></v-btn>
		<p v-for="a in arr">{{a.title}}</p>
	</v-layout>
</template>

<script>
	import StatsBox from '@/components/boxes/statsbox'
	export default {
		components: { StatsBox },
		data() {
			return {
				arr: [],
				count: 5,
				loc: 3
			}
		},
		methods: {
			inc() {
				this.loc = 2
			}
		},
		watch: {
			loc: function() {
				this.count++
			}
		}
	}
</script>