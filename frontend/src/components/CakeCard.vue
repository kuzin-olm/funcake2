<template>
  <div>
    <router-link class="card card-shadow" :to="{ name: 'detailCake', params: { uuid: recipe.uuid }}">
      <svg class="card-img-fun" xmlns="http://www.w3.org/2000/svg" role="img"
           aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false">
        <title>{{ recipe.title }}</title>
        <rect width="100%" height="100%" fill="#55595c"/>
        <text x="35%" y="50%" fill="#eceeef" dy=".3em">Thumbnail</text>

        <image v-if="recipe.imgPrev" v-bind="{'xlink:href' : baseUrl + recipe.imgPrev.url}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"/>
        <image v-else v-bind="{'xlink:href' : require('@/assets/cake_logo.png')}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"/>
      </svg>

      <div class="card-body">
        <h5 class="card-title f-text-bold">{{ truncate(recipe.title, 30) }}</h5>
<!--        <p class="card-text f-text-light" v-html="truncate(recipe.description, 125)"></p>-->
        <div class="d-flex justify-content-between align-items-center">
          <small v-if="$store.state.isAuth" class="text-muted">{{ recipe.isTrade? 'Продается':'Не продается' }}</small>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "CakeCard",
  props: {
    recipe: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      baseUrl: process.env.VUE_APP_BASE_URL,
    }
  },
  methods: {
    truncate(text, stop, clamp) {
      return text.slice(0, stop) + (stop < text.length ? clamp || '...' : '')
    }
  }
}
</script>

<style scoped>
.f-text-bold {
  font-family: open-sans-bold, serif;
  color: #444251;
}

.f-text-light {
  /*font-family: open-sans-light;*/
  color: #444251;
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 450px;
  word-wrap: break-word;
  background-color: rgba(69, 67, 81, 0.1);
  backdrop-filter: blur(15px);
  background-clip: border-box;
  border: 1px solid rgba(69, 67, 81, 0.1);
  border-radius: 25px;
}

.card-body {
  position: fixed;
  bottom: 3.5%;
  left: 5%;
  right: 5%;
  background-color: rgba(241, 241, 241, 0.6);
  backdrop-filter: blur(15px);
  border-radius: 25px;
  padding: 0.7rem 1rem 0.3rem;
}

.card.card-shadow {
  border: 1px solid rgba(69, 67, 81, 0.1);
  box-shadow: 0 0 10px 1px rgba(69, 67, 81, 0.17);
}

.card-img-fun {
  width: 100%;
  height: 100%;
  border-radius: 25px;
}

a.card {
  text-decoration: none;
}

a.card:hover {
  transition: 0.5s;
  border-color: #454351;
  box-shadow: 0 0 20px 2px rgba(53, 53, 86, 0.6);
}
</style>