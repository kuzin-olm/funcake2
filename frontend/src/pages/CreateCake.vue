<template>
  <div class="container">
    <h1 v-if="!$route.params.uuid" class="h1 text-center">Новый рецепт</h1>
    <h1 v-else class="h1 text-center">Редактирование</h1>

    <form enctype="multipart/form-data" class="was-validated">

      <div class="mb-3">
        <label for="inputTitle" class="form-label">
          <img src="@/assets/eye.png" alt="[Видно всем]" width="17" height="10">
          Название рецепта/торта
        </label>
        <cake-input v-model="inputTitle" placeholder="Заголовок" required/>
      </div>

      <div class="mb-3">
        <label for="inputAbout" class="form-label">
          <img src="@/assets/eye.png" alt="[Видно всем]" width="17" height="10">
          Краткое описание для превью
        </label>
        <QuillEditor id="inputAbout" v-model:content="inputAbout" content-type="html" theme="snow" toolbar="full"/>
      </div>

      <div class="mb-3">
        <label for="inputRecipe" class="form-label">
          <img src="@/assets/eye_hide.png" alt="[Видно только аторизованным]" width="17" height="10">
          Рецепт
        </label>
        <QuillEditor id="inputRecipe" v-model:content="inputRecipe" content-type="html" theme="snow" toolbar="full"/>
      </div>

      <div class="row">
        <label class="form-label">
          <img src="@/assets/eye.png" alt="[Видно всем]" width="17" height="10">
          Превью (главное фото)
        </label>
      </div>

      <div class="row mb-3">
        <div v-if="inputPrevImage" class="col-6 col-md-2 my-1 budge-del">
          <file-image :src="inputPrevImage" @click="deletePrevImage(inputPrevImage)" class="cake-preview"/>
        </div>
        <div v-else-if="currentPrev" class="col-6 col-md-2 my-1 budge-del">
          <img :src="baseUrl + currentPrev.url" @click="currentPrev=null" class="cake-preview" alt="image"/>
        </div>
        <div v-else class="col-6 col-md-2 my-1 hide-input">
          <label for="PrevImage">
            <img src="@/assets/add_img.svg" alt="[Добавить фото]" class="budge-add">
          </label>
          <file-input id="PrevImage" @change="addPrevImage" accept="image/*"/>
        </div>
      </div>

      <div class="row">
        <label class="form-label">
          <img src="@/assets/eye.png" alt="[Видно всем]" width="17" height="10">
          Дополнительные фото
        </label>
      </div>

      <div class="row mb-3">
        <div class="col-6 col-md-2 my-1 budge-del" v-for="(image, key) in currentOtherImages" :key="key">
          <img :src="baseUrl + image.url" class="cake-preview" @click="deleteCurrentOtherImage(image)" alt="image"/>
        </div>
        <div class="col-6 col-md-2 my-1 budge-del" v-for="(image, key) in inputOtherImages" :key="key">
          <file-image :src="image" class="cake-preview" @click="deleteOtherImage(image)"/>
        </div>

        <div class="col-6 col-md-2 my-1 hide-input">
          <label for="OtherImages">
            <img src="@/assets/add_img.svg" alt="[Добавить фото]" class="budge-add">
          </label>
          <file-input id="OtherImages" @change="addOtherImages" accept="image/*" multiple/>
        </div>
      </div>



      <div class="row">
        <label class="form-label">
          <img src="@/assets/eye_hide.png" alt="[Видно только аторизованным]" width="17" height="10">
          Документы
        </label>
      </div>

      <div class="row mb-3">
        <div class="col-6 col-md-2 my-1 budge-del" v-for="(file, idx) in currentDocs" :key="idx">
          <img src="@/assets/doc_img.svg" :alt="file" class="cake-preview" @click="deleteCurrentDoc(idx)"/>
          <p class="text-center">{{ getNameDoc(file.url).substring(0, 10) }}...</p>
        </div>
        <div class="col-6 col-md-2 my-1 budge-del" v-for="(file, idx) in inputDocs" :key="idx">
          <img src="@/assets/doc_img.svg" :alt="file.name" class="cake-preview" @click="deleteDoc(idx)"/>
          <p class="text-center">{{ file.name.substring(0, 10) }}...</p>
        </div>

        <div class="col-6 col-md-2 my-1 hide-input h-100">
          <label for="forDocs">
            <img src="@/assets/add_img.svg" alt="[Добавить документ]" class="budge-add">
          </label>
          <file-input id="forDocs" @change="addDocs" accept=".doc,.docx,.pdf" multiple/>
        </div>
      </div>

      <div class="row mb-3">
        <div class="col-xl-4 mb-3">
          <div class="form-floating">
            <cake-select v-model="inputVisible" :options="visibleOptions" aria-label="" id="stateTrade"/>
            <label for="stateTrade">Выставить, чтоб видели все?</label>
          </div>
        </div>

        <div class="col-xl-4 mb-3">
          <div class="form-floating">
            <cake-input v-model="inputProfit" type="number" step="0.01" required/>
            <label for="profitRecipe">Профит с продажи, т.е. price x N, где N =</label>
          </div>
        </div>
      </div>

      <div class="btn-access">
        <cake-button @click="goBack" class="btn-cake m-1">Назад</cake-button>
        <cake-button @click="createOrUpdateRecipe" class="btn-success m-1">{{ ($route.params.uuid) ? 'Применить изменения' : 'Создать' }}</cake-button>
        <cake-button v-if="$route.params.uuid" @click="deleteRecipe($route.params.uuid)" class="btn-danger m-1">Удалить</cake-button>
      </div>

    </form>

    <hr>

    <table v-for="(layer, idxLayer) in layers" :key="'layer-'+idxLayer" class="align-middle table table-responsive-sm my-5">
      <thead>
      <tr>
        <td colspan="1">Название слоя: <cake-input v-model="layer.name"/></td>
        <td colspan="1">Диаметр, см: <cake-input type="number" v-model.number="layer.diameter"/></td>
        <td colspan="1">
          <div class="hide-btn">
            <label :for="'trash-layer-'+idxLayer">
              <i class="gg-trash"></i>
            </label>
            <cake-button :id="'trash-layer-'+idxLayer" @click="deleteLayer(idxLayer)" class="btn btn-outline-danger">del</cake-button>
          </div>
        </td>
      </tr>
      </thead>
      <tbody>
      <tr v-if="layer.ingredients.length">
        <td>Название</td>
        <td>Необходимое кол-во</td>
        <td></td>
      </tr>
      <tr v-for="(ingredient, idxIngredient) in layer.ingredients" :key="'layer-'+idxLayer+'-'+idxIngredient">
        <td colspan="1"><cake-select-search v-model:valueUuid="ingredient.uuidIngredient" :options="catalogIngredient"></cake-select-search></td>
        <td colspan="1"><cake-input type="number" v-model.number="ingredient.quantity"/></td>
        <td colspan="1">
          <div class="hide-btn">
            <label :for="'trash-consistency-'+idxLayer+'-'+idxIngredient">
              <i class="gg-trash"></i>
            </label>
            <cake-button :id="'trash-consistency-'+idxLayer+'-'+idxIngredient" @click="deleteIngredientConsistency(idxLayer, idxIngredient)" class="">del</cake-button>
          </div>
        </td>
      </tr>
      </tbody>
      <caption><cake-button @click="addIngredientToLayer(idxLayer)" class="btn-cake col-12">Добавить ингредиент</cake-button></caption>
    </table>

    <div>
      <cake-button @click="addLayer" class="btn-cake col-12">Добавить слой</cake-button>
    </div>

    <cake-dialog v-model:show="dialogTemplate.show">
      <h4 class="text-center mb-3">Добавить слой</h4>
      <cake-select-search
          v-model:selectedObj="dialogTemplate.selectedTemplate"
          :options="templates"
          placeholder="выберите из списка шаблон или оставьте пустым"
          :allow-null="true"
      ></cake-select-search>
      <cake-button @click="addLayerByTemplate" class="btn-success mt-3">Добавить</cake-button>
    </cake-dialog>

    <spinner :isLoading="isLoading"></spinner>
  </div>
