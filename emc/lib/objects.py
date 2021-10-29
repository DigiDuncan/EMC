from __future__ import annotations

from typing import Union

import fuzzywuzzy


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

    @property
    def value(self) -> int:
        value = 0
        for item in self.recipe:
            if item is not None:
                value += item.value
        return value


class EMCItem:
    def __init__(self, name: str, *, value: int = None, recipe: Recipe = None):
        self.name = name
        self._raw_value = value
        self._recipe = recipe

    @property
    def value(self):
        if self._raw_value:
            return self._raw_value
        elif self._recipe:
            return self._recipe.value


class EMCSystem:
    def __init__(self, name: str, items: list[EMCItem] = []):
        self._items = items

    def add_item(self, item: EMCItem):
        self._items.append(item)

    def get_item(self, name: str):
        for item in self._items:
            if item.name == name:
                return item
        return None

    def search(self, name: str):
        names = [i.name for i in self._items]



class EMCDB:
    def __init__(self, systems: dict[str, EMCSystem] = {}):
        self._systems = systems
