<template>
  <select :value="modelValue" @change="changeOption" class="form-select">
    <option disabled value="">Выберите из списка</option>
    <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
    >
      {{ option.name }}
    </option>
  </select>
</template>

<script>
export default {
  name: 'cake-select',
  props: {
    modelValue: {
      type: [String, Number]
    },
    options: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    changeOption(event) {
      this.$emit('update:modelValue', event.target.value);
    }
  }
}
</script>

<style scoped>
.form-select {
  border-radius: 10px;
  color: #444251;
}

.form-select:focus {
  border-color: #454351;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(53, 53, 86, 0.25);
}
</style>