from fastapi import APIRouter
from app.api_v1.endpoint import auth, ingredient, measure, recipe, template_layer


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(ingredient.router)
api_router.include_router(measure.router)
api_router.include_router(recipe.router)
api_router.include_router(template_layer.router)
