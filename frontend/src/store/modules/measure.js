import API from '@/plugins/axios'
import {useToast} from "vue-toastification";

const toast = useToast()

export const measure = {
    state: () => ({
        measureCatalog: [],
    }),
    getters: {},
    mutations: {
        setMeasure(state, measures) {
            state.measureCatalog = measures;
        },
    },
    actions: {
        async fetchMeasure({state, commit}) {
            try {
                const response = await API.get('measure');
                let measures = [];

                if (response.status === 200) {
                    response.data.forEach(measure => {
                        measures.push(
                            {
                                value: measure.uuid,
                                name: measure.name,
                            }
                        )
                    })
                }

                commit('setMeasure', measures)
            } catch (e) {
                toast.warning('Не удалось получить каталог ед. измерений.')
            }
        },
    },
    namespaced: true
}