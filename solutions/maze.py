import utility

def _get_substance_amount():
    return get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

# region class

def new(anchor):
    world_size = get_world_size()
    world_area = world_size * world_size
    
    maze = []
    for _ in range(world_area):
        maze.append(None)
    member = maze, anchor

    visited = []
    for _ in range(world_area):
        visited.append(False)
    path = []
    cache = [visited, path]

    return member, cache

def _dfs(maze, cache):
    visited = cache[0]
    cache[1] = []
    
    world_size = get_world_size()
    world_area = world_size * world_size

    for i in range(world_area):
        maze[i] = 1024, None
        visited[i] = False

    def _get_directions(x, y):
        directions = []
        i = y * world_size + x
        if x > 0 and not visited[i - 1]:
            if can_move(West):
                directions.append(West)
        if x < world_size - 1 and not visited[i + 1]:
            if can_move(East):
                directions.append(East)
        if y > 0 and not visited[i - world_size]:
            if can_move(South):
                directions.append(South)
        if y < world_size - 1 and not visited[i + world_size]:
            if can_move(North):
                directions.append(North)
        return directions
    def dfs(x, y, dist, dir):
        i = y * world_size + x
        visited[i] = True
        if dist < maze[i][0]:
            maze[i] = dist, dir
        directions = _get_directions(x, y)
        for i in range(len(directions)):
            dir = directions[i]
            nx, ny = utility.peek((x, y), dir)
            move(dir)
            dfs(nx, ny, dist + 1, dir)
            move(utility.dir_opposite(dir))

    x = get_pos_x()
    y = get_pos_y()
    dfs(x, y, 0, None)

def _gps(maze, anchor, pos):
    path = []
    world_size = get_world_size()
    x, y = pos

    while (x, y) != anchor:
        i = y * world_size + x
        dir = maze[i][1]
        path.append(dir)
        x, y = utility.peek((x, y), utility.dir_opposite(dir))
    utility.reverse(path)
    return path

def _goto(maze, anchor, cache, target):
    path1 = _gps(maze, anchor, target)
    path2 = cache[1]

    prefix = 0
    for i in range(min(len(path1), len(path2))):
        if path1[i] != path2[i]:
            break
        prefix += 1

    world_size = get_world_size()
    def move_heuristic(dir):
        x = get_pos_x()
        y = get_pos_y()
        i = y * world_size + x
        def update(dir):
            if not can_move(dir):
                return
            nx, ny = utility.peek((x, y), dir)
            j = ny * world_size + nx
            dist_i = maze[i][0]
            dist_j = maze[j][0]
            if dist_i + 1 < dist_j:
                maze[j] = dist_i + 1, dir
            elif dist_j + 1 < dist_i:
                maze[i] = dist_j + 1, utility.dir_opposite(dir)
        update(East)
        update(West)
        update(North)
        update(South)
        move(dir)

    i = len(path2) - 1
    for _ in range(len(path2) - prefix):
        move_heuristic(utility.dir_opposite(path2[i]))
        i -= 1

    i = prefix
    while i < len(path1):
        move_heuristic(path1[i])
        i += 1

    cache[1] = path1

def step(obj):
    member, cache = obj
    maze, (x, y) = member
    entity = get_entity_type()
    if entity != Entities.Hedge and entity != Entities.Treasure:
        utility.move_to(x, y)
        utility.set_entity_type(Entities.Bush)
        use_item(Items.Weird_Substance, _get_substance_amount())
        _dfs(maze, cache)
    target = measure()
    _goto(maze, (x, y), cache, target)
    if not use_item(Items.Weird_Substance, _get_substance_amount()):
        harvest()

def delete():
    harvest()

# endregion

def _pred(num_gold):
    if num_gold == None:
        return True
    return num_items(Items.Gold) < num_gold

def run(num_gold=None):
    world_size = get_world_size()
    anchor = world_size // 2, world_size // 2
    obj = new(anchor)
    while _pred(num_gold):
        step(obj)
    delete()
