import utility
import thread

min_petals = 7
max_petals = 15

# region class

def new(workspace, threads):
    bucket = []
    for _ in range(max_petals - min_petals + 1):
        bucket.append(None)
    return workspace, bucket, threads

def _plant_and_measure(workspace, bucket, threads):
    for i in range(len(bucket)):
        bucket[i] = []

    def measure_and_append():
        petals = measure()
        x = get_pos_x()
        y = get_pos_y()
        bucket[petals - min_petals].append((x, y))
    if threads == 1:
        def cell():
            utility.set_entity_type(Entities.Sunflower)
            measure_and_append()
        return utility.work_for_each(cell, workspace)

    def cell():
        utility.set_entity_type(Entities.Sunflower)
    def task(workspace):
        utility.work_for_each(cell, workspace)
    thread.joinxy(task, workspace, threads)

    utility.work_for_each(measure_and_append, workspace)    

def _harvest(pos_sunflowers, threads):
    def harvest_single(pos_sunflowers):
        x = get_pos_x()
        y = get_pos_y()
        utility.greedy_sort((x, y), pos_sunflowers)
        for x, y in pos_sunflowers:
            utility.move_to(x, y)
            utility.ripen()
            harvest()

    if threads == 1:
        return harvest_single(pos_sunflowers)

    n = len(pos_sunflowers)
    threads = min(threads, n)
    b, r = n // threads, n % threads
    def task(id):
        if id < r:
            i, n = id * (b + 1), b + 1
        else:
            i, n = r * (b + 1) + (id - r) * b, b
        x = get_pos_x()
        y = get_pos_y()
        utility.greedy_sort((x, y), pos_sunflowers, i, n)
        for _ in range(n):
            x, y = pos_sunflowers[i]
            utility.move_to(x, y)
            utility.ripen()
            harvest()
            i += 1
    thread.join(task, threads)

def step(obj):
    workspace, bucket, threads = obj

    world_size = get_world_size()
    world_area = world_size * world_size
    cost = get_cost(Entities.Sunflower)
    carrot_threshold = cost[Items.Carrot] * world_area
    if num_items(Items.Carrot) < carrot_threshold:
        import common_crops
        common_crops.run({Items.Carrot:carrot_threshold}, workspace, threads)

    _plant_and_measure(workspace, bucket, threads)
    _, _, size_x, size_y = workspace
    num_sunflower = size_x * size_y
    i = len(bucket) - 1
    while i >= 0 and num_sunflower >= 10:
        bucket_i = bucket[i]
        if len(bucket_i) > 0:
            _harvest(bucket_i, threads)
            num_sunflower -= len(bucket_i)
        i -= 1

# endregion

def _pred(num_power):
    if num_power == None:
        return True
    return num_items(Items.Power) < num_power

def run_evil(num_power=None, workspace=utility.whole_world(), threads=max_drones()):
    def cell():
        utility.ripen()
        harvest()
        utility.set_entity_type(Entities.Sunflower)
    def run_evil_single(workspace):
        while _pred(num_power):
            utility.work_for_each(cell, workspace)
    if threads == 1:
        return run_evil_single(workspace)
    thread.joinxy(run_evil_single, workspace, threads)

def run_single(num_power=None, workspace=utility.whole_world(), threads=1):
    _, _, size_x, size_y = workspace
    if size_x * size_y < 36:
        run_evil(num_power, workspace, threads)
    obj = new(workspace, threads)
    while _pred(num_power):
        step(obj)

def run(num_power=None, workspace=utility.whole_world(), threads=max_drones()):
    if threads == 1:
        return run_single(num_power, workspace)
    obj = new(workspace, threads)
    while _pred(num_power):
        step(obj)
