## A Star

### Data preparation
#### Getting Neighbors
Collisions are precomputed in grid at begging contains all objects with collisions and walls. We use ```grid.generateNeighborsGraph()``` for generation in ```model._initModel()```. ```grid.generateNeighborsGraph()``` generates graph of neighbors where we can move from specific state. To get neighbors use ```getNeighbors(position)```.

#### Getting Cost
Cost is generated at begging in grid base on passed carpets. We use ```grid.setCarpets()``` and ```grid.getCost(position)``` for getting cost of tile. Default cost is specified in [config file](../AI/conf.py) and is used if we don't find register in grid for carpets. Each carpet can have their cost that is passed to grid at initialization of model in grid via ```carpet.getCost()```.


### Path finding
#### ```calculateDistance()```
Is used for calculation of distance between current position and target position. Uses manhattan norm.

#### ```_find_adjacent_target()```
Is used for finding best tile where we are going to. Because when we are giving food to client we are going to nearest free tile instead of in client.

#### ```updateKey()```
Validates new state. Checks if state didn't exist in g_score register. Checks if new one have better g_score. Calculates f_score = g_score + heuristic. Adds new state to priority queue base on f_score. Generates movement graph.

#### ```goTo()```
Give order of going somewhere. Main movement function. Generates ```_find_adjacent_target()``` than ```generatePath()```.

#### ```generatePath()``` implementation of ```A*```
##### Structures
- ```heapq``` - min heap queue.

##### Initialization
Generates starting position and key. Generates target position. Crates priority queue, visited set and adds first starting key to priority queue. Initialization of movement graph (```came_from```).

##### Search loop
Gets first element form priority queue and unpacks data. Checks if we reach target. Checks if we already visited state and skips if we do. Adds new states to visited. Gets list of allowed movement from precomputed grid neighbors list. Gets neighbor position base on current position and direction. Checks collisions for forward movement aka checks if new neighbor is in list of neighbors we obtained from gird. If no than we skip it. If yes than we generates new neighbor key than we gets cost and we are using```updateKey()```. After forward movement we are checking rotations for left and right and again we are using ```updateKey()``` for states with rotation.

##### Post search path generation
We are checking if we find target if not we return empty path. Elsewhere we are going back through movement graph(```came_from```) from target to start. We revert generated path to obtain path from start to target.

