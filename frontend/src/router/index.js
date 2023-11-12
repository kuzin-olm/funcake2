import { createRouter, createWebHistory } from 'vue-router'
import Main from "@/pages/Main";
import ListCakes from "@/pages/ListCakes";
import CreateCake from "@/pages/CreateCake";
import ListIngredient from "@/pages/ListIngredient";
import Authorization from "@/pages/Authorization";
import DetailCake from "@/pages/DetailCake";
import TemplateGroup from "@/pages/TemplateGroup";

const routes = [
  {
    path: '/',
    name: 'home',
    component: Main,
  },
  {
    path: '/cakes',
    name: 'cakes',
    component: ListCakes,
  },
  {
    path: '/cakes/:uuid',
    name: 'detailCake',
    component: DetailCake
  },
  {
    path: '/ingredient',
    name: 'ingredient',
    component: ListIngredient
  },
  {
    path: '/template-group',
    name: 'template-group',
    component: TemplateGroup
  },
  {
    path: '/create',
    name: 'create',
    component: CreateCake
  },
  {
    path: '/create/:uuid',
    name: 'update',
    component: CreateCake
  },
  {
    path: '/auth',
    name: 'authorization',
    component: Authorization
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
