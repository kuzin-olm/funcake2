<template>
  <div class="container">

    <div class="h1 row align-items-center mb-5">
      <div class="col-8 col-xl-10">
        <p class="h3">Шаблоны групп</p>
      </div>
      <div class="col-4 col-xl-2">
        <cake-button @click="addNewTemplate" type="button" class="btn-outline-success w-100">добавить</cake-button>
      </div>
    </div>

    <div class="accordion accordion-flush" id="accordionFlushTable">

      <template v-for="(template, idx) in templates">
        <div class="accordion-item">
          <h2 class="accordion-header" :id="`flush-heading-${idx}`">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="`#flush-collapse-${idx}`" aria-expanded="false" :aria-controls="`flush-collapse-${idx}`">
              <strong v-if="!template.isEdit">{{ template.name }}</strong>
              <cake-input v-else v-model="selectedTemplate.name"/>
            </button>
          </h2>
          <div :id="`flush-collapse-${idx}`" class="accordion-collapse collapse" :aria-labelledby="`flush-heading-${idx}`" data-bs-parent="#accordionFlushTable">
            <div class="accordion-body">

              <div v-if="!template.isEdit" class="hide-btn mb-2 float-end">
                <label :for="'edit-'+idx" class="warning mx-1">
                  <i class="gg-pen"></i>
                </label>
                <cake-button @click="selectTemplate(idx)" :id="'edit-'+idx">edit</cake-button>

                <label :for="'trash-'+idx" class="danger mx-1">
                  <i class="gg-trash"></i>
                </label>
                <cake-button @click="deleteTemplate(idx, template.uuid)" :id="'trash-'+idx">del</cake-button>
              </div>
              <div v-else class="hide-btn mb-2 float-end">
                <label :for="'check-'+idx" class="success mx-1">
                  <i class="gg-check"></i>
                </label>
                <cake-button @click="createOrUpdateTemplate(idx, template.uuid)" :id="'check-'+idx">edit</cake-button>

                <label :for="'undo-'+idx" class="danger mx-1">
                  <i class="gg-undo"></i>
                </label>
                <cake-button @click="resetSelectedTemplate(idx)" :id="'undo-'+idx">del</cake-button>
              </div>

              <table class="align-middle table table-responsive-sm">
                <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Ингредиент</th>
                  <th scope="col">Кол-во</th>
                  <th v-if="template.isEdit" scope="col"></th>
                </tr>
                </thead>

                <tbody v-if="!template.isEdit">
                  <tr v-for="(consistency, conIdx) in template.ingredients" >
                    <th scope="col">{{ conIdx + 1 }}</th>
                    <td>{{ consistency.ingredient.name }} (фасовка: {{consistency.ingredient.packing}} {{consistency.ingredient.measure.name}})</td>
                    <td>{{ consistency.quantity }}</td>
                  </tr>
                </tbody>
                <tbody v-else>
                  <tr v-for="(consistency, conIdx) in selectedTemplate.ingredients">
                    <th scope="col">{{ conIdx + 1 }}</th>
                    <td>
                      <cake-select-search
                          v-model:valueUuid="selectedTemplate.ingredients[conIdx].uuidIngredient"
                          :options="catalogIngredient">
                      </cake-select-search>
                    </td>
                    <td><cake-input type="number" v-model.number="selectedTemplate.ingredients[conIdx].quantity"/></td>
                    <td>
                      <div class="hide-btn">
                        <label :for="'trash-cons-'+conIdx" class="danger mx-1">
                          <i class="gg-trash"></i>
                        </label>
                        <cake-button :id="'trash-cons-'+conIdx" @click="selectedTemplate.ingredients.splice(conIdx, 1)">
                          del
                        </cake-button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <cake-button v-if="template.isEdit" @click="addIngredientToSelectedTemplate" class="btn-cake col-12">Добавить ингредиент</cake-button>

            </div>
          </div>
        </div>
      </template>

    </div>

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
import {useToast} from "vue-toastification";
import parsErrorAnswer from "@/plugins/answerParser";

const toast = useToast()

