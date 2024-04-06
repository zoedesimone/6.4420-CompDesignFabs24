# An example script to use your DSL and compile to an SVG

from tab import Tab, generate_root_tab, generate_child_tab, draw_svg
from tab import Side

#10 TAB element
root = generate_root_tab(children = [],width = 40, height = 40, omega = 30)
child1 = generate_child_tab(parent = root, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
root.children.append(child1)
child2 = generate_child_tab(parent = child1, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child1.children.append(child2)
child3 = generate_child_tab(parent = child2, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child2.children.append(child3)
child4 = generate_child_tab(parent = child3, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child3.children.append(child4)
child5 = generate_child_tab(parent = child4, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child4.children.append(child5)
child6 = generate_child_tab(parent = child5, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child5.children.append(child6)

child7 = generate_child_tab(parent = root, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.LEFT)
root.children.append(child7)
child8 = generate_child_tab(parent = child7, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child7.children.append(child8)
child9 = generate_child_tab(parent = child8, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child8.children.append(child9)
child10 = generate_child_tab(parent = child9, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child9.children.append(child10)
child11 = generate_child_tab(parent = child10, children = [], width = 40,height = 40, offset = 0, omega =30, alpha = 0, side = Side.BOTTOM)
child10.children.append(child11)

draw_svg(root, "3_4.svg")