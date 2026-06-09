import numpy as np
import random
import copy

from Classes.Core.Object.TableGroup import TableGroup
from Classes.Objects.Static.Table import Table
from Classes.Objects.Static.Chair import Chair, ChairOrientation

# Fields status on obstacle_array
EMPTY = 0           #free field
OBSTACLE = 1        #setup obstacle
TABLE = 2           #table set during algorithm's iteration
CHAIR = 3           #chair set during algorithm's iteration
BUFFER = 4          #1 field of space between TableGroup objects, so the tables won't be next to each other

    # HEY THERE WANNA BUY SOME CHROMOSOMES?
    # https://wykop.pl/cdn/c3201142/comment_3IGscyiPzLD8iVhyW1keLqjo9Ew1BPiC.jpg

def get_chair_places(table_coordinates: list[tuple[int, int]], gridX: int, gridY: int) -> list[tuple[int, int]]:
    #Looking for free space around tables
    # - C C C - 
    # C T T T C
    # - C C C -         for example

    free_coordinates = set()

    for tile in table_coordinates:
        cX = tile[0]
        cY = tile[1]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d in directions:
            dX = d[0]
            dY = d[1]

            newX = cX + dX
            newY = cY + dY

            if newX >= 0 and newX < gridX and newY >= 0 and newY < gridY:              #Checking grid boundaries
                if(newX, newY) not in table_coordinates:                                #Checking if such coordinates don't exist already
                    free_coordinates.add((newX, newY))

    return list(free_coordinates)
    


def get_table_coordinates(x: int, y: int, size: int, rotation: int, grid_X: int, grid_Y: int):
    coordinates = []

    for i in range(0, size):
        if rotation == 0:
            newX = x + i
            newY = y
        else:
            newX = x
            newY = y + i

        if newX >= grid_X or newY >= grid_Y:                #checking is table isn't outside grid
            return None
        coordinates.append((newX, newY))

    return coordinates

def set_buffor_coordinates(current_grid: np.ndarray, table_coord: np.ndarray, chair_coord: np.ndarray):
    grid_Y, grid_X = current_grid.shape
    placed_elements = table_coord + chair_coord

    neighbors = (
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),(1,  0),
        (-1,  1), (0,  1), (1,  1))
    for pX, pY in placed_elements:
        for dX, dY in neighbors:
            nX = pX + dX
            nY = pY + dY

            if nX >= 0 and nX < grid_X and nY >= 0 and nY < grid_Y:
                if current_grid[nY, nX] == EMPTY:
                    current_grid[nY, nX] = BUFFER


