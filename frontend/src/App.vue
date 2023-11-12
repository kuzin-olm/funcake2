<template>
  <navbar></navbar>
  <div class="margin-nav"></div>
  <div>
    <transition name="fade">
      <router-view></router-view>
    </transition>
  </div>
  <div class="margin-foot"></div>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
  components: {
    Navbar
  },
  methods: {
    handleStyles () {
      if (['/'].includes(this.$route.path)) document.body.className = 'landing'
      else document.body.className = 'main'
    },
  },
  mounted () {
    this.handleStyles()
  },
  watch: {
    '$route.path' () {
      this.handleStyles()
    }
  }
}
</script>

<style>
@font-face {
  font-family: open-sans-bold;
  src: url('@/assets/ttf/open-sans-bold.ttf');
}

@font-face {
  font-family: open-sans-light;
  src: url('@/assets/ttf/open-sans-light.ttf');
}
html, body {
  height: 100%;
}
body.landing {
  background-image: url('@/assets/funcake_bg_landing.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position-x: center;
}
body.main {
  background-image: url('@/assets/funcake_bg.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position-x: center;
}
.margin-nav {
  margin-bottom: 40px;
}

.margin-foot {
  padding-bottom: 40px;
}

.gg-trash {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 10px;
  height: 12px;
  border: 2px solid transparent;
  box-shadow:
      0 0 0 2px,
      inset -2px 0 0,
      inset 2px 0 0;
  border-bottom-left-radius: 1px;
  border-bottom-right-radius: 1px;
  margin-top: 4px
}
.gg-trash::after,
.gg-trash::before {
  content: '';
  display: block;
  box-sizing: border-box;
  position: absolute
}
.gg-trash::after {
  background: currentColor;
  border-radius: 3px;
  width: 16px;
  height: 2px;
  top: -4px;
  left: -5px
}
.gg-trash::before {
  width: 10px;
  height: 4px;
  border: 2px solid;
  border-bottom: transparent;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
  top: -7px;
  left: -2px
}

.gg-pen {
  box-sizing: border-box;
  position: relative;
  display: block;
  transform: rotate(-45deg);
  width: 14px;
  height: 4px;
  border-right: 2px solid transparent;
  box-shadow:
      0 0 0 2px,
      inset -2px 0 0;
  border-top-right-radius: 1px;
  border-bottom-right-radius: 1px;
  margin-right: -2px
}
.gg-pen::after,
.gg-pen::before {
  content: "";
  display: block;
  box-sizing: border-box;
  position: absolute
}
.gg-pen::before {
  background: currentColor;
  border-left: 0;
  right: -6px;
  width: 3px;
  height: 4px;
  border-radius: 1px;
  top: 0
}
.gg-pen::after {
  width: 8px;
  height: 7px;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  border-right: 7px solid;
  left: -11px;
  top: -2px
}

.gg-check {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 22px;
  height: 22px;
  border: 2px solid transparent;
  border-radius: 100px
}
.gg-check::after {
  content: "";
  display: block;
  box-sizing: border-box;
  position: absolute;
  left: 3px;
  top: -1px;
  width: 6px;
  height: 10px;
  border-width: 0 2px 2px 0;
  border-style: solid;
  transform-origin: bottom left;
  transform: rotate(45deg)
}

.gg-undo {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 14px;
  height: 14px;
  border: 2px solid;
  border-left-color: transparent;
  border-radius: 100px
}
.gg-undo::before {
  content: "";
  display: block;
  box-sizing: border-box;
  position: absolute;
  width: 6px;
  height: 6px;
  border-top: 2px solid;
  border-left: 2px solid;
  top: -3px;
  left: -1px;
  transform: rotate(-68deg)
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s ease;
}
.fade-enter, .fade-leave-active {
  opacity: 0;
}
</style>
