<template>
  <input :value="modelValue" @input="updateInput" class="form-control" type="text">
</template>

<script>
export default {
  name: 'cake-input',
  props: {
    modelValue: [String, Number, Array]
  },
  methods: {
    updateInput(event) {
      this.$emit('update:modelValue', event.target.value)
    }
  }
}
</script>

<style scoped>
.form-control {
  border-radius: 10px;
}

.form-control:focus {
  color: #444251;
  background-color: #fff;
  border-color: #454351;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(53, 53, 86, 0.25);
}

</style>