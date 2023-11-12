<template>
  <transition name="background">
    <div class="spinner" v-if="isLoading">
      <transition name="slide-fade">
        <div class="spinner-content">
          <div class="lds-heart">
            <div></div>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
export default {
  name: "spinner",
  props: {
    isLoading: {type: Boolean, default: false}
  },
}
</script>

<style scoped>
.spinner {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background-color: rgba(69, 67, 81, 0.5);
  position: fixed;
  display: flex;
  z-index: 9999;
}
.spinner-content {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  background: #fffeff;
  border-radius: 10px;
  min-height: 200px;
  min-width: 200px;
  padding: 20px;
}
.lds-heart {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
  transform: rotate(45deg);
  transform-origin: 40px 40px;
}
.lds-heart div {
  top: 32px;
  left: 32px;
  position: absolute;
  width: 32px;
  height: 32px;
  background: rgb(233, 119, 119);
  animation: lds-heart 1.2s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
  /*box-shadow: 0 0 10px 1px rgba(69, 67, 81, 1);*/
}
.lds-heart div:after,
.lds-heart div:before {
  content: " ";
  position: absolute;
  display: block;
  width: 32px;
  height: 32px;
  background: rgb(233, 119, 119);
  /*box-shadow: 0 0 10px 1px rgba(69, 67, 81, 1);*/
}
.lds-heart div:before {
  left: -24px;
  border-radius: 50% 0 0 50%;
}
.lds-heart div:after {
  top: -24px;
  border-radius: 50% 50% 0 0;
}
@keyframes lds-heart {
  0% {
    transform: scale(1.95);
  }
  5% {
    transform: scale(2.1);
  }
  39% {
    transform: scale(1.85);
  }
  45% {
    transform: scale(2);
  }
  60% {
    transform: scale(1.95);
  }
  100% {
    transform: scale(1.9);
  }

}
.slide-fade-enter-active {
  transition: all .8s ease;
}
.slide-fade-leave-active {
  transition: all .2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}

.slide-fade-enter
{
  /*transform: scale(0.5);*/
  transition: all .8s;
  opacity: 1;
}
.slide-fade-leave-to {
  /*transform: scale(0.5);*/
  transition: all .2s;
  opacity: 0;
}

.background-enter-active {
  opacity: 1;
  transition: all .8s;
}
.background-leave-active {
  opacity: 0;
  transition: all .2s;
}
</style>