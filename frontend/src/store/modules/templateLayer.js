import API from '@/plugins/axios'
import {useToast} from "vue-toastification";
import parsErrorAnswer from "@/plugins/answerParser";

const toast = useToast()

export const templateLayer = {
    state: () => ({
        templates: [],
    }),
    getters: {},
    mutations: {
        setTemplates(state, templates) {
            state.templates = templates;
        },
    },
    actions: {
        async fetchTemplates({state, commit}) {
            try {
                let templates = [];
                const response = await API.get('template-layer');

                if (response.status === 200) templates = response.data.sort((a,b) => (a.name > b.name) ? 1 : 0)

                commit('setTemplates', templates)
            } catch (e) {
                toast.warning('Не удалось получить список шаблонов.')
            }

            return state.templates
        },

    },
    namespaced: true
}