<template>
  <header>
    <!-- Fixed navbar -->
    <nav
        :style="navbarStyle"
        class="navbar navbar-expand-lg navbar-light"
        id="nav"
    >
      <div class="container">
        <router-link class="navbar-brand" to="/cakes">FunCake</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">

          <ul v-if="$store.state.isAuth" class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="f-a nav-link" :class="isCurrentPage('/ingredient')" to="/ingredient">Ингредиенты
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="f-a nav-link" :class="isCurrentPage('/template-group')" to="/template-group">Шаблоны групп</router-link>
            </li>
            <li class="nav-item">
              <router-link class="f-a nav-link" :class="isCurrentPage('/create')" to="/create">Новый рецепт
              </router-link>
            </li>
          </ul>
          <ul v-else class="navbar-nav me-auto mb-2 mb-lg-0"></ul>

          <div class="d-flex">
            <router-link v-if="$store.state.isAdmin" class="nav-link" tabindex="-1" aria-disabled="true" to="">{{$store.state.nickname}}</router-link>
            <router-link v-else class="nav-link text-secondary" tabindex="-1" aria-disabled="true" to="">{{$store.state.nickname}}</router-link>

            <cake-button v-if="!$store.state.isAuth" class="btn-cake m-1 my-sm-0" @click="$router.push('/auth')">Авторизация/Регистрация</cake-button>
            <cake-button v-else class="btn-outline-danger m-1 my-sm-0" @click="logoutUser">Выйти</cake-button>
          </div>
        </div>

      </div>
    </nav>
  </header>
</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default {
  components: {},

  data() {
    return {
      navbarStyle: {
        backgroundColor: "",
        boxShadow: "",
        borderRadius: "0px 0px 10px 10px",
      }
    }
  },
  methods: {
    ...mapActions({
      checkAuth: 'auth/checkAuth',
      logout: 'auth/logout',
    }),

    onScroll(event) {
      if (window.top.scrollY > 20) {
        this.navbarStyle.backgroundColor = "#e9e8ee"
        this.navbarStyle.boxShadow = "0 1rem 3rem rgba(69, 67, 81, 0.3) !important"
      } else {
        this.navbarStyle.backgroundColor = ""
        this.navbarStyle.boxShadow = ""
      }
    },

    isCurrentPage(conditionPath) {
      return {active: this.$route.path === conditionPath}
    },

    logoutUser(event) {
      this.logout()
      this.$router.go(this.$router.currentRoute)
    }
  },
  mounted() {
    this.checkAuth()
  },
}


</script>

<style scoped>
@font-face {
  font-family: rose;
  src: url('@/assets/ttf/rose.ttf');
}

.navbar-brand {
  color: #444251;
  font-family: rose, serif;
  font-weight: bolder;
  font-size: 1.6rem;
}

A.f-a {
  color: #444251;
}

A.f-a:link {
  text-decoration: none;
  color: #444251;
}

A.f-a:visited {
  text-decoration: none;
  color: #444251;
}

A.f-a:active {
  text-decoration: none;
  color: #444251;
}

A.f-a:hover {
  color: #444251;
}

a.f-a.nav-link.active::after {
  content: '';
  display: block;
  width: 100%;
  height: 3px;
  background: #444251;
}

a.f-a.nav-link.disabled {
  color: rgba(68, 66, 81, 0.6);
}

A.f-a::after {
  content: '';
  display: block;
  width: 0;
  height: 3px;
  background: #444251;
  transition: width .3s;
}

A.f-a:hover::after {
  width: 100%;
  transition: width .3s;
}
</style>