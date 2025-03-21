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
    },
    methods: {
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
	display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
  }
</style>
