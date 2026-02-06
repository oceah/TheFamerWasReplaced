import utility

def _loop():
    def moven(dir, n):
        for _ in range(n):
            if not move(dir):
                return False
        return True
    
    if not move(East):
        return False
    world_size = get_world_size()
    for _ in range(world_size // 2 - 1):
        if not moven(East, world_size - 2):
            return False
        if not move(North):
            return False
        if not moven(West, world_size - 2):
            return False
        if not move(North):
            return False
    if not moven(East, world_size - 2):
        return False
    if not move(North):
        return False
    if not moven(West, world_size - 1):
        return False
    if not moven(South, world_size - 1):
        return False
    return True

def step():
    utility.move_to(0, 0)
    change_hat(Hats.Dinosaur_Hat)
    while _loop():
        pass
    change_hat(Hats.Straw_Hat)

def _pred(num_bone):
    if num_bone == None:
        return True
    return num_items(Items.Bone) < num_bone

def _assert():
    world_size = get_world_size()
    world_area = world_size * world_size
    cost = get_cost(Entities.Apple)
    cactus_threshold = cost[Items.Cactus] * world_area
    if num_items(Items.Cactus) < cactus_threshold:
        import cactus
        cactus.run(cactus_threshold)

def run(num_bone=None):
    clear()
    while _pred(num_bone):
        _assert()
        step()
