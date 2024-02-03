<template>
  <div id="app">
    <h1>Consultar secciones</h1>
    <button v-on:click="fetchData">Consulta</button>
    <div class="grid" v-if="secciones">
      <div class="grid-item" v-for="seccion in secciones" :key="seccion.id">
        {{ seccion.name }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      secciones: null,
    };
  },
  methods: {
    fetchData() {
      fetch("http://127.0.0.1:8000/sections")
        .then((response) => response.json())
        .then((data) => {
          this.secciones = data.sections;
          console.log(data);
        });
    },
  },
};
</script>

<style>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 10px;
}

.grid-item {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}
</style>
