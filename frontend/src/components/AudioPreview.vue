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

      <div
        class="upload-status"
        v-if="uploadProgress > 0 && uploadProgress <= 100"
      >
        Uploading {{ uploadProgress }}%... please be patient
        <div class="progress-bar">
          <div class="progress" :style="{ width: uploadProgress + '%' }"></div>
        </div>
      </div>

      <button v-if="files.length > 0 && !isUploading" v-on:click="submitFile()">
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
        uploadProgress: 0,
        isUploading: false,
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
        this.isUploading = true
        this.uploadProgress = 0

        let formData = new FormData()

        for (var i = 0; i < this.files.length; i++) {
          formData.append('audio', this.files[i])
          formData.append('filename', this.files[i].name)
        }

        // alert('Transcribing audio, please be patient...')

        axios
          .post('http://127.0.0.1:5000/transcribe', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
              this.uploadProgress = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              )
              console.log('Upload progress: ' + this.uploadProgress)
            },
          })
          .then(() => {
            console.log('Upload succeeded')
            this.files = []
            this.filePreviewUrls = []
            this.isUploading = false
            this.uploadProgress = 0
            alert(
              'Upload succeeded, please check the results by pressing "Show All Transcriptions" '
            )
          })
          .catch((error) => {
            console.error('Upload failed:', error)
            this.isUploading = false
            alert('Upload failed! Please try again.')
          })
      },
    },
  }
</script>

<style scoped>
  .upload-status {
    margin: 15px 0;
  }

  .progress-bar {
    height: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
    margin-top: 5px;
    overflow: hidden;
  }

  .progress {
    height: 100%;
    background-color: #1890ff;
    transition: width 0.3s ease;
  }
</style>
