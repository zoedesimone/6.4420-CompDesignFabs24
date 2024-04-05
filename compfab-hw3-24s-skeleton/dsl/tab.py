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

        def normalize_vector(v):
            """
            Normalizes a 2D vector v = (x, y) to have a length of 1.

            Parameters:
            v (np.ndarray): A numpy array representing the 2D vector.

            Returns:
            np.ndarray: The normalized 2D vector.
            """
            norm = np.linalg.norm(v)
            if norm == 0:
                # Return the original vector if it's the zero vector to avoid division by zero
                return v
            return v / norm
        
        width_omega_shift = np.sin(math.radians(self.omega)) * self.height
        height_omega_shift = np.cos(math.radians(self.omega)) * self.height

        if self.parent is None:
            # If the object is the parent itself:
            V1 = np.array([0, 0])  # top left
            V2 = np.array([0 + width_omega_shift, -self.height])  # bottom left
            V3 = np.array([self.width + width_omega_shift, -self.height])  # bottom right
            V4 = np.array([self.width, 0])  # top right
        else:
            # Compute parent's corners to position this object
            P1, P2, P3, P4 = self.parent.compute_corner_points()

            # Choosing reference points based on the side to attach to
            if self.side == Side.BOTTOM:  # Attach to bottom of parent
                reference_point = P2
                direction_vector = normalize_vector(np.array([P3[0]-P2[0], P3[1]-P2[1]]))  # Rightward: P2 to P3
                
            elif self.side == Side.LEFT:  # Attach to left of parent
                reference_point = P1
                direction_vector = normalize_vector(np.array([P2[0]-P1[0], P2[1]-P1[1]]))  # Downward: P1 to P2

            elif self.side == Side.RIGHT:  # Attach to right of parent
                reference_point = P3
                direction_vector = normalize_vector(np.array([P4[0]-P3[0], P4[1]-P3[1]]))  # Upward

            else:  # Side.TOP or any other case, attach to top of parent
                reference_point = P4
                direction_vector = normalize_vector(np.array([P1[0]-P4[0], P1[1]-P4[1]]))  # Leftward

            # Adjusting for offset and alignment
            shift_vector = direction_vector * self.offset
            
            x_shift = width_omega_shift* direction_vector #The shift in the x direction should be along the direction vector
            normal_to_direction_vector = normalize_vector(np.array([direction_vector[1], -direction_vector[0]]))
            y_shift = height_omega_shift* normal_to_direction_vector #The shift in the y direction should be along the normal to the direction vector
            rotated_vector = x_shift +y_shift #np.array([width_omega_shift, -height_omega_shift])
            # Calculating new points
            V1 = reference_point + shift_vector
            V2 = V1 + rotated_vector
            rotated_width_vector = self.width*direction_vector 
            V3 = V2 + rotated_width_vector
            V4 = V1 + rotated_width_vector

        return V1, V2, V3, V4


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
