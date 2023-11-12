import API from '@/plugins/axios'
import {useToast} from "vue-toastification";
import parsErrorAnswer from "@/plugins/answerParser";

const toast = useToast()

export const ingredient = {
    state: () => ({
        ingredientCatalog: [],
    }),
    getters: {},
    mutations: {
        setIngredient(state, ingredients) {
            state.ingredientCatalog = ingredients;
        },
    },
    actions: {
        async fetchIngredient({state, commit}) {
            try {
                let ingredients = [];
                const response = await API.get('ingredient');

                if (response.status === 200) ingredients = response.data.sort((a,b) => (a.name > b.name) ? 1 : 0)

                commit('setIngredient', ingredients)
            } catch (e) {
                toast.warning('Не удалось получить список ингредиентов.')
            }

            return state.ingredientCatalog
        },
        async createOrUpdateIngredient({state, commit}, {ingredient, uuidIngredient}) {
            try {
                if (uuidIngredient !== null) {
                    const response = await API.put(`ingredient/${uuidIngredient}`, ingredient)

                    if (response.status === 200) {
                        const updatedIngredient = response.data
                        let currentIngredient = state.ingredientCatalog.find(ingr => ingr.uuid === updatedIngredient.uuid)
                        const idxIngredient = state.ingredientCatalog.indexOf(currentIngredient)
                        if (idxIngredient > -1) state.ingredientCatalog[idxIngredient] = updatedIngredient

                        toast.success('Ингредиент обновлен.')
                    }
                } else {
                    const response = await API.post("ingredient", ingredient)
                    if (response.status === 201) {
                        state.ingredientCatalog.unshift(response.data)
                        toast.success('Ингредиент создан.')
                    }
                }
                return true
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
                return false
            }
        },
        async deleteIngredient({state, commit}, index) {
            if (confirm("Точно удалить?")) {
                const ingredient = state.ingredientCatalog.at(index)
                try {
                    const response = await API.delete(`ingredient/${ingredient.uuid}`)
                        if (response.status === 204) {
                            state.ingredientCatalog.splice(index, 1)
                            toast.success('Ингредиент удален.')
                        }
                } catch (e) {
                    const err = parsErrorAnswer(e.response.data.detail)
                    toast.error(err)
                }
            }
        },
    },
    namespaced: true
}