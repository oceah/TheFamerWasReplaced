import utility
import thread

# region class

def new(workspace, num_crops):
    _, _, size_x, size_y = workspace
    companion_entity = []
    for _ in range(size_x * size_y):
        companion_entity.append(None)
    if num_crops == None:
        num_hay_wood_carrot = 0, 0, 0
    else:
        def num_crop(item):
            if item in num_crops:
                return num_crops[item]
            return 0
        num_hay = num_crop(Items.Hay)
        num_wood = num_crop(Items.Wood)
        num_carrot = num_crop(Items.Carrot)
        num_hay_wood_carrot = num_hay, num_wood, num_carrot
    return workspace, companion_entity, num_hay_wood_carrot

def _bush_or_tree():
    x = get_pos_x()
    y = get_pos_y()
    if (x + y) % 2 == 0:
        return Entities.Tree
    return Entities.Bush

# preference=None|Items.(Hay|Wood|Carrot)
def step(obj, preference=None):
    workspace, companion_entity, num_hay_wood_carrot = obj
    origin_x, origin_y, size_x, size_y = workspace
    num_hay, num_wood, num_carrot = num_hay_wood_carrot

    can_plant_bush = num_unlocked(Unlocks.Plant)
    can_plant_tree = can_plant_bush and num_unlocked(Unlocks.Trees)
    can_plant_carrot = can_plant_bush and num_unlocked(Unlocks.Carrots)
    if can_plant_carrot:
        world_size = get_world_size()
        world_area = world_size * world_size
        cost = get_cost(Entities.Carrot)
        hay_threshold = cost[Items.Hay] * world_area
        wood_threshold = cost[Items.Wood] * world_area
        if num_items(Items.Hay) < hay_threshold:
            can_plant_carrot = False
            if preference == Items.Carrot:
                preference = Items.Hay
        elif num_items(Items.Wood) < wood_threshold:
            can_plant_carrot = False
            if preference == Items.Carrot:
                preference = Items.Wood

    def choose_grass():
        return Entities.Grass
    def choose_bush():
        return Entities.Bush
    def choose_carrot():
        return Entities.Carrot
    
    def grass_or_bush():
        gap_hay = num_hay - num_items(Items.Hay)
        gap_wood = num_wood - num_items(Items.Wood)
        if gap_wood > gap_hay:
            return Entities.Bush
        return Entities.Grass
    def grass_bush_or_tree():
        gap_hay = num_hay - num_items(Items.Hay)
        gap_wood = num_wood - num_items(Items.Wood)
        if gap_wood > gap_hay:
            return _bush_or_tree()
        return Entities.Grass
    def grass_bush_or_carrot():
        gap_hay = num_hay - num_items(Items.Hay)
        gap_wood = num_wood - num_items(Items.Wood)
        gap_carrot = num_carrot - num_items(Items.Carrot)
        if gap_wood > gap_hay:
            entity = Entities.Bush
            max_gap = gap_wood
        else:
            entity = Entities.Grass
            max_gap = gap_hay
        if gap_carrot > max_gap:
            entity = Entities.Carrot
        return entity
    def grass_bush_tree_or_carrot():
        gap_hay = num_hay - num_items(Items.Hay)
        gap_wood = num_wood - num_items(Items.Wood)
        gap_carrot = num_carrot - num_items(Items.Carrot)
        if gap_carrot > gap_hay:
            entity = Entities.Carrot
            max_gap = gap_carrot
        else:
            entity = Entities.Grass
            max_gap = gap_hay
        if gap_wood > max_gap:
            entity = _bush_or_tree()
        return entity

    def get_wood_handler():
        if can_plant_tree:
            return _bush_or_tree
        if can_plant_bush:
            return choose_bush
        return choose_grass
    def get_carrot_handler():
        if can_plant_carrot:
            return choose_carrot
        if can_plant_tree:
            return grass_bush_or_tree
        if can_plant_bush:
            return grass_or_bush
        return choose_grass
    def get_compare_handler():
        if can_plant_bush:
            if can_plant_tree:
                if can_plant_carrot:
                    return grass_bush_tree_or_carrot
                return grass_bush_or_tree
            if can_plant_carrot:
                return grass_bush_or_carrot
            return grass_or_bush
        return choose_grass
            
    if preference == Items.Hay:
        choose_entity = choose_grass
    elif preference == Items.Wood:
        choose_entity = get_wood_handler()
    elif preference == Items.Carrot:
        choose_entity = get_carrot_handler()
    else:
        choose_entity = get_compare_handler()

    if num_unlocked(Unlocks.Polyculture):
        def get_companion_entity(x, y):
            x -= origin_x
            y -= origin_y
            return companion_entity[y * size_x + x]
        def set_companion_entity(x, y, entity):
            if x >= origin_x and y >= origin_y:
                x -= origin_x
                y -= origin_y
                if x < size_x and y < size_y:
                    companion_entity[y * size_x + x] = entity
        def cell():
            utility.ripen()
            harvest()
            x = get_pos_x()
            y = get_pos_y()
            plant_type = get_companion_entity(x, y)
            set_companion_entity(x, y, None)
            if plant_type == None:
                plant_type = choose_entity()
            while True:
                utility.set_entity_type(plant_type)
                entity, (x, y) = get_companion()
                if origin_x <= x and x < origin_x + size_x and origin_y <= y and y < origin_y + size_y:
                    cur_entity = get_companion_entity(x, y)
                    if cur_entity == entity:
                        break
                    if cur_entity == None:
                        if entity == Entities.Grass:
                            break
                        if entity == Entities.Bush and can_plant_bush:
                            break
                        if entity == Entities.Tree and can_plant_tree:
                            break
                        if entity == Entities.Carrot and can_plant_carrot:
                            break
                harvest()
            set_companion_entity(x, y, entity)
    else:
        def cell():
            utility.ripen()
            harvest()
            entity = choose_entity()
            utility.set_entity_type(entity)

    utility.work_for_each(cell, workspace)

# endregion

def _pred(num_crops):
    if num_crops == None:
        return True
    if Items.Hay in num_crops and num_items(Items.Hay) < num_crops[Items.Hay]:
        return True
    if Items.Wood in num_crops and num_items(Items.Wood) < num_crops[Items.Wood]:
        return True
    if Items.Carrot in num_crops and num_items(Items.Carrot) < num_crops[Items.Carrot]:
        return True
    return False

def run_single(num_crops=None, workspace=utility.whole_world()):
    obj = new(workspace, num_crops)
    while _pred(num_crops):
        step(obj)

def run(num_crops=None, workspace=utility.whole_world(), threads=max_drones()):
    _, _, size_x, size_y = workspace

    x_threads, y_threads = 1, 1
    max_t = 1
    min_e = abs(size_x - size_y)
    x = 1
    max_x = min(threads, size_x)
    while x <= max_x:
        sz_x = size_x // x
        min_sz_y = (32 + sz_x - 1) // sz_x
        y = max(1, (max_t + x - 1) // x)
        max_y = min(threads // x, size_y // min_sz_y)
        while y <= max_y:
            xy = x * y
            e = abs(x * size_y - y * size_x)
            if xy > max_t:
                x_threads, y_threads = x, y
                max_t = xy
                min_e = e
            elif xy == max_t and e < min_e:
                x_threads, y_threads = x, y
                min_e = e
            y += 1
        x += 1

    if x_threads * y_threads == 1:
        return run_single(num_crops, workspace)
    def task(workspace):
        run_single(num_crops, workspace)
    thread.joinxy(task, workspace, x_threads, y_threads)
