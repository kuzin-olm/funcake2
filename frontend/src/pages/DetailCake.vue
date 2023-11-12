<template>
  <div class="container">
    <div class="row align-items-center">
      <div class="col-12 col-xl-6">
        <div>
          <h2 class="f-text-bold">{{ recipe.title }}</h2>
          <p class="detail mt-4"  v-html="recipe.description"></p>
          <cake-button @click="$router.go(-1)" class="btn btn-cake my-5">На главную</cake-button>
        </div>
      </div>
      <div class="col-12 col-xl-6">
        <!--        {% if  other_images | length > 0%}-->
        <div id="carouselControls" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner rounded-25 shadow">
            <div class="carousel-item active">
              <img v-if="recipe.imgPrev" :src="baseUrl + recipe.imgPrev.url" class="d-block w-100" alt="...">
              <img v-else src="@/assets/cake_logo.png" class="d-block w-100" alt="...">
            </div>
            <div class="carousel-item" v-for="image in recipe.imgOther">
              <img :src="baseUrl + image.url" class="d-block w-100" alt="...">
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselControls" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselControls" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
        <!--        {% endif %}-->
      </div>
    </div>

    <div v-if="$store.state.isAuth" class="mt-5">

      <h4 class="mb-3">Рецепт</h4>
      <p class="detail mb-4" v-html="recipe.recipeText"></p>

      <div v-if="recipe.doc" class="mb-3">
        <h5>Документы</h5>
        <div v-for="doc in recipe.doc" class="row">
          <div class="col">
            <a :href="baseUrl + doc.url" class="link-primary">{{ getNameDoc(doc.url) }}</a>
          </div>
        </div>
      </div>


<!--      <button type="button" class="btn btn-sm btn-outline-secondary my-3" data-bs-toggle="modal"-->
<!--              data-bs-target="#restructDiameter">изменить диаметр и пересчитать ингредиенты-->
<!--      </button>-->
      <div class="accordion accordion-flush" id="accordionFlushTable">
        <div class="accordion-item">
          <h2 class="accordion-header" id="flush-headingOne">
            <button class="accordion-button collapsed btn-secondary" type="button" data-bs-toggle="collapse"
                    data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
              <strong>Список ингредиентов</strong>
            </button>
          </h2>
          <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
               data-bs-parent="#accordionFlushTable">
            <div class="accordion-body table-responsive">

              <table class="table table-striped caption-top table-responsive align-middle">

<!--                <thead class="table-light">-->
                <thead>
                <tr>
                  <th scope="col" colspan="5">Группы</th>
                </tr>
                </thead>

                <tbody>
                <template v-for="layer in recipe.layers">
                  <tr>
                    <td colspan="4"><strong> {{ layer.name }} (диаметер: {{ layer.diameter }}) </strong></td>
                  </tr>
                  <tr>
                    <td colspan="4">
                      <table class="table table-hover mb-0">
                        <tbody>
                        <tr>
                          <td>Название</td>
                          <td>Необходимо</td>
                          <td>Цена</td>
                        </tr>
                        <tr v-for="consistency in layer.ingredients">
                          <td>{{ consistency.ingredient.name }}</td>
                          <td>{{ consistency.quantity }} {{ consistency.ingredient.measure.name }}</td>
                          <td :class="{ 'table-danger': consistency.ingredient.price === 0 }">
                            {{ (consistency.ingredient.price / consistency.ingredient.packing * consistency.quantity).toFixed(2) }}
                          </td>
                        </tr>
                        <tr>
                          <td colspan="2">Стоимость ингредиентов</td>
                          <td>{{ layer.cost }}</td>
                        </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </template>
                </tbody>

                <tfoot>
<!--                <tr class="table-light">-->
                <tr>
                  <td colspan="3">Стоимость ингредиентов</td>
                  <td>{{ recipe.totalCost }}</td>
                </tr>
<!--                <tr class="table-light">-->
                <tr>
                  <td colspan="3">Стоимость с учетом трудозатрат (x {{ recipe.profit }})</td>
                  <td colspan="1">{{ recipe.totalCost * recipe.profit }}</td>
                </tr>
<!--                <tr class="table-light">-->
                <tr>
                  <td colspan="3">Приблизительный суммарный вес</td>
                  <td colspan="1">{{ recipe.totalQty }} грамм</td>
                </tr>
                </tfoot>
              </table>

            </div>
          </div>
        </div>

        <div class="accordion-item">
          <h2 class="accordion-header" id="flush-headingTwo">
            <button class="accordion-button collapsed btn-secondary" type="button" data-bs-toggle="collapse"
                    data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseOne">
              <strong>Список покупок</strong>
            </button>
          </h2>
          <div id="flush-collapseTwo" class="accordion-collapse collapse" aria-labelledby="flush-headingOne"
               data-bs-parent="#accordionFlushTable">
            <div class="accordion-body table-responsive">

              <table class="table table-sm table-hover align-middle">
