<template>
	<v-layout row wrap>
		<stats-box ></stats-box>
		<vue-audio :file="audio"/>
	</v-layout>
</template>

<script>
	import VueAudio from 'vue-audio'
	import StatsBox from '@/components/boxes/statsbox'
	export default {
		components: { StatsBox, VueAudio },
		data() {
			return {
				audio: 'https://vk.com/mp3/audio_api_unavailable.mp3?extra=zvPOBZvIzxnImem6se9LyxDADKmOovDTBeLdyJrpzKHIDJGVy25Wr1HLDNKWl25wnJqXBxz1ztyWCKiVsdqUDwfJCZfVpvPJnvbWtKzZAv03nN02xOnRDffHlKr1mKXbzdrLuMvTCdbWqZLLn3LZmdjbzhPJmxfqCLjSzZ9emL9LzhbsDgWZzw9euvPurODAnujlx2n4DfPJrI9LB1PhAgnMAfvNtLHvuuWTtxmOCfaYA3n1vMDOBY54m25VvwjAn1HcA1f2qJn5me41Ce82ywThEtzsrLy#AqS2nZK'
			}
		},
		methods: {
		},
		mounted() {
		}
	}
</script>