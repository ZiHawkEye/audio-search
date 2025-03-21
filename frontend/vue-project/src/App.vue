<template>
  <div class="container">
    <div class="component">
      <audio-preview />
    </div>
    <div class="component">
      <search-bar />
    </div>
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
    mounted() {},
    methods: {},
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
    max-width: 1600px;
    margin: auto;
    justify-content: center;
    align-items: center;
    height: 100vh;
    display: flex;
  }

  .container {
    display: flex;
    justify-content: space-between;
    width: 80%;
  }

  .component {
    flex: 1;
    margin: 10px;
    padding: 20px;
    max-height: 500px;
    width: 500px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    overflow: auto;
  }
</style>
