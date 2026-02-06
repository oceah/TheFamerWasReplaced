# region abstract

def ceil(x):
    floor_x = x // 1
    if floor_x == x:
        return floor_x
    return floor_x + 1

def isqrt(x):
    """ return int(sqrt(x)) """
    lo = 0
    hi = x // 2 + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi

def randint(low, high):
    """
    Samples a random number between low (inclusive) and high (exclusive).
    """
    return random() * (high - low) + low

def reverse(arr, i = 0, n = None):
    if n == None:
        n = len(arr)
    j = n - 1
    while i < j:
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1

def sgn_abs(x):
    """ return sgn(x), abs(x) """
    if x > 0:
        return 1, x
    if x < 0:
        return -1, -x
    return 0, 0

def shuffle(arr):
    n = len(arr)
    while n > 1:
        id = randint(0, n)
        arr[id], arr[n - 1] = arr[n - 1], arr[id]
        n -= 1

def factorize(x):
    a = isqrt(x)
    while a > 1:
        if x % a == 0:
            b = x // a
            return a, b
        a -= 1
    return 1, x

# endregion

# region getters

_entity_info = {
    Entities.Grass:     0.5,
    Entities.Bush:      4.8,
    Entities.Tree:      8.4,
    Entities.Carrot:    7.2,
    Entities.Pumpkin:   3.8,
    Entities.Cactus:    1,
    Entities.Sunflower: 8.4,
}

def get_grouth_time(entity):
    return _entity_info[entity]

_item_info = {
    Items.Hay:              (Entities.Grass,        None),
    Items.Wood:             (Entities.Tree,         Unlocks.Plant),
    Items.Carrot:           (Entities.Carrot,       Unlocks.Carrots),
    Items.Pumpkin:          (Entities.Pumpkin,      Unlocks.Pumpkins),
    Items.Cactus:           (Entities.Cactus,       Unlocks.Cactus),
    Items.Bone:             (Entities.Apple,        Unlocks.Dinosaurs),
    Items.Weird_Substance:  (None,                  Unlocks.Fertilizer),
    Items.Gold:             (None,                  Unlocks.Mazes),
    Items.Water:            (None,                  Unlocks.Watering),
    Items.Fertilizer:       (None,                  Unlocks.Fertilizer),
    Items.Power:            (Entities.Sunflower,    Unlocks.Sunflowers),
}

def item_to_entity(item):
    if item in _item_info:
        return _item_info[item][0]

def item_to_unlock(item):
    if item in _item_info:
        return _item_info[item][1]

# endregion

# region position

def dir_opposite(dir):
    if dir == East:
        return West
    if dir == West:
        return East
    if dir == North:
        return South
    return North

def get_dist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    n = get_world_size()
    dx = min(dx, n - dx)
    dy = min(dy, n - dy)
    return dx + dy

def greedy_sort(pos, list_pos, i = 0, n = None):
    if n == None:
        n = len(list_pos)
    while n > 1:
        id = 0
        min_d = get_dist(pos, list_pos[i])
        j = 1
        while j < n:
            d = get_dist(pos, list_pos[i + j])
            if d < min_d:
                id = j
                min_d = d
            j += 1
        pos = list_pos[i + id]
        list_pos[i + id] = list_pos[i + n - 1]
        list_pos[i + n - 1] = pos
        n -= 1
    reverse(list_pos, i, n)

def move_to(x, y):
    set_pos_x(x)
    set_pos_y(y)

def moven(dir, n):
    for _ in range(n):
        move(dir)

def peek(pos, dir):
    x, y = pos
    n = get_world_size()
    if dir == East:
        x = (x + 1) % n
    elif dir == West:
        x = (x - 1) % n
    elif dir == North:
        y = (y + 1) % n
    else:
        y = (y - 1) % n
    return x, y

def set_pos_x(x):
    sx, dx = sgn_abs(x - get_pos_x())
    if sx == 0:
        return
    n = get_world_size()
    n_dx = n - dx
    if n_dx < dx:
        dx = n_dx
        sx = -sx
    if sx > 0:
        moven(East, dx)
    else:
        moven(West, dx)

def set_pos_y(y):
    sy, dy = sgn_abs(y - get_pos_y())
    if sy == 0:
        return
    n = get_world_size()
    n_dy = n - dy
    if n_dy < dy:
        dy = n_dy
        sy = -sy
    if sy > 0:
        moven(North, dy)
    else:
        moven(South, dy)

# endregion

# region setters

def ripen():
    fertilizer_threshold = max_drones()
    water_threshold = fertilizer_threshold * 4
    def do_ripen(grouth_time, is_ripe):
        if grouth_time <= 2:
            while not is_ripe():
                if num_items(Items.Fertilizer) > fertilizer_threshold:
                    use_item(Items.Fertilizer)
                elif num_items(Items.Water) > water_threshold:
                    if get_water() <= 0.75:
                        use_item(Items.Water)
        else:
            water = grouth_time / 8 - 0.25
            while not is_ripe():
                if num_items(Items.Fertilizer) > fertilizer_threshold and num_items(Items.Water) > water_threshold:
                    set_water(water)
                    use_item(Items.Fertilizer)
                elif num_items(Items.Water) > water_threshold:
                    if get_water() <= 0.75:
                        use_item(Items.Water)

    entity = get_entity_type()
    
    if entity == None:
        return
    if entity == Entities.Tree:
        while not can_harvest():
            if num_items(Items.Water) > water_threshold:
                if get_water() <= 0.75:
                    use_item(Items.Water)
            if num_items(Items.Fertilizer) > fertilizer_threshold:
                use_item(Items.Fertilizer)
    if entity == Entities.Dead_Pumpkin:
        return
    if entity == Entities.Pumpkin:
        def pumpkin_is_ripe():
            if get_entity_type() == Entities.Dead_Pumpkin:
                return True
            return can_harvest()
        grouth_time = get_grouth_time(Entities.Pumpkin)
        return do_ripen(grouth_time, pumpkin_is_ripe)
    
    grouth_time = get_grouth_time(entity)
    do_ripen(grouth_time, can_harvest)

def set_entity_type(entity):
    cur_entity = get_entity_type()
    if cur_entity == entity:
        return True
    # assert get_entity_type() != entity
    def reset_ground(ground):
        if get_ground_type() != ground:
            till()
        else:
            harvest()
    if entity == None:
        reset_ground(Grounds.Soil)
        return True
    elif entity == Entities.Grass:
        reset_ground(Grounds.Grassland)
        return True
    elif entity == Entities.Bush or entity == Entities.Tree:
        if cur_entity != None and cur_entity != Entities.Grass:
            harvest()
        return plant(entity)
    else:
        reset_ground(Grounds.Soil)
        return plant(entity)

def set_ground_type(ground):
    if get_ground_type() != ground:
        till()

def set_water(water):
    water -= get_water()
    if water <= 0:
        return
    num_water = ceil(water / 0.25)
    for _ in range(num_water):
        use_item(Items.Water)

# endregion

# region workspace

def whole_world():
    n = get_world_size()
    return 0, 0, n, n

def work_and_move(cell, dir):
    cell()
    move(dir)

def work_and_moven(cell, dir, n):
    for _ in range(n):
        work_and_move(cell, dir)

def work_for_each(cell, workspace):
    origin_x, origin_y, size_x, size_y = workspace
    move_to(origin_x, origin_y)
    dir = East
    for _ in range(size_y - 1):
        work_and_moven(cell, dir, size_x - 1)
        work_and_move(cell, North)
        dir = dir_opposite(dir)
    work_and_moven(cell, dir, size_x - 1)
    cell()

# endregion
