import API from '@/plugins/axios'
import {useToast} from "vue-toastification";
import parsErrorAnswer from "@/plugins/answerParser";

const toast = useToast()

export const auth = {
    state: () => ({}),
    getters: {},
    mutations: {
        setAuth(state, newState) {
            this.state.isAuth = newState
        },
        setToken(state, token) {
            this.state.token = token
        },
        setNickname(state, nickname) {
            this.state.nickname = nickname
        },
        setAdmin(state, status) {
            this.state.isAdmin = status
        },
    },
    actions: {
        async registration({state, commit}, {login, password, confirmPassword}) {
            if (password !== confirmPassword) {
                toast.error('Не совпадают пароли.')
                return false
            }

            let body = new FormData();
            body.append('user', JSON.stringify({
                'nickname': login,
                'password1': password,
                'password2': confirmPassword
            }));
            try {
                const response = await API.post(
                    "auth/register",
                    body,
                    {headers: {"Content-Type": "multipart/form-data"}}
                )

                if (response.status === 201) {
                    toast.success('Пользователь создан.')
                    return true
                }
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
            }
            return false
        },
        async authenticate({state, commit}, {login, password}) {
            let body = new FormData();
            body.append('user', JSON.stringify({
                'nickname': login,
                'password': password
            }));

            try {
                const response = await API.post(
                    "auth/login",
                    body,
                    {headers: {"Content-Type": "multipart/form-data"}}
                )

                if (response.status === 200) {
                    const token = response.data.accessToken
                    API.defaults.headers['Authorization'] = `Bearer ${token}`

                    const responseMe = await API.get("auth/me")
                    if (responseMe.status === 200) {
                        commit('setAuth', true)
                        commit('setToken', token)
                        commit('setNickname', responseMe.data.user)
                        commit('setAdmin', responseMe.data.isAdmin)
                        localStorage.setItem("JWT", token)
                    }
                    return true
                }
            } catch (e) {
                const err = parsErrorAnswer(e.response.data.detail)
                toast.error(err)
            }
            return false
        },
        async checkAuth({dispatch, state, commit}) {
            const token = localStorage.getItem('JWT')
            if (token) {
                API.defaults.headers['Authorization'] = `Bearer ${token}`
                try {
                    const response = await API.get('auth/me')
                    commit('setAuth', true)
                    commit('setToken', token)
                    commit('setNickname', response.data.user)
                    commit('setAdmin', response.data.isAdmin)
                } catch (e) {
                    dispatch('logout')
                }
            } else {
                dispatch('logout')
            }
        },
        logout({commit}) {
            localStorage.removeItem('JWT')
            API.defaults.headers['Authorization'] = ``
            commit('setAuth', false)
            commit('setToken', null)
            commit('setNickname', '')
            commit('setAdmin', false)
        }
    },
    namespaced: true
}