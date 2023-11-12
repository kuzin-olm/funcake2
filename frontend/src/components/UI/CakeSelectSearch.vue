<template>
  <div>
    <VueMultiselect
        v-model="selected"
        :close-on-select="true"
        :searchable="true"
        :options="options"
        :placeholder="placeholder"
        :track-by="trackBy"
        :show-labels="false"
        :allow-empty="allowNull"
        :maxHeight="200"
        :label="trackBy"
        @select="changeUuid"
    />
  </div>
</template>
<script>
import VueMultiselect from 'vue-multiselect'

export default {
  components: {
    VueMultiselect,
  },
  name: 'cake-select-search',
  props: {
    valueUuid: {
      type: Number,
      default: null,
    },
    selectedObj: {
      type: Object,
      default: null,
    },
    options: {
      type: Array,
      default: () => []
    },
    trackBy: {
      type: String,
      default: 'name',
    },
    allowNull: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: 'выберите из списка'
    }
  },
  data() {
    return {
      selected: this.getSelectedByUUID(this.valueUuid)
    }
  },
  emits: ['update:valueUuid', 'update:selectedObj'],
  methods: {
    changeUuid(event) {
      this.$emit('update:valueUuid', event.value)
      this.$emit('update:selectedObj', this.selected)
    },
    getSelectedByUUID(uuid) {
      for (let i = 0; i < this.options.length; i++) {
        if (this.options[i].value === uuid) {
          return this.options[i]
        }
      }
      return null
    },
  },
  watch: {
    valueUuid(newVal, oldVal) {
      this.selected = this.getSelectedByUUID(newVal)
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
<style scoped>
:deep(.multiselect) {
  color: #444251;
  border-radius: 10px;
  font-size: 0.875rem;
}

:deep(.multiselect__placeholder) {
  display: inline-block !important;
  font-size: 1rem;
  padding: 0 0 0 0 !important;
  margin: -2px 0 0 0 !important;
}

:deep(.multiselect--active .multiselect__tags) {
  border-color: #454351;
  box-shadow: 0 0 0 0.25rem rgba(53, 53, 86, 0.25);
}

:deep(.multiselect__tags) {
  border-radius: 10px;
  min-height: 2.4rem;
  padding: 8px 0 0 10px !important;
  border: 1px solid #ced4da;
}

:deep(.multiselect__input) {
  padding: 0 !important;
}

:deep(.multiselect__option--selected) {
  background-color: #444251;
  color: #fff;
}

:deep(.multiselect__option--highlight) {
  background-color: #e2e1e7ff;
  color: #444251;
}


:deep(.multiselect__content-wrapper) {
  border-color: #454351;
  outline: 0;
}
</style>