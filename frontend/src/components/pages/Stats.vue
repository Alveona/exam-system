<template>
	<v-layout>
		<stats-box v-for="a in length"
		:answers="arr[a]"></stats-box>
	</v-layout>
</template>

<script>
	import StatsBox from '@/components/boxes/statsbox'
	export default {
		components: { StatsBox },
		data() {
			return {
				arr: [],
				length: 3
			}
		}
	}
</script>