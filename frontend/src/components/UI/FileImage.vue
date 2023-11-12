<template>
  <img :src="loadFile" alt="image"/>
</template>

<script>
export default {
  name: 'file-image',

  props: ['src'],
  data: () => ({path: ""}),
  computed: {
    loadFile() {
      const reader = new FileReader();
      reader.readAsDataURL(this.src);
      reader.onload = event => this.path = event.target.result;
      return this.path;
    }
  }
}
</script>
