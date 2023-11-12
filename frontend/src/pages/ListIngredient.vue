<template>
  <div class="container">

    <div class="h1 row align-items-center mb-5">
      <div class="col-8 col-xl-10">
        <p class="h3">Список ингредиентов</p>
      </div>
      <div class="col-4 col-xl-2">
        <cake-button @click="ingredientDialog()" type="button" class="btn-outline-success w-100">добавить</cake-button>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-hover caption-top">
        <thead class="table-light">
        <tr>
          <th scope="col">#</th>
          <th scope="col">Название</th>
          <th scope="col">Фасовка</th>
          <th scope="col">Цена</th>
          <th scope="col"></th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="(ingredient, idx) in ingredients" class="align-middle">
          <th scope="col">{{ idx + 1 }}</th>
          <td>{{ ingredient.name }}</td>
          <td>{{ ingredient.packing }} {{ ingredient.measure.name }}</td>
          <td :class="{'table-danger': ingredient.price === 0}">{{ ingredient.price }}</td>
          <td class="text-center">
            <div class="hide-btn">
              <label :for="'edit-'+idx" class="warning mx-1">
                <i class="gg-pen"></i>
              </label>
              <cake-button @click="ingredientDialog(idx)" :id="'edit-'+idx">edit</cake-button>

              <label :for="'trash-'+idx" class="danger mx-1">
                <i class="gg-trash"></i>
              </label>
              <cake-button @click="ingredientDelete(idx)" :id="'trash-'+idx">del</cake-button>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <cake-dialog v-model:show="showDialog">
      <h3 class="text-center mb-3">Добавление ингридиента</h3>
      <div class="form-floating col-12">
        <label for="NameIngredient">Название ингридиента</label>
        <cake-input class="my-2" v-model="inputNameIngredient" id="NameIngredient" required/>
      </div>
      <div class="form-floating col-12">
        <label for="PackingIngredient">Весовка</label>
        <cake-input class="my-2" type="number" step="0.01" v-model.number="inputPackingIngredient" id="PackingIngredient" required/>
      </div>
      <div class="form-floating col-12">
        <label for="MeasureIngredient">Ед. измерения</label>
        <cake-select class="my-2" v-model.number="inputMeasureIngredient" :options="catalogMeasure"
                     id="MeasureIngredient" required/>
      </div>
      <div class="form-floating col-12">
        <label for="PriceIngredient">Цена ингридиента</label>
        <cake-input class="my-2" type="number" step="0.01" v-model.number="inputPriceIngredient" id="PriceIngredient" required/>
      </div>
      <cake-button @click="createOrUpdateIngredient()" class="btn-success mt-3">Сохранить</cake-button>
    </cake-dialog>

    <Spinner :isLoading="isLoading"></Spinner>
  </div>
</template>

<script>
import CakeButton from "@/components/UI/CakeButton";
import Spinner from "@/components/UI/Spinner";
import API from '@/plugins/axios'
import CakeInput from "@/components/UI/CakeInput";
import CakeSelect from "@/components/UI/CakeSelect";
import Alert from "@/components/UI/Alert";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default {
  components: {CakeSelect, CakeInput, CakeButton, Spinner, Alert},
  data() {
    return {
      isLoading: false,
      showDialog: false,

      inputIdIngredient: null,
      inputNameIngredient: null,
      inputPriceIngredient: null,
      inputMeasureIngredient: null,
      inputPackingIngredient: null,
    }
  },
  computed: {
    ...mapState({
      ingredients: state => state.ingredient.ingredientCatalog,
      catalogMeasure: state => state.measure.measureCatalog,
    }),
  },
  methods: {
    ...mapActions({
      fetchMeasure: 'measure/fetchMeasure',
      fetchIngredient: 'ingredient/fetchIngredient',
      createUpdateIngredient: 'ingredient/createOrUpdateIngredient',
      ingredientDel: 'ingredient/deleteIngredient'
    }),

    ingredientDialog(index = null) {
      if (index !== null) {
        const ingredient = this.ingredients.at(index)
        this.inputNameIngredient = ingredient.name
        this.inputPackingIngredient = ingredient.packing
        this.inputMeasureIngredient = ingredient.measure.uuid
        this.inputPriceIngredient = ingredient.price
        this.inputIdIngredient = ingredient.uuid
      } else {
        this.inputNameIngredient = null
        this.inputPackingIngredient = null
        this.inputMeasureIngredient = null
        this.inputPriceIngredient = null
        this.inputIdIngredient = null
      }
      this.showDialog = true;
    },
    async createOrUpdateIngredient() {
      this.isLoading = true

      let ingredient = {
        name: this.inputNameIngredient,
        price: this.inputPriceIngredient,
        packing: this.inputPackingIngredient,
        uuidMeasure: this.inputMeasureIngredient
      }

      const statusOk = await this.createUpdateIngredient({ingredient: ingredient, uuidIngredient: this.inputIdIngredient})
      if (statusOk) this.showDialog = false;
      this.isLoading = false;
    },
    async ingredientDelete(index) {
      this.isLoading = true;
      await this.ingredientDel(index);
      this.isLoading = false;
    },

    async fetchCatalogs() {
      this.isLoading = true;
      await this.fetchIngredient();
      await this.fetchMeasure();
      this.isLoading = false;
    }
  },

  mounted() {
    this.fetchCatalogs();
  },
}
</script>

<style scoped>
.hide-btn {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hide-btn > button {
  display: none;
}

.hide-btn > label {
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.4;
  border-radius: 10px;
  width: 30px;
  height: 30px;
}

.hide-btn > label:hover {
  transition: 0.3s;
  opacity: 0.9;
}

.hide-btn .danger {
  color: #dc3545;
  border: 1px solid rgb(220, 53, 69);
}

.hide-btn .danger:hover {
  color: #fffeff;
  background-color: #dc3545;
}

.hide-btn .warning {
  color: #ffc107;
  border: 1px solid rgb(255, 193, 7);
}

.hide-btn .warning:hover {
  color: #fffeff;
  background-color: #ffc107;
}

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