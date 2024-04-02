import numpy as np
from typing import Optional, Union
from dataclasses import dataclass
from functools import cache
import svgwrite
from svgwrite.shapes import Polygon
from pathlib import Path
import math
from enum import Enum

class Side(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"

@dataclass
class Tab:
    """
    A structure that represents a tab and a bend with respect to the parent tab.

    Hint: See figure 2 on some guidance to what parameters need to be put here.
    """

    parent: Optional["Tab"]
    children: list["Tab"]
    width : float # w in the diagram
    height :float # l in the diagram
    offset : Optional[float] #d in the diagram
    omega : float # planar angle off of the parent tab
    alpha : Optional[float] # 3D angle off of the parent tab
    side: Optional[Side]


    def __hash__(self):
        return id(self)

    @cache
    def compute_corner_points(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes the four corner points in 2D (2,) based on the attributes.

        Hint: You may want to specify the convention on how you order these points.
        Hint: You can call this function on the parent to help get started.
        """
        width_omega_shift = math.sin(self.omega)*self.height
        height_omega_shift = math.cos(self.omega)*self.height
        
        if self.parent == None:
            #If the tab is the parent tab:
            V1 = np.array([0, 0]) #top left
            V2 = np.array([0 + width_omega_shift,-self.height]) #bottom left
            V3 = np.array([self.width+ width_omega_shift,-self.height]) #bottom right
            V4 = np.array([self.width,0]) #top right
        else:
            parent_tab = self.parent
            P1,P2,P3,P4 = parent_tab.compute_corner_points() 
            #check which side the child is attaching to the parent

            #Edge case: in the case of LEFT and RIGHT we need to consider if the parent has an omega
            # in this case we need to take into account the shifts based on that angle
            parent_omega = parent_tab.omega

            if self.side == Side.BOTTOM:# P2, the lower left point is the reference
                P2_x = P2[0]
                P2_y = P2[1]
                V1 = np.array([P2_x+self.offset, P2_y])  
                V2 = np.array([P2_x+self.offset + width_omega_shift, P2_y - height_omega_shift]) 
                V3 = np.array([P2_x+self.offset + width_omega_shift + self.width, P2_y - height_omega_shift]) 
                V4 = np.array([P2_x+self.offset + self.width, P2_y]) 

            elif self.side == Side.LEFT:
                P1_x = P1[0]
                P1_y = P1[1]
                V1 = np.array([P1_x, P1_y - self.offset])
                V2 = np.array([P1_x - height_omega_shift, P1_y - width_omega_shift - self.offset ])
                V3 = np.array([P1_x - height_omega_shift, P1_y - self.width - width_omega_shift - self.offset ])
                V4 = np.array([P1_x, P1_y - self.offset - self.width])
            
            elif self.side == Side.RIGHT:
                P3_x = P3[0]
                P3_y = P3[1]
                V1 = np.array([P3_x, P3_y +self.offset])
                V2 = np.array([P3_x +height_omega_shift, P3_y +self.offset +width_omega_shift])
                V3 = np.array([P3_x + height_omega_shift, P3_y + self.offset + self.width +width_omega_shift])
                V4 = np.array([P3_x, P3_y +self.offset +self.width])

            else: #Side.TOP
                P4_x = P4[0]
                P4_y = P4[1]
                V1 = np.array([P4_x - self.offset, P4_y])
                V2 = np.array([P4_x - self.offset - width_omega_shift, P4_y +height_omega_shift])
                V3 = np.array([P4_x - self.offset - self.width - width_omega_shift, P4_y + height_omega_shift])
                V4 = np.array([P4_x - self.offset - self.width, P4_y])

        
        return (V1,V2,V3,V4)


    def compute_all_corner_points(self) -> list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
        """
        Computes all four corner points of all tabs in the current subtree.
        """
        cps = [self.compute_corner_points()]
        for child in self.children:
            cps.extend(child.compute_all_corner_points())
        return cps


def generate_root_tab(children: list[Tab], width : float, height :float, omega : float) -> Tab:
    """
    Generate a new parent tab
    """
    # TODO: 3.2: Update the arguments and implement this function.
    return Tab(parent = None, children = children, width=width,height=height, offset= None, omega=omega, alpha = None, side = None)
    


def generate_child_tab(parent: Tab,children: list[Tab], width : float, height :float, offset : float, omega : float, alpha : float, side: Side) -> Tab:
    """
    Generate a child tab. Make sure to update the children of parent accordingly.
    """
    # TODO: 3.2: Update the arguments and implement this function.
    return Tab(parent, children,width,height, offset, omega, alpha, side )


def draw_svg(root_tab: Tab, output: Union[str, Path], stroke_width: float = 1):
    cps = root_tab.compute_all_corner_points()
    points = np.array(cps).reshape(-1, 2)
    min_point = points.min(axis=0)  # (2,)
    max_point = points.max(axis=0)  # (2,)
    points -= min_point
    points += 2 * stroke_width
    size = max_point - min_point  # (2,)
    size += 4 * stroke_width
    rects = points.reshape(-1, 4, 2)

    dwg = svgwrite.Drawing(str(output), size=(size[0], size[1]), profile="tiny")

    for rect in rects:
        dwg.add(Polygon(rect, stroke="black", fill="lightgray", stroke_width=stroke_width))

    dwg.save()
