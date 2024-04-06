# An example script to use your DSL and compile to an SVG

from tab import Tab, generate_root_tab, generate_child_tab, draw_svg
from tab import Side

#CUBE
root = generate_root_tab(children = [],width = 4, height = 4, omega = 0)
child1 = generate_child_tab(parent = root, children = [], width = 4,height = 4, offset = 0, omega =0, alpha = 0, side = Side.BOTTOM)
root.children.append(child1)
child2 = generate_child_tab(parent = child1, children = [], width = 4,height = 4, offset = 0, omega =0, alpha = 0, side = Side.BOTTOM)
root.children.append(child2)
child3 = generate_child_tab(parent = child2, children = [], width = 4,height = 4, offset = 0, omega =0, alpha = 0, side = Side.BOTTOM)
root.children.append(child3)
child4 = generate_child_tab(parent = child1, children = [], width = 4,height = 4, offset = 0, omega =0, alpha = 0, side = Side.LEFT)
root.children.append(child4)
child5 = generate_child_tab(parent = child1, children = [], width = 4,height = 4, offset = 0, omega =0, alpha = 0, side = Side.RIGHT)
root.children.append(child5)

draw_svg(root, "cube.svg")