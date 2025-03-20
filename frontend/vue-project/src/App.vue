<template>
  <div>
    <audio-preview />
    <search-bar />
  </div>
</template>

<script>
  import AudioPreview from './components/AudioPreview.vue'
  import SearchBar from './components/SearchBar.vue'
  import axios from 'axios'

  export default {
    name: 'App',
    components: {
      AudioPreview,
      SearchBar,
    },
    data() {
      return {
        items: [],
      }
    },
    mounted() {
      axios
        .get('http://127.0.0.1:5000/transcriptions')
        .then((response) => {
          console.log(response.data)
          this.items = response.data
        })
        .catch((error) => {
          console.error('Error fetching data:', error)
        })
    },
    methods: {
      pretty(value) {
        return JSON.stringify(value, null, 2)
      },
    },
  }
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    max-width: 600px;
    margin: auto;
  }
</style>
