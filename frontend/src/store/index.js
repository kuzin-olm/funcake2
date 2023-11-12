import {createStore} from 'vuex'
import {measure} from "@/store/modules/measure";
import {ingredient} from "@/store/modules/ingredient";
import {recipe} from "@/store/modules/recipe";
import {auth} from "@/store/modules/auth";
import {templateLayer} from "@/store/modules/templateLayer";

export default createStore({
    state: {
        isAuth: false,
        token: null,
        nickname: '',
        isAdmin: false,

        isAlert: false,
        errMsg: '',
    },
    getters: {},
    mutations: {},
    actions: {},
    modules: {
        auth: auth,
        measure: measure,
        ingredient: ingredient,
        recipe: recipe,
        templateLayer: templateLayer,
    }
})