def repair_chromosome(chromosome: list[dict], obstacle_array: np.ndarray) -> list[dict]:
    grid_Y, grid_X = obstacle_array.shape
    current_grid = obstacle_array.copy()

    for gene in chromosome:

        size = gene["table_size"]
        needed_chairs = gene["chair_number"]
        is_good_position = False

        if gene["x"] != -1 and gene["y"] != -1:         #if table already has some coordinates

            table_coord = get_table_coordinates(gene["x"], gene["y"], size, gene["table_rotation"], grid_X, grid_Y)

            if table_coord is not None:
                empty_area = True

                for cX, cY in table_coord:
                    if current_grid[cY, cX] != EMPTY:               #checking if the future coordinates of the table aren't occupied by any other object
                        empty_area = False
                        break
                if empty_area == True:
                    is_good_position = True

                    for cX, cY in table_coord:
                        current_grid[cY, cX] = TABLE                #putting table there  

                    chair_space = get_chair_places(table_coord, grid_X, grid_Y)            #generating a frid of possible free tiles
                    actually_free_chair_space = []

                    for tile in chair_space:                                    #checking if tile is actually free
                        aX = tile[0]
                        aY = tile[1]

                        if current_grid[aY, aX] == EMPTY:
                            actually_free_chair_space.append((aX, aY))
                    max_available_chair_number = min(needed_chairs, len(actually_free_chair_space))

                    placed_chairs = []
                    for i in range(0, max_available_chair_number):
                        placed_chairs.append(actually_free_chair_space[i])

                    for aX, aY in placed_chairs:
                        current_grid[aY, aX] = CHAIR 

                    set_buffor_coordinates(current_grid, chair_space, placed_chairs)


        if is_good_position == False:
            possible_positions = []

            for y in range(grid_Y):
                for x in range(grid_X):
                    for possible_rot in [0, 1]:
                        table_coord = get_table_coordinates(x, y, size, possible_rot, grid_X, grid_Y)

                        if table_coord is not None:
                            empty_area = True

                            for cX, cY in table_coord:
                                if current_grid[cY, cX] != EMPTY:               #checking if the future coordinates of the table aren't occupied by any other object
                                    empty_area = False
                                    break
                            if empty_area == True:
                                is_good_position = True

                            chair_space = get_chair_places(table_coord, grid_X, grid_Y)            #generating a frid of possible free tiles
                            actually_free_chair_space = []

                            possible_positions.append({
                                    "x": x, "y": y, "rot": possible_rot,
                                    "cells": table_coord,
                                    "free_slots": actually_free_chair_space,
                                    "slots_count": len(actually_free_chair_space)
                            })

            if possible_positions:
                random.shuffle(possible_positions)
                possible_positions.sort(key=lambda p: min(needed_chairs, p["slots_count"]), reverse=True)
                
                best_pos = possible_positions[0]
                gene["x"] = best_pos["x"]
                gene["y"] = best_pos["y"]
                gene["table_rotation"] = best_pos["rot"]
                
                for cX, cY in best_pos["cells"]:
                    current_grid[cY, cX] = TABLE
                    
                placed_chairs_count = min(needed_chairs, best_pos["slots_count"])
                placed_chairs = best_pos["free_slots"][:placed_chairs_count]
                
                for aX, aY in placed_chairs:
                    current_grid[aY, aX] = CHAIR
                
                set_buffor_coordinates(current_grid, best_pos["cells"], placed_chairs)
            else:
                gene["x"] = -1
                gene["y"] = -1

    return chromosome

def calculate_fitness(chromosome: list[dict], obstacle_array: np.ndarray):
    grid_Y, grid_X = obstacle_array.shape
    current_grid = obstacle_array.copy()
    score = 0

    for gene in chromosome:
        if gene["x"] == -1 or gene["y"] == -1:
            score -= 2000
            continue

        table_coord = get_table_coordinates(gene["x"], gene["y"], gene["table_size"], gene["table_rotation"], grid_X, grid_Y)
        if table_coord is None:
            score -= 1000
            continue

        collision = False
        for cX, cY in table_coord:
            if current_grid[cY, cX] != EMPTY:
                collision = True
                break

        if collision:
            score -= 1500
            continue

        for cX, cY in table_coord:
            current_grid[cY, cX] = TABLE
            score += 30 

        chair_space = get_chair_places(table_coord, grid_X, grid_Y)
        actually_free_chair_space = []
        for tile in chair_space:
            aX = tile[0]
            aY = tile[1]
            if current_grid[aY, aX] == EMPTY:
                actually_free_chair_space.append((aX, aY))

        needed_chairs = gene["chair_number"]
        placed_chairs_count = min(needed_chairs, len(actually_free_chair_space))
        
        score += placed_chairs_count * 20
        
        missing_chairs = needed_chairs - placed_chairs_count
        if missing_chairs > 0:
            score -= missing_chairs * 150

        placed_chairs = actually_free_chair_space[:placed_chairs_count]
        for aX, aY in placed_chairs:
            current_grid[aY, aX] = CHAIR
            
        set_buffor_coordinates(current_grid, table_coord, placed_chairs)

    return score






def create_population(population_size: int, groups_number: int, chairs: np.ndarray, tables: np.ndarray, obstacle_array: np.ndarray):
    population = []

    for i in range(0, population_size):
        chromosome = []
        random_chair_number = random.sample(list(chairs), len(chairs))      #setting random number of chairs from chairs: np.ndarray

        for j in range(groups_number):
            chromosome.append(
                {"table_size": tables[j], 
                 "chair_number": random_chair_number[j],
                 "x": -1, "y": -1,                                          #default position (-1, -1)
                 "table_rotation": 0})                                      #table not chair orientation can be vertical or horizontal, lubie placki
            
        chromosome = repair_chromosome(chromosome, obstacle_array)           #forcing algorithm to find some place, replacing that (-1, -1) from default position, and other starnge errors, like 2 tables in one position
        population.append(chromosome)
    return population