</template>

<script>
import CakeInput from "@/components/UI/CakeInput";
import CakeTextarea from "@/components/UI/CakeTextarea";
import FileInput from "@/components/UI/FileInput";
import FileImage from "@/components/UI/FileImage";
import CakeSelect from "@/components/UI/CakeSelect";
import CakeButton from "@/components/UI/CakeButton";
import CakeSelectSearch from "@/components/UI/CakeSelectSearch";
import Alert from "@/components/UI/Alert";
import { QuillEditor } from '@vueup/vue-quill'
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

import '@vueup/vue-quill/dist/vue-quill.snow.css';

export default {
  components: {QuillEditor, CakeButton, CakeSelect, FileImage, FileInput, CakeInput, CakeTextarea, Alert, CakeSelectSearch},
  data() {
    return {
      isLoading: false,

      dialogTemplate: {
        show: false,
        selectedTemplate: null,
      },

      baseUrl: process.env.VUE_APP_BASE_URL,
      currentPrev: null,
      currentOtherImages: [],
      currentDocs: [],

      inputTitle: null,
      inputAbout: null,
      inputRecipe: null,
      inputPrevImage: null,
      inputOtherImages: [],
      inputDocs: [],
      inputProfit: 2.2,
      inputVisible: false,
      layers: [],

      emptyLayer: {
        // uuid: null,
        name: null,
        diameter: null,
        ingredients: []
      },

      emptyIngredientConsistency: {
        // uuid: null,
        quantity: null,
        uuidIngredient: null
      },

      visibleOptions: [
        {value: false, name: 'Не выставлять'},
        {value: true, name: 'Выставить'},
      ],

      catalogIngredient : [],
    }
  },
  computed: {
    ...mapState({
      templates: state => state.templateLayer.templates,
    })
  },
  methods: {
    ...mapActions({
      fetchIngredient: 'ingredient/fetchIngredient',
      createNewRecipe: 'recipe/createRecipe',
      getRecipe: 'recipe/getRecipeDetail',
      updateRecipe: 'recipe/updateRecipe',
      delRecipe: 'recipe/deleteRecipe',
      fetchTemplates: 'templateLayer/fetchTemplates',
    }),
    async createOrUpdateRecipe() {
      let recipe = {
        'title': this.inputTitle,
        'description': this.inputAbout,
        'shortDescription': '',
        'recipeText': this.inputRecipe,
        'profit': this.inputProfit,
        'isTrade': this.inputVisible,
        'layers': this.layers,
        'uuidsCurrentImages': this.getOnlyUUIDS(this.currentOtherImages),
        'uuidsCurrentDocs': this.getOnlyUUIDS(this.currentDocs)
      }

      if (this.$route.params.uuid) {
        recipe["uuid"] = Number(this.$route.params.uuid)
        const statusOk = await this.updateRecipe({
          recipe: recipe,
          uuid: recipe.uuid,
          prev_img: this.inputPrevImage,
          other_imgs: this.inputOtherImages,
          docs: this.inputDocs
        })
        if (statusOk) this.$router.push(`/cakes/${recipe.uuid}`)
      } else {
        const statusOk = await this.createNewRecipe({
              recipe: recipe,
              prev_img: this.inputPrevImage,
              other_imgs: this.inputOtherImages,
              docs: this.inputDocs
        })
        if (statusOk) this.$router.push('/cakes')
      }
    },

    addPrevImage(event) {
      this.inputPrevImage = event.target.files[0];
    },
    deletePrevImage(image) {
      this.inputPrevImage = null
    },

    addOtherImages(event) {
      let selectedFiles = event.target.files;
      for (let i = 0; i < selectedFiles.length; i++) {
        this.inputOtherImages.push(selectedFiles[i]);
      }
    },
    deleteOtherImage(image) {
      let index = this.inputOtherImages.indexOf(image)
      if (index !== -1) {
        this.inputOtherImages.splice(index, 1)
      }
    },
    deleteCurrentOtherImage(image) {
      let index = this.currentOtherImages.indexOf(image)
      if (index !== -1) {
        this.currentOtherImages.splice(index, 1)
      }
    },

    addDocs(event) {
      let selectedFiles = event.target.files;
      for (let i = 0; i < selectedFiles.length; i++) {
        this.inputDocs.push(selectedFiles[i]);
      }
    },
    deleteDoc(index) {
      this.inputDocs.splice(index, 1)
    },
    deleteCurrentDoc(index) {
      this.currentDocs.splice(index, 1)
    },

    addLayer() {
      this.dialogTemplate.show = true
    },
    addLayerByTemplate() {
      let newLayer = JSON.parse(JSON.stringify(this.emptyLayer));

      if (this.dialogTemplate.selectedTemplate) {
        newLayer.name = this.dialogTemplate.selectedTemplate.name
        this.dialogTemplate.selectedTemplate.ingredients.forEach(cons => {
          newLayer.ingredients.push({
            quantity: cons.quantity,
            uuidIngredient: cons.ingredient.uuid
          })
        })
      }

      this.layers.push(newLayer)
      this.dialogTemplate.show = false
      this.dialogTemplate.selectedTemplate = null
    },
    deleteLayer(index) {
      this.layers.splice(index, 1)
    },

    addIngredientToLayer(index) {
      let newIngredientConsistency = JSON.parse(JSON.stringify(this.emptyIngredientConsistency));
      this.layers.at(index).ingredients.push(newIngredientConsistency)
    },
    deleteIngredientConsistency(indexLayer, indexIngredient) {
      this.layers.at(indexLayer).ingredients.splice(indexIngredient, 1)
    },

    goBack() {
      this.$router.go(-1)
    },

    async deleteRecipe(uuid) {
      if (confirm('Точно удалить?')) {
        this.isLoading = true;
        const statusOk = await this.delRecipe({uuid: uuid})
        this.isLoading = false;
        if (statusOk) this.$router.push('/cakes')
      }
    },

    async loadRecipeForUpdate(){
      if (this.$route.params.uuid) {
        this.isLoading = true;
        const recipe = await this.getRecipe({uuid: this.$route.params.uuid})
        this.isLoading = false;

        this.currentPrev = recipe.imgPrev
        this.currentOtherImages = recipe.imgOther
        this.currentDocs= recipe.doc

        this.inputTitle = recipe.title
        this.inputAbout = recipe.description
        this.inputRecipe = recipe.recipeText
        this.inputProfit = recipe.profit
        this.inputVisible = recipe.isTrade

        recipe.layers.forEach(layer => {
          let updLayer = {
            uuid: layer.uuid,
            name: layer.name,
            diameter: layer.diameter,
            ingredients: []
          }

          layer.ingredients.forEach(consistency => {
            let updCons = {
              uuid: consistency.uuid,
              quantity: consistency.quantity,
              uuidIngredient: consistency.ingredient.uuid
            }
            updLayer.ingredients.push(updCons)
          })

          this.layers.push(updLayer)
        })
      }
    },

    async loadIngredient(){
      const ingredients = await this.fetchIngredient();
      ingredients.forEach(ingredient => {
        this.catalogIngredient.push({
          value: ingredient.uuid,
          name: `${ingredient.name} (${ingredient.packing} ${ingredient.measure.name})`,
        })
      })
    },

    getNameDoc(docStr) {
      const strArray = docStr.split("/")
      return strArray[strArray.length - 1]
    },
    getOnlyUUIDS(arr){
      let uuids = []
      if (arr) arr.forEach(each => { uuids.push(each.uuid) })
      return uuids
    },
  },
  mounted() {
    this.loadIngredient().then(
        this.loadRecipeForUpdate
    );
    this.fetchTemplates();
  },
  watch: {
    '$route.params.uuid': function (newUuid, oldUuid) {
      if (!newUuid) {
        this.$router.go(this.$router.currentRoute)
        // this.inputTitle = null
        // this.inputAbout = null
        // this.inputRecipe = null
        // this.inputPrevImage = null
        // this.inputOtherImages = []
        // this.inputDocs = []
        // this.inputProfit = 2.2
        // this.inputVisible = false
        // this.layers = []
      } else {
        this.loadRecipeForUpdate();
      }
    }
  },
}

