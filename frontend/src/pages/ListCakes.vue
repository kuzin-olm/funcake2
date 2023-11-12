<template>
  <div class="container">
    <section class="container text-center">

      <figure class="text-center mb-5">
        <blockquote class="blockquote">
          <p style="color: #444251;">Шоколадный с шоколадом. С шоколадной начинкой и шоколадной крошкой сверху. И
            чашечка горячего шоколада рядом.</p>
        </blockquote>
        <figcaption class="blockquote-footer">
          Дженсен Эклз <cite title="Source Title">американский актер и режиссер, певец 1978</cite>
        </figcaption>
      </figure>
    </section>

    <div class="container-xl">
      <div class="row">
        <div class="mb-3" v-bind:class="{'col-sm-10': $store.state.isAuth,  'col-sm-12': !$store.state.isAuth}">
          <cake-input v-model="searchQuery" placeholder="Поиск по рецептам"></cake-input>
        </div>
        <div v-if="$store.state.isAuth" class="mb-3 col-sm-2">
          <cake-select v-model="selectedSort" :options="sortOptions" aria-label="Search"></cake-select>
        </div>
      </div>
    </div>

    <div class="album py-5">
      <div class="container-xl">

        <div class="row row-cols-1 row-cols-md-2 row-cols-xl-4 g-3">
          <cake-card v-for="recipe in filteredAndSearchedRecipes" :recipe="recipe" class="col"></cake-card>
        </div>
      </div>
    </div>

    <spinner :isLoading="isLoading"></spinner>
  </div>
</template>

<script>
import CakeInput from "@/components/UI/CakeInput";
import CakeSelect from "@/components/UI/CakeSelect";
import Spinner from "@/components/UI/Spinner";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';
import CakeCard from "@/components/CakeCard";

export default {
  components: {CakeCard, CakeSelect, CakeInput, Spinner},

  data() {
    return {
      searchQuery: '',
      selectedSort: 'all',
      sortOptions: [
        {value: 'all', name: 'Все'},
        {value: 'true', name: 'Продаются'},
        {value: 'false', name: 'Не продаются'},
      ],
      isLoading: false,
    }
  },
  computed: {
    ...mapState({
      recipes: state => state.recipe.recipes,
    }),
    filteredTradeRecipes() {
      if (this.selectedSort !== 'all') {
        const isTrade = this.selectedSort === 'true'
        return [...this.recipes].filter(recipe => recipe.isTrade === isTrade)
      }
      return this.recipes
    },
    filteredAndSearchedRecipes() {
      return this.filteredTradeRecipes.filter(recipe => recipe.title.toLowerCase().includes(this.searchQuery.toLowerCase()))
    }
  },
  methods: {
    ...mapActions({
      getRecipes: 'recipe/fetchRecipe',
    }),

    async fetchRecipes() {
      this.isLoading = true;
      await this.getRecipes()
      this.isLoading = false;
    },
  },
  mounted() {
    this.fetchRecipes()
  },
}
</script>

<style scoped>
</style>