from __future__ import annotations

from typing import Union

import fuzzywuzzy.process


ShapedRecipe = tuple[Union[str, None], Union[str, None], Union[str, None],
                     Union[str, None], Union[str, None], Union[str, None],
                     Union[str, None], Union[str, None], Union[str, None]]
ShapelessRecipe = list[str]
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

    def to_json(self) -> dict:
        return {
            "recipe": self.recipe,
            "shaped": self.shaped
        }

    @classmethod
    def from_json(cls, json: dict) -> EMCRecipe:
        return cls(json["recipe"], json["shaped"])


class EMCItem:
    def __init__(self, name: str, *, value: int = None, recipe: Recipe = None):
        self.name = name
        self._raw_value = value
        self._recipe = recipe

    @property
    def value(self):
        if self._raw_value:
            return self._raw_value
        else:
            return None

    @property
    def composite(self):
        return self._recipe is not None

    def to_json(self) -> dict:
        return {"name": self.name, "value": self._raw_value, "recipe": self._recipe.to_json() if self._recipe else None}

    @classmethod
    def from_json(cls, json: dict):
        return cls(json["name"], value=json["value"], recipe=EMCRecipe.from_json(json["recipe"]))


class EMCSystem:
    def __init__(self, name: str, items: list[EMCItem] = []):
        self._items = items

    def add_item(self, item: EMCItem):
        self._items.append(item)

    def add_items(self, items: list[EMCItem]):
        for item in items:
            self.add_item(item)

    def remove_item(self, name: str):
        i = next((i for i in self._items if i.name == name), None)
        if i:
            self._items.remove(i)

    def get_item(self, name: str):
        return next((i for i in self._items if i.name == name), None)

    def search(self, name: str) -> Union[EMCItem, None]:
        i = self.get_item(name)
        if i:
            return i
        else:
            search_item = fuzzywuzzy.process.extractOne(name, [i.name for i in self._items])[0]
            if search_item:
                return self.get_item(search_item)
            else:
                return None

    def calculate_value(self, name: Union[str, None]) -> int:
        if name is None:
            return 0
        item = self.get_item(name)
        if item.composite:
            recipe = [self.get_item(i) for i in item._recipe.recipe if i is not None]
            return sum([self.calculate_value(i.name) for i in recipe])
        else:
            return item.value

    def to_json(self):
        return {"name": self.name, "items": [i.to_json() for i in self._items]}

    @classmethod
    def from_json(cls, json: dict):
        return cls(json["name"], items=[EMCItem.from_json(i) for i in json["items"]])


class EMCDB:
    def __init__(self, systems: dict[str, EMCSystem] = {}):
        self._systems = systems
