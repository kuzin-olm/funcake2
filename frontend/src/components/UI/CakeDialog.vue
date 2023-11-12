<template>
  <div class="modal" v-if="show" @click.stop="setShow(false)">
    <div class="modal-content was-validated" @click.stop>
      <div class="cross-button">
        <cake-button @click.stop="setShow(false)">
<!--          <img src="@/assets/cross.svg" alt="[закрыть]" @click="setShow(false)" width="30" height="30">-->
          <i class="gg-close"></i>
        </cake-button>
      </div>

      <slot></slot>

    </div>
  </div>
</template>


<script>
export default {
  name: "cake-dialog",
  props: {
    show: {
      type: Boolean,
      default: false,
    }
  },
  emits: ['update:show'],
  methods: {
    setShow(value) {
      this.$emit('update:show', value)
    }
  }
}
</script>

<style scoped>
.modal {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background-color: rgba(69, 67, 81, 0.5);
  position: fixed;
  display: flex;
  color: #454351;
}

.modal-content {
  margin: auto;
  background: #fffeff;
  border: 1px solid rgb(69, 67, 81, 0.7);
  border-radius: 10px;
  min-width: 300px;
  min-height: 50px;
  width: 500px;
  padding: 20px;
}

.cross-button {
  display: flex;
  align-items: center;
  justify-content: end;
}

.gg-close {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 22px;
  height: 22px;
  border: 2px solid transparent;
  border-radius: 40px
}
.gg-close::after,
.gg-close::before {
  content: "";
  display: block;
  box-sizing: border-box;
  position: absolute;
  width: 16px;
  height: 2px;
  background: currentColor;
  transform: rotate(45deg);
  border-radius: 5px;
  top: 8px;
  left: 1px
}
.gg-close::after {
  transform: rotate(-45deg)
}
</style>