<template>
  <div class="container">
    <div v-if="!$store.state.isAuth" class="window">
      <h1 v-if="isRegistration" class="h1 text-center">Регистрация</h1>
      <h1 v-else class="h1 text-center">Авторизация</h1>

      <form enctype="multipart/form-data">
        <div class="row">
          <div class="mb-3 offset-sm-4 col-sm-4">
            <cake-input class="col-4" v-model="login" placeholder="Логин" required/>
          </div>

          <div class="mb-3 offset-sm-4 col-sm-4">
            <cake-input v-model="password" type="password" placeholder="Пароль" required/>
            <cake-input v-if="isRegistration" class="mt-3" v-model="confirmPassword" type="password"
                        placeholder="Подтверждение пароля" required/>
          </div>

          <div v-if="isRegistration" class="mb-3 offset-sm-4 col-sm-4">
            <cake-button class="col-12 btn-cake" @click="registy">Зарегистрироваться</cake-button>
          </div>
          <div v-else class="mb-3 offset-sm-4 col-sm-4">
            <cake-button class="col-12 btn-cake" @click="auth">Log In</cake-button>
          </div>
          <div class="mb-3 offset-sm-4 col-sm-4">
            <cake-button class="col-12 btn-cake" @click="switchModeAuth">{{ this.textButton }}</cake-button>
          </div>
        </div>
      </form>
    </div>
    <div v-else class="h4 text-center">Вы уже авторизованы</div>
  </div>
</template>

<script>
import CakeButton from "@/components/UI/CakeButton";
import CakeSelect from "@/components/UI/CakeSelect";
import CakeInput from "@/components/UI/CakeInput";
import CakeTextarea from "@/components/UI/CakeTextarea";
import Alert from "@/components/UI/Alert";
import API from "@/plugins/axios";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default {
  components: {CakeButton, CakeSelect, CakeInput, CakeTextarea, Alert},
  name: "Authorization",
  data() {
    return {
      login: "",
      password: "",
      confirmPassword: "",
      isRegistration: false,
      textButton: "Регистрация"
    }
  },
  methods: {
    ...mapActions({
      authenticate: 'auth/authenticate',
      registration: 'auth/registration',
    }),

    switchModeAuth() {
      this.isRegistration = !this.isRegistration
      if (this.isRegistration) this.textButton = "Авторизация"
      else this.textButton = "Регистрация"
    },

    async auth() {
      const statusOk = await this.authenticate({login: this.login, password: this.password})
      if (statusOk) {
        this.login = null
        this.password = null
        this.$router.push('/cakes')
      }
    },

    async registy() {
      const statusOk = await this.registration({
        login: this.login,
        password: this.password,
        confirmPassword: this.confirmPassword
      })
      if (statusOk) {
        this.login = null
        this.password = null
        this.confirmPassword = null
        this.switchModeAuth()
      }
    },
  }
}
</script>

<style scoped>
.window {
  position: fixed;
  top: 25%;
  left: 15%;
  right: 15%;
}
</style>