def genetic_algorithm(tables: np.ndarray, chairs: np.ndarray, obstacle_array: np.ndarray):
    population_size = 60        
    generations = 100
    elitism_count = 3                               #how many best results is copied to the next generation without any changes (najlepsze samce alpha)

    grid_Y, grid_X = obstacle_array.shape
    groups_number = len(tables)                     #how many groups to create

    population = create_population(population_size, groups_number, chairs, tables, obstacle_array)


    for _ in range(generations):
        fitnesses = [calculate_fitness(ind, obstacle_array) for ind in population]
        pop_fit = sorted(list(zip(population, fitnesses)), key=lambda item: item[1], reverse=True)
        
        new_population = []
        
        for i in range(elitism_count):
            new_population.append(copy.deepcopy(pop_fit[i][0]))

        while len(new_population) < population_size:
            candidates1 = random.sample(pop_fit, 4)
            parent1 = max(candidates1, key=lambda item: item[1])[0]
            
            candidates2 = random.sample(pop_fit, 4)
            parent2 = max(candidates2, key=lambda item: item[1])[0]

            child = []
            for i in range(groups_number):
                p_source = parent1 if random.random() < 0.5 else parent2
                child.append({
                    "table_size": parent1[i]["table_size"],
                    "chair_number": parent1[i]["chair_number"],
                    "x": p_source[i]["x"],
                    "y": p_source[i]["y"],
                    "table_rotation": p_source[i]["table_rotation"]
                })

            if random.random() < 0.35:
                g = random.randint(0, groups_number - 1)
                child[g]["x"] = random.randint(0, grid_X - 1)
                child[g]["y"] = random.randint(0, grid_Y - 1)
                child[g]["table_rotation"] = random.choice([0, 1])

            if random.random() < 0.25:
                g1, g2 = random.sample(range(groups_number), 2)
                child[g1]["chair_number"], child[g2]["chair_number"] = child[g2]["chair_number"], child[g1]["chair_number"]

            child = repair_chromosome(child, obstacle_array)
            new_population.append(child)

        population = new_population

    final_fitnesses = [calculate_fitness(ind, obstacle_array) for ind in population]
    best_idx = np.argmax(final_fitnesses)
    best = population[best_idx]

    final_grid = obstacle_array.copy()
    result_groups = []

    for i in range(groups_number):
        gene = best[i]
        if gene["x"] == -1 or gene["y"] == -1:
            continue

        table_coord = get_table_coordinates(gene["x"], gene["y"], gene["table_size"], gene["table_rotation"], grid_X, grid_Y)
        if table_coord is None:
            continue

        table_objs = []
        for cX, cY in table_coord:
            final_grid[cY, cX] = TABLE
            table_objs.append(Table(position=np.array([cX, cY]), render_order=2))

        chair_space = get_chair_places(table_coord, grid_X, grid_Y)
        actually_free_chair_space = []
        for tile in chair_space:
            aX = tile[0]
            aY = tile[1]
            if final_grid[aY, aX] == EMPTY:
                actually_free_chair_space.append((aX, aY))

        chair_objs = []
        placed_chairs = []
        placed_count = min(gene["chair_number"], len(actually_free_chair_space))
        
        for j in range(placed_count):
            cX, cY = actually_free_chair_space[j]
            final_grid[cY, cX] = CHAIR
            placed_chairs.append((cX, cY))
            
            if (cX + 1, cY) in table_coord:
                chosen_orientation = ChairOrientation.NORTHWEST
            elif (cX - 1, cY) in table_coord:
                chosen_orientation = ChairOrientation.SOUTHEAST
            elif (cX, cY + 1) in table_coord:
                chosen_orientation = ChairOrientation.NORTHEAST
            elif (cX, cY - 1) in table_coord:
                chosen_orientation = ChairOrientation.SOUTHWEST
            else:
                chosen_orientation = ChairOrientation.NORTHEAST

            chair_objs.append(Chair(position=np.array([cX, cY]), orientation=chosen_orientation))
            
        set_buffor_coordinates(final_grid, table_coord, placed_chairs)
        result_groups.append(TableGroup(tables=table_objs, chairinterfaces=chair_objs))

    return result_groups


