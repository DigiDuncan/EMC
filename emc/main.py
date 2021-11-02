from emc.console import console
from emc.lib.objects import EMCItem, EMCRecipe, EMCSystem


def do_the_thing():
    system = EMCSystem("system")
    names = ("cobblestone", "compressed cobblestone", "double compressed cobblestone")
    items = [
        EMCItem("cobblestone", value = 1),
        EMCItem("compressed cobblestone", recipe = EMCRecipe(["cobblestone"] * 9)),
        EMCItem("double compressed cobblestone", recipe = EMCRecipe(["compressed cobblestone"] * 9))
    ]
    system.add_items(items)
    return [system.calculate_value(name) for name in names]


def main():
    console.width = 80
    console.clear()
    for i in do_the_thing():
        console.print(i)


if __name__ == "__main__":
    main()
