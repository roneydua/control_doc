#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   coordinate_system.py
@Time    :   2025/08/12 09:45:21
@Author  :   Roney D Silva
@Contact :   roneyddasilva@gmail.com,
@Desc    :   A brief description of the file's purpose.
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.style.use("eahc.mplstyle")

my_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

fin = {"c":2.0,"b":1.5,"alpha":np.deg2rad(30)}
stage_s31 = {"radius": 2.5, "height": 3}
stage_s30 = {"radius": stage_s31["radius"], "height": 4}
FIG_L = 6.29
FIG_A = 11/9 * FIG_L


def draw_coordinate_system(ax, position, attitude, length=1.0,color='black',system="", draw_labels='xyz'):
    """
    Draws a 3D coordinate system.

    Parameters:
    - ax: Matplotlib 3D axis object.
    - position: A 3-element list or numpy array representing the origin of the coordinate system.
    - attitude: A 3x3 rotation matrix (numpy array) representing the orientation.
    - length: The length of the axes.
    """
    # Define the standard basis vectors
    x_axis = np.array([length, 0, 0])
    y_axis = np.array([0, length, 0])
    z_axis = np.array([0, 0, length])

    # Rotate the axes according to the attitude matrix
    x_axis_rotated = attitude.dot(x_axis)
    y_axis_rotated = attitude.dot(y_axis)
    z_axis_rotated = attitude.dot(z_axis)
    print(r"$\mathbf{x}_{" + system + "}$"+"\t",r"$\mathbf{y}_{"+system+"}$",r"$\mathbf{z}_{"+system+"}$")
    # Draw the axes using quiver
    if 'x' in draw_labels:
        ax.quiver(*position, *x_axis_rotated, color=color)
        ax.text(*(position + x_axis_rotated), r"$\mathbf{x}_{"+system+"}$", color=color)
    if 'y' in draw_labels:
        ax.quiver(*position, *y_axis_rotated, color=color)
        ax.text(*(position + y_axis_rotated), r"$\mathbf{y}_{"+system+"}$", color=color)
    if 'z' in draw_labels:
        ax.quiver(*position, *z_axis_rotated, color=color)

        ax.text(*(position + z_axis_rotated), r"$\mathbf{z}_{"+system+"}$", color=color)


def draw_cylinder(ax, position, attitude, radius, height, color="cyan", alpha=0.5, stage_name=""):
    """
    Draws a cylinder in a 3D plot.

    Parameters:
    - ax: Matplotlib 3D axis object.
    - position: A 3-element list or numpy array for the cylinder's base center.
    - attitude: A 3x3 rotation matrix (numpy array) for the cylinder's orientation.
    - radius: The radius of the cylinder.
    - height: The height of the cylinder.
    - color: The color of the cylinder.
    """
    # Create the points for the cylinder sides
    u = np.linspace(0, 2 *np.pi, 50)  # Azimuthal angle
    v = np.linspace(0, height, 2)  # Height
    u, v = np.meshgrid(u, v)

    x = -v
    y = radius * np.sin(u)
    z = radius * np.cos(u)

    # Stack the coordinates for easier rotation
    points = np.stack([x.flatten(), y.flatten(), z.flatten()])

    # Rotate and translate the points
    rotated_points = attitude.dot(points)
    translated_points = rotated_points + np.array(position).reshape(3, 1)

    # Reshape for plotting
    x_t = translated_points[0, :].reshape(x.shape)
    y_t = translated_points[1, :].reshape(y.shape)
    z_t = translated_points[2, :].reshape(z.shape)

    # Plot the cylinder surface
    ax.plot_surface(x_t, y_t, z_t, color=color, alpha=alpha,label=stage_name)
    ax.legend()
    # # Create and plot the bottom and top caps
    # for h in [0, height]:
    #     cap_z = np.full(u[0].shape, h)
    #     cap_points = np.stack([x[0], y[0], cap_z])
    #     rotated_cap = attitude.dot(cap_points)
    #     translated_cap = rotated_cap + np.array(position).reshape(3, 1)

    # ax.plot(translated_cap[0], translated_cap[1], translated_cap[2], color="black")

def draw_triangle(ax, r, attitude, color='yellow', alpha=0.7):
    """
    Draws a 3D triangle.

    Parameters:
    - ax: Matplotlib 3D axis object.
    - vertices: A list of three 3-element lists or numpy arrays representing the triangle's vertices.
    - color: The color of the triangle.
    - alpha: The transparency of the triangle (0 to 1).
    """
    p1 = np.array(r)
    p2 = p1 + attitude @ np.array([-fin["c"], 0, 0])
    p3 = p1 + attitude @ np.array([-fin["c"], fin["b"], 0])
    p2_rotated = p2
    p3_rotated = p3
    vertices = np.array([p1, p2_rotated, p3_rotated])
    triangle = Poly3DCollection([vertices], color=color, alpha=alpha)
    ax.add_collection3d(triangle)


def draw_vector(ax, start_point, end_point, vector_name, color="black",y_offset=0):
    """
    Draws a 3D vector and adds a label parallel to it.

    Parameters:
    - ax: Matplotlib 3D axis object.
    - start_point: A 3-element list or numpy array for the vector's starting point.
    - end_point: A 3-element list or numpy array for the vector's ending point.
    - vector_name: The text label for the vector.
    - color: The color of the vector and label.
    """
    vector = np.array(end_point) - np.array(start_point)

    ax.quiver(
        *start_point,
        *vector,
        color=color,
        arrow_length_ratio=0.1,
        label=vector_name,
    )
    ax.legend()
    # Calculate the midpoint of the vector for label placement
    mid_point = (np.array(start_point) + np.array(end_point)) / 2

    # 1. Calculate a slightly larger offset
    offset_magnitude = 0
    if np.linalg.norm(vector) > 0:
        offset = offset_magnitude * vector / np.linalg.norm(vector)
    else:
        offset = np.array([offset_magnitude, offset_magnitude, offset_magnitude])

    text_position = mid_point + offset
    text_position += np.array([0, y_offset, 0])  # Slightly above the vector for better visibility
    # ax.text(
    #     *text_position,
    #     vector_name,
    #     color=color,
    #     ha="center",
    #     va="center",
    #     # bbox=dict(
    #         # facecolor="black", alpha=1, edgecolor="none", pad=1.5
    #     # )  # Background box
    # )


