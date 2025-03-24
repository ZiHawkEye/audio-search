// Reference:
https://github.com/serversideup/uploading-files-vuejs-axios/tree/main
<template>
  <div class="container">
    <div>
      <label
        >Upload an audio file for transcription
        <input
          type="file"
          multiple
          accept="audio/*"
          @change="handleFileUpload($event)"
        />
      </label>
      <div v-if="files.length > 0" class="file-preview-container">
        <h3>Selected Files:</h3>
        <div v-for="(file, index) in files" :key="index" class="file-preview">
          <div class="file-info">
            <span>{{ file.name }}</span>
            <button @click="removeFile(index)" class="remove-btn">
              Remove
            </button>
          </div>
          <audio
            :src="filePreviewUrls[index]"
            controls
            class="audio-player"
          ></audio>
        </div>
      </div>
      <button v-if="files.length > 0" v-on:click="submitFile()">
        Submit File
      </button>
    </div>
  </div>
</template>

// Note: uses script instead of script setup
<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        files: [],
        filePreviewUrls: [],
      }
    },

    methods: {
      handleFileUpload(event) {
        const selectedFiles = event.target.files

        if (!selectedFiles.length) return

        for (let i = 0; i < selectedFiles.length; i++) {
          this.files.push(selectedFiles[i])
          console.log('Uploaded file name:', selectedFiles[i].name)

          // Create a URL for preview
          const url = URL.createObjectURL(selectedFiles[i])
          this.filePreviewUrls.push(url)
        }
      },

      removeFile(index) {
        // Revoke the URL to prevent memory leaks
        URL.revokeObjectURL(this.filePreviewUrls[index])

        // Remove the file and its preview URL
        this.files.splice(index, 1)
        this.filePreviewUrls.splice(index, 1)
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

        for (var i = 0; i < this.files.length; i++) {
          formData.append('audio', this.files[i])
          formData.append('filename', this.files[i].name)
        }

        alert('Transcribing audio, please be patient...')

        axios
          .post('http://127.0.0.1:5000/transcribe', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then(() => {
            console.log('Upload succeeded')
            this.files = []
            this.filePreviewUrls = []
            alert(
              'Upload succeeded, please check the results by pressing "Show All Transcriptions" '
            )
          })
          .catch((error) => {
            console.error('Upload failed:', error)
            alert('Upload failed! Please try again.')
          })
      },
    },
  }
</script>
