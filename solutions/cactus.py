import utility
import thread

def _sort(workspace_x, get, swp, front, x):
    origin_x, size_x = workspace_x
    back = utility.dir_opposite(front)
    world_size = get_world_size()

    def try_swap(i, dir):
        if dir == front:
            j = i + 1
            if get(i) > get(j):
                swap(front)
                swp(i, j)
                return True
        if dir == back:
            j = i - 1
            if get(i) < get(j):
                swap(back)
                swp(i, j)
                return True
        return False
    def stabilize(i):
        is_unstable = True
        while is_unstable:
            is_unstable = False
            if i > 0 and try_swap(i, back):
                is_unstable = True
            if i < size_x - 1 and try_swap(i, front):
                is_unstable = True
    def is_unsorted(i):
        if i > 0 and get(i) < get(i - 1):
            return True
        if i < size_x - 1 and get(i) > get(i + 1):
            return True
        return False
    def get_nearest_unsorted(x):
        if is_unsorted(x - origin_x):
            return x
        x1 = (x - 1) % world_size
        x2 = (x + 1) % world_size
        i = size_x - 1
        while i > 0:
            x = x1 - origin_x
            if 0 <= x and x < size_x:
                if is_unsorted(x):
                    return x1
                i -= 1
            x = x2 - origin_x
            if 0 <= x and x < size_x:
                if is_unsorted(x):
                    return x2
                i -= 1
            x1 = (x1 - 1) % world_size
            x2 = (x2 + 1) % world_size
        return None
    def goto(x, nx):
        sx, x = utility.sgn_abs(nx - x)
        if sx == 0:
            return
        nx = world_size - x
        if nx < x:
            x = nx
            sx = -sx
        if sx > 0:
            utility.moven(front, x)
        else:
            utility.moven(back, x)

    while True:
        nx = get_nearest_unsorted(x)
        if nx == None:
            break
        goto(x, nx)
        x = nx
        stabilize(x - origin_x)

def _plant(workspace, cache=[]):
    origin_x, origin_y, size_x, size_y = workspace
    area = size_x * size_y
    for i in range(min(area, len(cache))):
        cache[i] = None
    for _ in range(area - len(cache)):
        cache.append(None)

    def try_swap(i, dir):
        ok = False
        if dir == East:
            j = i + 1
            ok = cache[j] and cache[i] > cache[j]
        elif dir == West:
            j = i - 1
            ok = cache[j] and cache[i] < cache[j]
        else:
            j = i - size_x
            ok = cache[i] < cache[j]
        if ok:
            swap(dir)
            cache[i], cache[j] = cache[j], cache[i]
        return ok
    def stabilize(x, y):
        x -= origin_x
        y -= origin_y
        i = y * size_x + x
        is_unstable = True
        while is_unstable:
            is_unstable = False
            if x > 0 and try_swap(i, West):
                is_unstable = True
            if x < size_x - 1 and try_swap(i, East):
                is_unstable = True
            if y > 0 and try_swap(i, South):
                is_unstable = True
    def cell():
        utility.set_entity_type(Entities.Cactus)
        x = get_pos_x()
        y = get_pos_y()
        i = (y - origin_y) * size_x + x - origin_x
        cache[i] = measure()
        stabilize(x, y)
    
    workspace_x = origin_x, size_x
    def sort_x(j):
        utility.set_pos_y(origin_y + j)
        ox = j * size_x
        def get(i):
            return cache[ox + i]
        def swp(i1, i2):
            cache[ox + i1], cache[ox + i2] = cache[ox + i2], cache[ox + i1]
        _sort(workspace_x, get, swp, East, get_pos_x())
    workspace_y = origin_y, size_y
    def sort_y(i):
        utility.set_pos_x(origin_x + i)
        def get(j):
            return cache[j * size_x + i]
        def swp(j1, j2):
            cache[j1 * size_x + i], cache[j2 * size_x + i] = cache[j2 * size_x + i], cache[j1 * size_x + i]
        _sort(workspace_y, get, swp, North, get_pos_y())

    utility.work_for_each(cell, workspace)

    j = size_y - 1
    while j >= 0:
        sort_x(j)
        j -= 1

    i = get_pos_x() - origin_x
    if i < size_x - i - 1:
        for i in range(size_x):
            sort_y(i)
    else:
        i = size_x - 1
        while i >= 0:
            sort_y(i)
            i -= 1

def _scan(front, x):
    back = utility.dir_opposite(front)
    world_size = get_world_size()
    arr = []
    for _ in range(world_size):
        arr.append(None)

    def try_swap(x, dir):
        ok = False
        if dir == front:
            i = x + 1
            ok = arr[i] and arr[x] > arr[i]
        else:
            i = x - 1
            ok = arr[i] and arr[x] < arr[i]
        if ok:
            swap(dir)
            arr[x], arr[i] = arr[i], arr[x]
        return ok
    def stabilize(x):
        is_unstable = True
        while is_unstable:
            is_unstable = False
            if x > 0 and try_swap(x, back):
                is_unstable = True
            if x < world_size - 1 and try_swap(x, front):
                is_unstable = True
    def cell(x):
        arr[x] = measure()
        stabilize(x)
    
    for _ in range(world_size - 1):
        cell(x)
        move(front)
        x = (x + 1) % world_size
    cell(x)

    return arr

def _sort_x(y):
    utility.set_pos_y(y)
    arr = _scan(East, get_pos_x())
    workspace_x = 0, get_world_size()
    def get(x):
        return arr[x]
    def swp(x1, x2):
        arr[x1], arr[x2] = arr[x2], arr[x1]
    _sort(workspace_x, get, swp, East, get_pos_x())

def _sort_y(x):
    utility.set_pos_x(x)
    arr = _scan(North, get_pos_y())
    workspace_y = 0, get_world_size()
    def get(y):
        return arr[y]
    def swp(y1, y2):
        arr[y1], arr[y2] = arr[y2], arr[y1]
    _sort(workspace_y, get, swp, North, get_pos_y())

def _pred(num_cactus):
    if num_cactus == None:
        return True
    return num_items(Items.Cactus) < num_cactus

def _assert():
    world_size = get_world_size()
    world_area = world_size * world_size
    cost = get_cost(Entities.Cactus)
    pumpkin_threshold = cost[Items.Pumpkin] * world_area
    if num_items(Items.Pumpkin) < pumpkin_threshold:
        import pumpkin
        pumpkin.run(pumpkin_threshold)

def run_single(num_cactus=None):
    cache = []
    while _pred(num_cactus):
        _assert()
        _plant(utility.whole_world(), cache)
        harvest()

def run(num_cactus=None):
    if max_drones() == 1:
        return run_single(num_cactus)

    def sort_x(workspace):
        _, origin_y, _, size_y = workspace
        for i in range(size_y):
            _sort_x(origin_y + i)
    def sort_y(workspace):
        origin_x, _, size_x, _ = workspace
        for i in range(size_x):
            _sort_y(origin_x + i)

    while _pred(num_cactus):
        _assert()
        thread.joinxy(_plant)
        thread.joinx(sort_x)
        thread.joiny(sort_y)
        harvest()
