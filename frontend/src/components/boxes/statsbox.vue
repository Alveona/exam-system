<template>
	<v-layout row wrap>
  		<file-input 
            class="fileBtn"
            accept="audio/*"
            ref="fileInput"
            @input="getUploadedAudio"
            :dis="!enabledAudio"
            :checked="enabledAudio"
            :label="audioLoadText"
        ></file-input>
	</v-layout>
</template>

<script>
	import FileLoader from '@/components/other/FileLoader'
	export default {
		components: {FileLoader},
		props: [],
		data() {
			return 	{
			}
		}
	}
</script>