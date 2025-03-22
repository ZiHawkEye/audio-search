// Reference: https://blog.logrocket.com/create-search-bar-vue/
<template>
  <input
    id="search-bar"
    type="text"
    v-model="input"
    placeholder="Search transcriptions..."
  />
  <button @click="showAllTranscriptions">Show All Transcriptions</button>
  <div
    class="item transcription"
    v-for="transcription in transcriptions"
    :key="transcription.id"
  >
    <p>{{ transcription.title }}</p>
    <p>{{ transcription.content }}</p>
    <button @click="deleteTranscription(transcription.id)">Delete</button>
  </div>
  <div class="item error" v-if="input && !transcriptions.length">
    <p>No results found!</p>
  </div>
</template>

// Note: Uses script setup instead of script
<script setup>
  import { ref, watch } from 'vue'
  import axios from 'axios'

  // Define reactive state
  const transcriptions = ref([])
  const input = ref('')

  // Filters for transcriptions by their content
  const getTranscriptions = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/search?title=${input.value}`
      )
      console.log(response.data.transcriptions)
      transcriptions.value = response.data.transcriptions // Update transcriptions with the results
    } catch (error) {
      console.error('Error fetching data:', error)
      transcriptions.value = []
    }
  }

  // Show all transcriptions when button is clicked
  const showAllTranscriptions = () => {
    input.value = ''
    getTranscriptions()
  }

  // Watch for changes in the input value
  watch(input, (newValue) => {
    getTranscriptions()
  })

  // Call getTranscriptions() on component mount to fetch initial data
  getTranscriptions()

  const deleteTranscription = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/delete?id=${id}`)
      transcriptions.value = transcriptions.value.filter((t) => t.id !== id)
    } catch (error) {
      console.error('Error deleting transcription:', error)
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');

  * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-family: 'Montserrat', sans-serif;
  }

  body {
    padding: 20px;
    min-height: 100vh;
    background-color: rgb(234, 242, 255);
  }

  input {
    display: block;
    width: 350px;
    margin: 20px auto;
    padding: 10px 45px;
    background: white url('assets/search-icon.svg') no-repeat 15px center;
    background-size: 15px 15px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    box-shadow:
      rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
      rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  }

  .item {
    width: 350px;
    margin: 0 auto 10px auto;
    padding: 10px 20px;
    color: white;
    border-radius: 5px;
    box-shadow:
      rgba(0, 0, 0, 0.1) 0px 1px 3px 0px,
      rgba(0, 0, 0, 0.06) 0px 1px 2px 0px;
  }

  .transcription {
    cursor: pointer;
  }

  .error {
    background-color: tomato;
  }
</style>
