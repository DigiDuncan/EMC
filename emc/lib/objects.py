from __future__ import annotations

from typing import Union


ShapedRecipe = tuple[Union["EMCItem", None], Union["EMCItem", None], Union["EMCItem", None],
                     Union["EMCItem", None], Union["EMCItem", None], Union["EMCItem", None],
                     Union["EMCItem", None], Union["EMCItem", None], Union["EMCItem", None]]
ShapelessRecipe = list["EMCItem"]
Recipe = Union[ShapedRecipe, ShapelessRecipe]


class EMCRecipe:
    def __init__(self, recipe: Recipe, shaped = False) -> None:
        # Validation
        if shaped:
            if len(recipe) != 9:
                raise ValueError("Recipe is marked shaped but is not length 9.")
        else:
            if len(recipe) > 9:
                raise ValueError("Recipe must be 9 items or less.")

        # Store variables
        self.recipe = recipe
        self.shaped = shaped


class EMCItem:
    def __init__(self, name: str, value_or_recipe: Union[int, EMCRecipe]):
        self.name = name
        self._raw_value = None
        self._recipe = None

        if isinstance(value_or_recipe, int):
            self._raw_value = value_or_recipe
        elif isinstance(value_or_recipe, EMCRecipe):
            self._recipe = value_or_recipe

    @property
    def value(self):
        if self._raw_value:
            return self._raw_value
        elif self._recipe:
            recipe = [i for i in self._recipe if i is not None]
            return sum([i.value for i in recipe])


class EMCSystem:
    def __init__(self, name: str, items: list[EMCItem] = []):
        self._items = items


class EMCDB:
    def __init__(self, systems: dict[str, EMCSystem] = {}):
        self._systems = systems
