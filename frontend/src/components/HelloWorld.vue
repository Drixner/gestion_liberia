<template>
  <div>
    <h1>{{ msg }}</h1>
    <h2>Secciones</h2>
    <div class="grid" v-if="secciones">
      <div class="grid-item" v-for="seccion in secciones" :key="seccion.id">
        {{ seccion.nombre }}
      </div>
    </div>
    <!-- Resto de tu interfaz -->
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data() {
    return {
      secciones: null,
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/articulos")
      .then((response) => {
        this.secciones = response.data.sections;
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
