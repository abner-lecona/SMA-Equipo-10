"""
El problema simula un entorno donde aspiradoras deben limpiar una habitación 
que contiene celdas sucias. Las aspiradoras se mueven por la habitación y aspiran 
la suciedad en las celdas hasta limpiarlas todas.

Autores: Abner Maximiliano Lecona Nieves | A01753179 & Joahan Javier García Fernández | A01748222

Fecha de creacion: 10/11/2023
"""

import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class TrashAgent(Agent):
    # Se crea la nueva insta
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # La celda no esta marcada para se removida
        self.marked_for_removal = False

    def mark_for_removal(self):
        # La celda ya esta marca para ser removida
        self.marked_for_removal = True

    def step(self):
        # No hace nada la celda sucia, solo esta ahi
        pass


class VacuumAgent(Agent):
    def __init__(self, unique_id, model):
        # Se crea la aspiradora en el lugar (1,1)
        super().__init__(unique_id, model)
        self.pos = (1, 1)

    def move(self):
        # Se guardan los vecinos de las 8 celdas
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        # Se escoge a donde se quier ir el agente
        new_position = random.choice(possible_steps)
        # El agente se mueve hacia ese lugar
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Cuando el agente esta en una celda, se guardan los agentes que ya esten en esta
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        # Se almacena la celda sucia para despues limpiarla
        dirty_cells = [agent for agent in this_cell if isinstance(agent, TrashAgent)]
        for dirty_cell in dirty_cells:
            dirty_cell.mark_for_removal()
        # El agente Vacuum aspira si encontro un agente Trash, y se mueve
        self.move()


class VacuumModel(Model):
    def __init__(self, N, M, num_agents, dirty_percent, max_steps):
        super().__init__()
        self.current_id = 0
        self.num_agents = num_agents
        self.grid = MultiGrid(N, M, False)
        self.schedule = RandomActivation(self)
        self.max_steps = max_steps
        self.step_count = 0

        # Crear agentes aspiradora
        for i in range(self.num_agents):
            a = VacuumAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        # Crear celdas sucias
        dirty_cells = random.sample(
            list(self.grid.coord_iter()), int(dirty_percent * N * M)
        )
        for i, cell in enumerate(
            dirty_cells, start=self.num_agents
        ):  # Iniciar IDs únicos desde num_agents
            x, y = cell[1]  # Acceder a las coordenadas como una tupla
            a = TrashAgent(i, self)
            self.schedule.add(a)  # Agregar TrashAgent al schedule
            self.grid.place_agent(a, (x, y))

    def remove_marked_agents(self):
        # Eliminar agentes marcados para eliminación
        marked_agents = [
            agent
            for agent in self.schedule.agents
            if isinstance(agent, TrashAgent) and agent.marked_for_removal
        ]
        # Eliminar agentes marcados de la schedule y la grid
        for agent in marked_agents:
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)

    def print_stats(self):
        # Imprimir estadísticas sobre el estado del modelo
        clean_cells_percentage = (
            self.schedule.get_agent_count() / (self.grid.width * self.grid.height) * 100
        )
        num_movements = self.schedule.steps * self.num_agents

        print(f"Step: {self.schedule.steps}")
        print(f"Percentage of clean cells: {clean_cells_percentage}%")
        print(f"Number of movements: {num_movements}")
        print()

    def step(self):
        dirty_cells = sum(
            isinstance(agent, TrashAgent) for agent in self.schedule.agents
        )
        print(dirty_cells)
        # Verificar si el número de celdas sucias es diferente de cero y si no se ha alcanzado el máximo de pasos
        if self.step_count < self.max_steps and dirty_cells != 0:
            self.schedule.step()
            self.remove_marked_agents()
            self.print_stats()
            self.step_count += 1  # Añadir esta línea
