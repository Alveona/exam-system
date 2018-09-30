<template>
    <div>
        <div>
            <img
                    v-if="accept=='image/*'"
                    :src="fileUrl"
                    ref="fileUrl"
                    height="150"
                    @click="onPickFile"
                    style="cursor: pointer;"
            >
        </div>
        <div>
            <v-btn raised 
                    :disabled="dis" @click="onPickFile" v-if="!fileUrl">
                {{ selectLabel }}
            </v-btn>
            <v-btn raised 
                    :disabled="dis" class="error" @click="removeFile" v-else>
                {{ removeLabel }}
            </v-btn>
            <input
                    type="file"
                    ref="file"
                    name="file"
                    :accept="accept"
                    @change="onFilePicked"
                    :disabled="dis"
            >
        </div>
            <v-label v-if="!fileUrl">{{label}}</v-label>
            <v-label v-if="(fileUrl) && (accept=='audio/*')">{{filename}}</v-label>
    </div>
</template>

<script>
    export default {
        props: {
            value: {
                type: String
            },
            accept: {
                type: String,
                default: '*'
            },
            selectLabel: {
                type: String,
                default: 'Выберите файл'
            },
            removeLabel: {
                type: String,
                default: 'Удалить'
            },
            dis: {
                type: Boolean
            },
            label: {
                type: String
            }
        },

        data() {
            return {
                fileUrl: '',
                filename: ''
            }
        },

        watch: {
            value(v) {
                this.fileUrl = v
            }
        },

        mounted() {
            this.fileUrl = this.value
        },

        methods: {
            onPickFile() {
                this.$refs.file.click()
            },

            onFilePicked(event) {
                const files = event.target.files || event.dataTransfer.files

                if (files && files[0]) {
                    this.filename = files[0].name

                    if (this.filename && this.filename.lastIndexOf('.') <= 0) {
                        return alert('add valid file!')
                    }

                    const fileReader = new FileReader()
                    fileReader.addEventListener('load', () => {
                        this.fileUrl = fileReader.result
                    })
                    fileReader.readAsDataURL(files[0])

                    this.$emit('input', files[0])
                }
            },

            removeFile() {
                this.fileUrl = ''
            }
        }
    }
</script>

<style scoped>
    input[type=file] {
        position: absolute;
        left: -99999px;
    }
</style>