export default {
  components: {CakeSelect, CakeInput, CakeButton, Spinner, Alert},
  data() {
    return {
      isLoading: false,
      showDialog: false,
      catalogIngredient: [],

      selectedTemplate: {
        name: null,
        ingredients: []
      },
    }
  },
  computed: {
    ...mapState({
      templates: state => state.templateLayer.templates,
    }),

    isEdit(){
      for (let i = 0; i < this.templates.length; i++) {
        if (this.templates[i].isEdit) {
          return true
        }
      }
      return false
    }
  },
  methods: {
    ...mapActions({
      fetchIngredient: 'ingredient/fetchIngredient',
      fetchTemplates: 'templateLayer/fetchTemplates',
    }),

    async loadIngredient(){
      const ingredients = await this.fetchIngredient();
      this.catalogIngredient = []
      ingredients.forEach(ingredient => {
        this.catalogIngredient.push({
          value: ingredient.uuid,
          name: `${ingredient.name} (${ingredient.packing} ${ingredient.measure.name})`,
        })
      })
    },

    async fetchCatalogs() {
      this.isLoading = true;
      await this.loadIngredient();
      await this.fetchTemplates();
      this.isLoading = false;
    },

    selectTemplate(idx){
      if (this.isEdit) {
        toast.error("Нельзя редактировать несколько шаблонов одновременно.")
        return
      }

      let template = JSON.parse(JSON.stringify(this.templates[idx]));

      this.selectedTemplate = {name: template.name, ingredients: []}
      template.ingredients.forEach(consystency => {
        this.selectedTemplate.ingredients.push(
            {
              uuid: consystency.uuid,
              quantity: consystency.quantity,
              uuidIngredient: consystency.ingredient.uuid
            }
        )
      })
      this.templates[idx].isEdit = true
    },
    resetSelectedTemplate(idx){
      this.selectedTemplate.name = null
      this.selectedTemplate.ingredients = []

      if (this.templates[idx].uuid) this.templates[idx].isEdit = false
      else this.templates.splice(idx, 1)
    },
    addIngredientToSelectedTemplate(){
      this.selectedTemplate.ingredients.push(
          {
            uuid: null,
            quantity: null,
            uuidIngredient: null
          }
      )
    },
    async createOrUpdateTemplate(idx, uuid){
      if (!confirm('Подтвердить изменения?')) return

      this.isLoading = true
      if (uuid) {
        await API.put(`/template-layer/${uuid}`, this.selectedTemplate).then(response => {
          this.templates[idx] = response.data
          toast.success("Шаблон обновлен.")
          this.resetSelectedTemplate(idx)
        }).catch(error => {
          const err = parsErrorAnswer(error.response.data.detail)
          toast.error(err)
        })
      } else {
        await API.post(`/template-layer`, this.selectedTemplate).then(response => {
          this.templates[idx] = response.data
          toast.success("Шаблон создан.")
          this.resetSelectedTemplate(idx)
        }).catch(error => {
          const err = parsErrorAnswer(error.response.data.detail)
          toast.error(err)
        })
      }
      this.isLoading = false
    },
    addNewTemplate(){
      if (this.isEdit) {
        toast.error("Нельзя добавлять несколько шаблонов одновременно.")
        return
      }
      this.templates.unshift({name: null, ingredients: []})
      this.selectTemplate(0)
    },
    async deleteTemplate(idx, uuid){
      if (!confirm('Удалить шаблон?')) return

      this.isLoading = true
      await API.delete(`/template-layer/${uuid}`).then(response => {
        this.templates.splice(idx, 1)
        toast.success("Шаблон удален.")
      }).catch(error => {
        const err = parsErrorAnswer(error.response.data.detail)
        toast.error(err)
      })
      this.isLoading = false
    }
  },

  mounted() {
    this.fetchCatalogs();
  },
}
</script>

<style scoped>
thead {
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
  width: 2.35em;
  height: 2.35em;
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

.hide-btn .success {
  color: #198754;
  border: 1px solid rgb(25, 135, 84);
}

.hide-btn .success:hover {
  color: #fffeff;
  background-color: #198754;
}
</style>