from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    uuid = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default=None)
    short_description = Column(String, default=None)
    recipe_text = Column(String, default=None)
    profit = Column(Float, default=2.5)
    is_trade = Column(Boolean, default=False)
    layers = relationship("Layer", back_populates="recipes")
    files = relationship("File", back_populates="recipe")


class Layer(Base):
    __tablename__ = "layer"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    diameter = Column(Float, nullable=True)
    is_template = Column(Boolean, default=False)
    uuid_recipe = Column(Integer, ForeignKey("recipe.uuid", ondelete="CASCADE"), nullable=True)

    ingredients = relationship("ConsistencyIngredient", back_populates="layer")
    recipes = relationship("Recipe", back_populates="layers")


class Measure(Base):
    __tablename__ = "measure"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Ingredient(Base):
    __tablename__ = "ingredient"

    uuid = Column(Integer, primary_key=True, index=True)
    uuid_measure = Column(Integer, ForeignKey("measure.uuid"))
    name = Column(String)
    price = Column(Float)
    packing = Column(Float)

    measure = relationship("Measure", backref="ingredient", uselist=False)
    consistency = relationship("ConsistencyIngredient", back_populates="ingredient")


class ConsistencyIngredient(Base):
    __tablename__ = "consistency_ingredient"

    uuid = Column(Integer, primary_key=True, index=True)
    uuid_layer = Column(Integer, ForeignKey("layer.uuid", ondelete="CASCADE"))
    uuid_ingredient = Column(Integer, ForeignKey("ingredient.uuid"))
    quantity = Column(Float)

    ingredient = relationship("Ingredient", back_populates="consistency", uselist=False)
    layer = relationship("Layer", back_populates="ingredients")
