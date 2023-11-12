import API from '@/plugins/axios'
import {useToast} from "vue-toastification";
import components from "@/components/UI";
import parsErrorAnswer from "@/plugins/answerParser";

const toast = useToast()

export const recipe = {
    state: () => ({
        recipes: [],
    }),
    getters: {},
    mutations: {
        setRecipe(state, recipes) {
            state.recipes = recipes;
        },
    },
    actions: {
        async getRecipeDetail({state, commit}, {uuid}) {
            try {
                const response = await API.get(`recipe/${uuid}`);

                return response.data

            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
            }
            return {}
        },
        async fetchRecipe({dispatch, state, commit}) {
            try {
                const response = await API.get('recipe');
                let recipes = [];

                if (response.status === 200) recipes = response.data.sort((a,b) => (a.uuid < b.uuid) ? 1 : 0)

                commit('setRecipe', recipes)
            } catch (e) {
                toast.warning('Не удалось получить список рецептов.')
            }
        },
        async createRecipe({state, commit}, {recipe, prev_img, other_imgs, docs}) {
            let bodyFormData = new FormData();
            bodyFormData.append('recipe', JSON.stringify(recipe));

            if (prev_img) bodyFormData.append('prev_image', prev_img);
            other_imgs.forEach((img) => bodyFormData.append('other_images', img));
            docs.forEach((doc) => bodyFormData.append('docs', doc));

            try {
                const response = await API.post(
                    'recipe',
                    bodyFormData,
                    {headers: {"Content-Type": "multipart/form-data"}}
                )
                toast.success('Рецепт создан.')
                return true
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
                return false
            }
        },
        async updateRecipe({state, commit}, {recipe, uuid, prev_img, other_imgs, docs}) {
            let bodyFormData = new FormData();
            bodyFormData.append('recipe', JSON.stringify(recipe));

            if (prev_img) bodyFormData.append('prev_image', prev_img);
            other_imgs.forEach((img) => bodyFormData.append('other_images', img));
            docs.forEach((doc) => bodyFormData.append('docs', doc));

            try {
                const response = await API.put(
                    `recipe/${uuid}`,
                    bodyFormData,
                    {headers: {"Content-Type": "multipart/form-data"}}
                )
                toast.success('Рецепт обновлен.')
                return true
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
                return false
            }
        },
        async deleteRecipe({state, commit}, {uuid}) {
            try {
                const response = await API.delete(`recipe/${uuid}`)
                toast.success('Рецепт удален.')
                return true
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
                return false
            }
        }
    },
    namespaced: true
}