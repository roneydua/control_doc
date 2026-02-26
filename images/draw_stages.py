#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   draw_stages.py
@Time    :   2025/07/29 20:15:52
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
'''
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
plt.style.use('./eahc.mplstyle')
my_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Configuração dos parâmetros


params = {
    "bottom_height": 3.3,
    "middle_height": 3.2,
    "top_height": 3.2,
    "diameter": 0.56,
    "bottom_fuel": 3.3,
    "middle_fuel": 3.2,
    "top_fuel": 3.20*.5,
    "nose_height": 1.5
}
FIG_L = 6.29
FIG_A = (90.0) / 25.4


if plt.fignum_exists("rocket_schematic"):
    plt.close("rocket_schematic")  # Fecha a figura se já existir
# Criar figura e eixo
fig, ax = plt.subplots(figsize=(6, 10),num="rocket_schematic")
# Ajustar limites e layout
# ax.set_xlim(-.25, params["diameter"] + 1)
ax.set_ylim(-10, 3)
ax.set_aspect('equal')
ax.axis('off')  # Remover eixos
# Função para desenhar um sistema de coordenadas
def draw_coordinate_system(ax, x, y, label="", size=0.2, color="k",sizex=None):
    # Eixos X e Y
    if sizex is None:
        sizex = size
    ax.arrow(x, y, sizex, 0, head_width=0.05, head_length=0.05, fc=color, ec=color)
    ax.arrow(x, y, 0, -size, head_width=0.05, head_length=0.05, fc=color, ec=color)

    # Rótulos
    ax.text(x + sizex + 0.15, y, "y", ha="left", va="center", color=color)
    ax.text(x, y -(size + 0.25), "x", ha="center", va="bottom", color=color)

    # Ponto de origem
    ax.plot(x, y, "o", color=color, markersize=4)

    # Label do sistema
    if label:
        ax.text(x -0.1, y, label, ha="right", va="top", color=color)


# Desenhar sistemas de coordenadas principais
draw_coordinate_system(ax, x=-params["diameter"] , y=0, label="$\mathrm{b}$", size=0.25, color="black")
# Função para desenhar cotas dimensionais
def add_dimension(ax, x, y1, y2, text, offset=0.5, color="black"):
    # Linha de cota principal
    # ax.plot([x, x], [y1, y2], color=color, linestyle="--", alpha=0.7)
    ax.plot()
    # Seta inferior
    arrowA = FancyArrowPatch(
        (x - offset / 3, y1),
        (x - offset / 3, y2),
        arrowstyle="->",
        mutation_scale=10,
        color=color,
    )
    ax.add_patch(arrowA)
    # Texto da cota
    ax.text(
        x - offset / 3,
        (y1 + y2) / 2,
        text,
        ha="left",
        va="center",
        fontsize=14,
        color=color,
        rotation=90,  # Rotação em graus (90 = vertical)
        bbox=dict(facecolor="white", alpha=0.0, edgecolor="none"),
    )


# Função para desenhar um estágio com combustível
def draw_stage(ax, x, y, width, height, fuel_height, index, label=None):
    # Estrutura do estágio
    structure = Rectangle(
        (x, y),
        width,
        height,
        alpha=0.3,
        facecolor=my_colors[index],
        edgecolor=my_colors[index],
        lw=1.5,
    )
    ax.add_patch(structure)

    # Combustível (com transparência)
    fuel = Rectangle(
        (x, y),
        width,
        fuel_height,
        facecolor=my_colors[index],
        alpha=0.7,
        edgecolor=my_colors[index],
        lw=1,
    )
    ax.add_patch(fuel)

    # Sistema de coordenadas local do estágio
    local_origin_x = params["diameter"]
    local_origin_y = y #+ height / 2
    draw_coordinate_system(
        ax,
        local_origin_x+.1,
        local_origin_y,
        # label,
        size=0.5,
        sizex=2,
        color=my_colors[index],
    )

    # Adicionar cotas para o estágio e combustível
    stage_right = x + width
    add_dimension(
        ax,
        stage_right + 0.5,
        y,
        y + height/2,
        r"$\mathbf{c}_{s}$",
        offset=-1,
        color=my_colors[index],
    )

    add_dimension(
        ax,
        stage_right + 0.5,
        y,
        y + fuel_height / 2,
        r"$\mathbf{c}_{f}$",
        offset=-2.5,
        color=my_colors[index],
    )

    # # Detalhes decorativos (linhas)
    # for y_pos in np.linspace(y + 0.2, y + height - 0.2, 4):
    #     ax.plot([x + width, x + width + 0.2], [y_pos, y_pos], 'k-', lw=1)

    if label:
        ax.text(
            x + width / 2,
            y + height / 2,
            label,
            ha="center",
            va="center",
            rotation=90,
            fontweight="bold",
        )


# Desenhar os três estágios
draw_stage(
    ax,
    x=0,
    y=0,
    width=params["diameter"],
    height=-params["bottom_height"],
    fuel_height=-params["bottom_fuel"],
    label="VSB-30(2)",
    index=0
)

draw_stage(
    ax,
    x=0,
    y=-params["bottom_height"],
    width=params["diameter"],
    height=-params["middle_height"],
    fuel_height=-params["middle_fuel"],
    label="VSB-30(1)",
    index=1
)

draw_stage(
    ax,
    x=0,
    y=-(params["bottom_height"]+ params["middle_height"]),
    width=params["diameter"],
    height=-params["top_height"],
    fuel_height=-params["top_fuel"],
    label="VSB-31",
    index=2
)

# Desenhar o nariz (cone)
# nose_points = [
#     [0, params["bottom_height"] + params["middle_height"] + params["top_height"]],
#     [params["diameter"], params["bottom_height"] + params["middle_height"] + params["top_height"]],
#     [params["diameter"]/2, params["bottom_height"] + params["middle_height"] + params["top_height"] + params["nose_height"]]
# ]
# nose = Polygon(nose_points, facecolor=structure_color, edgecolor='black')
# ax.add_patch(nose)

# ax.set_ylim(-0.5, params["bottom_height"] + params["middle_height"] + params["top_height"] + params["nose_height"] + 0.5)
# plt.tight_layout()
plt.grid()
# Mostrar ou salvar
# plt.savefig("rocket_schematic.png", dpi=300, bbox_inches='tight')
plt.show()
