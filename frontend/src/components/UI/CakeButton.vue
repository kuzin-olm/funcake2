<template>
  <button type="button" class="btn">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'cake-button'
}
</script>

<style scoped>
.btn {
  border-radius: 10px;
}


.btn-cake {
  border-color: #454351;
  background-color: #fffeff;
}

.btn-cake:hover {
  color: #fffeff;
  background-color: #454351;
  border-color: #454351;
}

.btn-cake:focus,
.btn-cake.focus {
  color: #444251;
  background-color: #fff;
  border-color: #454351;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(53, 53, 86, 0.25);
}

/*.btn-cake:focus + .btn-cake, .btn-cake:focus {*/
/*  background-color: #453949;*/
/*  color: #fffeff;*/
/*}*/

.btn-cake.disabled,
.btn-cake:disabled {
  color: #4c4a59;
  border-color: #4c4a59
}

.btn-cake:not(:disabled):not(.disabled):active,
.btn-cake:not(:disabled):not(.disabled).active,
.show>.btn-cake.dropdown-toggle {
  color: #fffeff;
  background-color: #454351;
  border-color: #454351
}
</style>