</script>

<style scoped>
.cake-preview {
  display: flex;
  justify-content: center;
  position: center;
  object-fit: cover;
  width: 150px;
  height: 150px;
  margin: auto;
  border-radius: 10px;
  box-shadow: 0 0 10px 1px rgba(69, 67, 81, 0.17);
}

.cake-preview:hover {
  opacity: 0.5;
  transition: 0.5s;
}

.hide-input {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hide-input > input {
  display: none;
}

.hide-input > label {
  opacity: 0.5;
  border: 1px solid rgba(69, 67, 81, 0.1);
  border-radius: 10px;
  box-shadow: 0 0 10px 1px rgba(69, 67, 81, 0.17);
  width: 150px;
  height: 150px;
}

.hide-input > label:hover {
  transition: 0.3s;
  opacity: 1;
  border-color: #454351;
  box-shadow: 0 0 20px 2px rgba(53, 53, 86, 0.6);
}

.hide-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  /*margin-bottom: 0.3rem;*/
  /*margin-top: 0.25rem;*/
}

.hide-btn > button {
  display: none;
}

.hide-btn > label {
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.4;
  color: #dc3545;
  border: 1px solid rgb(220, 53, 69);
  border-radius: 10px;
  width: 2.35em;
  height: 2.35em;
}

.hide-btn > label:hover {
  transition: 0.3s;
  opacity: 0.9;
  color: #fffeff;
  background-color: #dc3545;
}

.budge-add {
  background-color: #fffeff;
  border-radius: 10px;
  display: block;
  margin: auto;
  width: 100%;
  height: 100%;
}

.budge-del {
  background-image: url('@/assets/del_img.svg');
  background-repeat: no-repeat;
  background-size: 30%;
  background-position: center;
}

.btn-access {
  display: flex;
  justify-content: center;
}

:deep(.ql-container) {
  border-radius: 0 0 10px 10px;
  border-color: #454351;
  background-color: #fffeff;
}

:deep(.ql-toolbar) {
  border-radius: 10px 10px 0 0;
  border-color: #454351;
  background-color: #fffeff;
}
</style>