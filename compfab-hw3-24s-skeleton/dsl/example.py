# An example script to use your DSL and compile to an SVG

from tab import Tab, generate_root_tab, generate_child_tab, draw_svg
from tab import Side

root = generate_root_tab(children = [],width = 13, height = 17, omega = 0)
child1 = generate_child_tab(parent = root, children = [], width = 12,height = 8, offset = 1, omega = 20, alpha = 50, side = Side.LEFT)
root.children.append(child1)
child2 = generate_child_tab(parent = root, children = [], width = 5,height = 6, offset = 2, omega = 20, alpha = 50,side = Side.RIGHT)
root.children.append(child2)
child3 = generate_child_tab(parent = child2, children = [], width = 4,height = 3, offset = 0, omega = 0, alpha = 50,side = Side.TOP)
child2.children.append(child3)
draw_svg(root, "example.svg")