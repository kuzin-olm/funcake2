<template>
  <transition name="alert-msg" class="alert alert-danger">
    <div v-if="$store.state.isAlert" @click="this.$store.commit('closeAlert', )">
      <p>Ошибка: {{ $store.state.errMsg }}</p>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Alert",
}
</script>

<style scoped>
.alert {
  position: fixed;
  top: 7%;
  left: 15%;
  right: 15%;
}

.alert-msg-enter-active {
  position: fixed;
  top: 7%;
  left: 15%;
  right: 15%;
  animation: alert-enter- 0.3s;
}

@keyframes alert-enter- {
  0% {
    opacity: 0;
    top: 12%;
  }
  100% {
    opacity: 1;
    top: 7%;
  }
}

.alert-msg-leave-active {
  transition: all 0.3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
  opacity: 0;
}
</style>