<!--                <thead class="table-light">-->
                <thead>
                <tr>
                  <th scope="col">Название</th>
                  <th scope="col">Необходимо</th>
                  <th scope="col">Фасовка</th>
                  <th scope="col">Кол-во</th>
                  <th scope="col">Цена</th>
                </tr>
                </thead>
                <tbody>

                <tr v-for="ingredient in recipe.shoppingList">
                  <td>{{ ingredient.name }}</td>
                  <td>{{ ingredient.quantity }} {{ ingredient.measure }}</td>
                  <td>{{ ingredient.packing }} {{ ingredient.measure }}</td>
                  <td>{{ ingredient.shopQty }}</td>
                  <td>{{ ingredient.price }}</td>
                </tr>

                </tbody>
                <tfoot>
<!--                <tr class="table-light">-->
                <tr>
                  <td colspan="4">Стоимость ингредиентов</td>
                  <td>{{ recipe.shoppingListCost }}</td>
                </tr>
                </tfoot>
              </table>

            </div>
          </div>
        </div>
      </div>

      <div class="row my-5">
        <div class="col">
          <cake-button class="btn btn-cake m-1" @click="$router.push('/cakes')">На главную</cake-button>
          <cake-button class="btn btn-cake m-1" @click="$router.push(`/create/${recipe.uuid}`)">Редактировать</cake-button>
          <cake-button class="btn-outline-danger m-1" @click="deleteRecipe">Удалить</cake-button>
        </div>
      </div>

    </div>

    <Spinner :isLoading="isLoading"></Spinner>
  </div>
</template>

<script>
import Spinner from "@/components/UI/Spinner";
import {mapActions} from "vuex";
import Alert from "@/components/UI/Alert";
import CakeButton from "@/components/UI/CakeButton";

export default {
  components: {CakeButton, Alert, Spinner},
  data() {
    return {
      baseUrl: process.env.VUE_APP_BASE_URL,

      recipe: {},

      isLoading: false
    }
  },
  methods: {
    ...mapActions({
      getRecipe: 'recipe/getRecipeDetail',
      delRecipe: 'recipe/deleteRecipe',
    }),

    async fetchRecipe() {
      this.isLoading = true;
      this.recipe = await this.getRecipe({uuid: this.$route.params.uuid})
      this.isLoading = false;
    },
    async deleteRecipe() {
      if (confirm('Точно удалить?')) {
        this.isLoading = true;
        const statusOk = await this.delRecipe({uuid: this.recipe.uuid})
        this.isLoading = false;
        if (statusOk) this.$router.push('/cakes')
      }
    },

    getNameDoc(docStr) {
      const strArray = docStr.split("/")
      return strArray[strArray.length - 1]
    }
  },
  mounted() {
    this.fetchRecipe();
  },
}
</script>

<style scoped>
.rounded-25 {
  border-radius: 25px !important;
}

.shadow {
  box-shadow: 0 0 20px 2px rgba(53, 53, 86, 0.6) !important;
}

thead, tfoot {
  color: #454351;
  background: rgba(69, 67, 81, 0.1);
}

.accordion-item {
  margin-bottom: 20px;
  border-radius: 10px;
  border: 1px solid rgba(69, 67, 81, 0.1);
  box-shadow: 0 0 10px 1px rgba(69, 67, 81, 0.17);
  background-color: rgba(69, 67, 81, 0.1);
  backdrop-filter: blur(15px);
  background-clip: border-box;
}

.accordion-item .accordion-button {
  color: #454351;
  border-radius: 10px;
  backdrop-filter: blur(15px);
  background-color: rgba(69, 67, 81, 0.1);
}
.accordion-item .accordion-button:focus {
  outline: 0;
  box-shadow: none;
}

.accordion-item:hover, .accordion-item:first-of-type:hover, .accordion-item:last-of-type:hover {
  transition: 0.3s;
  border-color: #454351;
  box-shadow: 0 0 20px 2px rgba(53, 53, 86, 0.61);
}

.accordion-item:first-of-type {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border: 1px solid rgba(69, 67, 81, 0.1);
}
.accordion-item:first-of-type .accordion-button {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.accordion-item:last-of-type {
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  border: 1px solid rgba(69, 67, 81, 0.1);
}
.accordion-item:last-of-type .accordion-button.collapsed {
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}
.accordion-item:last-of-type .accordion-collapse {
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.detail :deep(p) {
  margin-bottom: 0.1rem;
}
</style>