if __name__ == "__main__":
    if plt.fignum_exists("atmos"):
        ax.clear()
    else:
        fig = plt.figure(figsize=(FIG_L, FIG_A),num="atmos")
        ax = fig.add_subplot(111, projection="3d")
    # ax.axis('off')

    ax.set_aspect("equal")
    # --- Draw the main coordinate system at the origin ---
    origin_position = [0, 0, 0]

    # --- Define parameters for the cylinder and its coordinate system ---
    stage_1_position = [0, 0, 0]

    rotation_angles_deg = [0, 0, 0]
    rotation = R.from_euler("zyx", rotation_angles_deg, degrees=True)
    stage_1_attitude = rotation.as_matrix()

    # --- Draw the cylinder and its local coordinate system ---
    draw_coordinate_system(ax, stage_1_position, stage_1_attitude, length=2,system=r"\mathrm{v}", color=my_colors[0],draw_labels='xyz')
    cg_position = [(-(stage_s31["height"]+2.0*stage_s30["height"])/2.),0,0]
    ## Draw top stage
    draw_coordinate_system( ax, cg_position, stage_1_attitude, length=1., system=r"\mathrm{b}", color=my_colors[1], draw_labels='yz')
    draw_cylinder(
        ax,
        stage_1_position,
        stage_1_attitude,
        stage_s30["radius"],
        stage_s30["height"],
        color=my_colors[0],
        alpha=.25,
        stage_name="S30 (top)"
    )
    ## draw stage 2
    stage_2_position = [-stage_s30["height"], 0, 0]
    # draw_coordinate_system(ax, stage_2_position, stage_1_attitude, length=2.5)
    draw_cylinder(
        ax,
        stage_2_position,
        stage_1_attitude,
        stage_s30["radius"],
        stage_s30["height"],
        color=my_colors[1],
        alpha=0.1,
        stage_name="S30 (middle)",
    )

    ## draw stage 3
    stage_3_position = [-stage_s30["height"]*2, 0, 0]
    # draw_coordinate_system(ax, stage_3_position, stage_1_attitude, length=2.5)
    draw_cylinder(
        ax,
        stage_3_position,
        stage_1_attitude,
        stage_s31["radius"],
        stage_s31["height"],
        color=my_colors[2],
        alpha=0.1,
        stage_name="S31 (bottom)",
    )

    # # --- Define the vertices of the triangle ---
    fin1_position = [
        -(stage_s30["height"] * 2 + stage_s31["height"] - fin["c"]),
        stage_s30["radius"],
        0,
    ]  
    rotation_angles_deg = [0, 0, 0]
    rotation = R.from_euler("zyx", rotation_angles_deg, degrees=True)
    # # --- Draw the triangle left---
    draw_triangle(ax, fin1_position, rotation.as_matrix(), color=my_colors[0], alpha=0.7)

    fin2_position = [
        -(stage_s30["height"] * 2 + stage_s31["height"] - fin["c"]),
        -stage_s30["radius"],
        0,
    ]  
    rotation_angles_deg = [0, 0, 180]
    rotation = R.from_euler("zyx", rotation_angles_deg, degrees=True)
    # --- Draw the triangle ---
    draw_triangle(ax, fin2_position, rotation.as_matrix(), color=my_colors[0], alpha=0.7)

    # vectors
    vector_start_1 = [0, 0, 0]
    vector_end_1 = [cg_position[0], 0, 0]
    vector_name_str_1 = r"$\mathbf{c}_{\mathrm{b}}^{v}$ (CG position wrt. vehicle reference)" # Another way to denote a vector

    # --- Draw the second vector ---
    draw_vector(ax, vector_start_1, vector_end_1, vector_name_str_1, color=my_colors[2],y_offset=-.2)
    # draw coordinate system for the surface
    draw_coordinate_system(ax=ax, position=fin1_position, attitude=np.eye(3), length=2, system=r"\mathcal{S}", color=my_colors[4], draw_labels='yz')
    draw_vector(
        ax,
        cg_position,
        fin1_position,
        # {\boldsymbol{\varsigma}}_{\mathcal{S}}^{b}""
        r"${\boldsymbol{\varsigma}}_{\mathcal{S}}^{\mathrm{b}}$ (surface position wrt. CG position)",
        color=my_colors[3],
        y_offset=-0.2,
    )
    draw_vector(
        ax,
        [0, 0, 0],
        fin1_position,
        r"${\boldsymbol{\varrho}}^{\mathrm{v}}_{\mathcal{S}}$ (surface position wrt. vehicle reference)",
        color=my_colors[5],
        y_offset=0.2,
    )
    # --- Plot settings ---
    # ax.view_init(elev=-80, azim=-140,roll=180)  # Set the viewing angle
    ax.view_init(elev=-45, azim=60, roll=-170)    # Set axis limits to ensure all objects are visible
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.legend(ncols=2, fontsize=10, loc="upper center")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.savefig(
        "images/coordinate_system_on_body.pdf",
        bbox_inches="tight",
        # pad_inches=-0.4,
        transparent=True,
    )
    # plt.show()
    plt.close(fig="all")
