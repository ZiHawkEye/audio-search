// Reference: https://github.com/canopas/vue-file-upload/tree/main
<template>
  <div class="container">
    <div>
      <label
        >Upload an audio file for transcription
        <input
          type="file"
          accept="audio/*"
          @change="handleFileUpload($event)"
        />
      </label>
      <br />
      <audio id="audio-preview" controls v-show="file != ''" />
      <br />
      <button v-on:click="submitFile()">Submit File</button>
    </div>
  </div>
</template>

// Note: uses script instead of script setup
<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        file: '',
		fileName: '',
      }
    },

    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0]
		if (this.file) {
			this.fileName = this.file.name;
			console.log('Uploaded file name:', this.fileName);
			this.previewAudio();
		}
      },

      previewAudio() {
        let audio = document.getElementById('audio-preview')
        let reader = new FileReader()

        reader.readAsDataURL(this.file)
        reader.addEventListener('load', function () {
          audio.src = reader.result
        })
      },

      submitFile() {
        let formData = new FormData()

        formData.append('audio', this.file)
        formData.append('filename', this.fileName)

        axios
          .post('http://127.0.0.1:5000/transcribe', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(function () {
            console.log('SUCCESS!!')
          })
          .catch(function () {
            console.log('FAILURE!!')
          })
      },
    },
  }
</script>
