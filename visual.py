"""
El problema simula un entorno donde aspiradoras deben limpiar una habitación 
que contiene celdas sucias. Las aspiradoras se mueven por la habitación y aspiran 
la suciedad en las celdas hasta limpiarlas todas.

Autores: Abner Maximiliano Lecona Nieves - A01753179 & Joahan Javier García Fernández - A01748222

Fecha de creacion: 10/11/2023
"""

from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from logic import TrashAgent, VacuumAgent, VacuumModel


# Clase ModelData que define cómo se mostrarán los datos del modelo
class ModelData(TextElement):
    def render(self, model):
        # Cálculos de estadísticas sobre la limpieza de las celdas y el movimiento de agentes
        total_cells = model.grid.width * model.grid.height
        dirty_cells_count = sum(
            isinstance(agent, TrashAgent) for agent in model.schedule.agents
        )
        clean_cells_count = total_cells - dirty_cells_count
        clean_cells_percentage = round((clean_cells_count / total_cells) * 100, 1)

        num_room_agents = sum(
            1 for agent in model.schedule.agents if isinstance(agent, VacuumAgent)
        )
        num_movements = model.schedule.steps * num_room_agents

        return f"Step: {model.schedule.steps}<br>Percentage of clean cells: {clean_cells_percentage}%<br>Number of movements: {num_movements}"


# Función que define cómo se representarán los agentes en la visualización
def agent_portrayal(agent):
    if isinstance(agent, VacuumAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5,
        }
    elif isinstance(agent, TrashAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "brown",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5,
        }
    else:
        portrayal = (
            {}
        )  # No se representa nada para agentes que no son aspiradoras ni basura
    return portrayal


# Parámetros del modelo y configuración de la cuadrícula de visualización
width = 15
height = 15
num_agents = 700
dirty_percentage = 0.40
max_steps = 30

grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

# Instancia de ModelData que se utilizará para mostrar información del modelo
model_data = ModelData()

# Configuración del servidor modular de Mesa con el modelo, la cuadrícula y los datos del modelo
server = ModularServer(
    VacuumModel,
    [grid, model_data],
    "Room Model",
    {
        "N": width,
        "M": height,
        "num_agents": num_agents,
        "dirty_percent": dirty_percentage,
        "max_steps": max_steps,
    },
)
server.port = 8521

# Inicio del servidor
server.launch()
