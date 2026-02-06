import utility
import thread

# region class

# origin_x, origin_y, pumpkin_size = p_workspace
def new(p_workspace, threads):
    origin_x, origin_y, pumpkin_size = p_workspace
    workspace = origin_x, origin_y, pumpkin_size, pumpkin_size
    return workspace, threads

def _plant_check_fix(workspace):
    def cell():
        utility.set_entity_type(Entities.Pumpkin)
    utility.work_for_each(cell, workspace)

    dead_pumpkins = []
    def cell():
        utility.ripen()
        if get_entity_type() == Entities.Dead_Pumpkin:
            harvest()
            plant(Entities.Pumpkin)
            x = get_pos_x()
            y = get_pos_y()
            dead_pumpkins.append((x, y))
    utility.work_for_each(cell, workspace)

    def fix():
        x = get_pos_x()
        y = get_pos_y()
        utility.greedy_sort((x, y), dead_pumpkins)
        i = 0
        for x, y in dead_pumpkins:
            utility.move_to(x, y)
            utility.ripen()
            if get_entity_type() == Entities.Dead_Pumpkin:
                harvest()
                plant(Entities.Pumpkin)
                dead_pumpkins[i] = x, y
                i += 1
        for _ in range(len(dead_pumpkins) - i):
            dead_pumpkins.pop()

    while len(dead_pumpkins) > 0:
        fix()

def step(obj):
    workspace, threads = obj

    world_size = get_world_size()
    world_area = world_size * world_size
    cost = get_cost(Entities.Pumpkin)
    carrot_threshold = cost[Items.Carrot] * world_area * 2

    if num_items(Items.Carrot) < carrot_threshold:
        import common_crops
        common_crops.run({Items.Carrot:carrot_threshold}, workspace, threads)

    if threads == 1:
        _plant_check_fix(workspace)
    else:
        thread.joinxy(_plant_check_fix, workspace, threads)
    harvest()

# endregion

def _pred(num_pumpkin):
    if num_pumpkin == None:
        return True
    return num_items(Items.Pumpkin) < num_pumpkin

def run_single(num_pumpkin=None, workspace=utility.whole_world(), threads=1):
    origin_x, origin_y, size_x, size_y = workspace
    pumpkin_size = min(size_x, size_y)
    p_workspace = origin_x, origin_y, pumpkin_size
    obj = new(p_workspace, threads)
    while _pred(num_pumpkin):
        step(obj)

def run(num_pumpkin=None, workspace=utility.whole_world(), threads=max_drones()):
    origin_x, origin_y, size_x, size_y = workspace

    min_p = min(6, size_x, size_y)
    x_blocks, y_blocks = 1, 1
    blocks = 1
    x = 1
    max_x = min(threads, (size_x + 1) // (min_p + 1))
    while x <= max_x:
        min_y = max(1, (blocks + x - 1) // x)
        y = min(threads // x, (size_y + 1) // (min_p + 1))
        if y >= min_y:
            xy = x * y
            if xy > blocks:
                x_blocks, y_blocks = x, y
                blocks = xy
        x += 1

    pumpkin_size_x = (size_x + 1) // x_blocks - 1
    pumpkin_size_y = (size_y + 1) // y_blocks - 1
    pumpkin_size = min(pumpkin_size_x, pumpkin_size_y)

    b, r = threads // blocks, threads % blocks

    def task(id):
        i, j = id % x_blocks, id // x_blocks
        t_origin_x = origin_x + i * (pumpkin_size + 1)
        t_origin_y = origin_y + j * (pumpkin_size + 1)
        if id == blocks - 1:
            t_pumpkin_size_x = origin_x + size_x - t_origin_x
            t_pumpkin_size_y = origin_y + size_y - t_origin_y
            t_pumpkin_size = min(t_pumpkin_size_x, t_pumpkin_size_y)
        else:
            t_pumpkin_size = pumpkin_size
        if blocks - id - 1 < r:
            threads = b + 1
        else:
            threads = b
        workspace = t_origin_x, t_origin_y, t_pumpkin_size, t_pumpkin_size
        run_single(num_pumpkin, workspace, threads)

    thread.join(task, blocks)
