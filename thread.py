import utility

# region detach/fork/join
# def task(id): pass

def detach(task, threads):
    for id in range(threads):
        def wrapper():
            task(id)
        spawn_drone(wrapper)

def fork(task, threads):
    if threads <= 0:
        return
    id = 1
    while id < threads:
        def wrapper():
            task(id)
        spawn_drone(wrapper)
        id += 1
    task(0)

def join(task, threads):
    if threads <= 0:
        return
    drones = []
    id = 1
    while id < threads:
        def wrapper():
            task(id)
        drones.append(spawn_drone(wrapper))
        id += 1
    task(0)
    for drone in drones:
        wait_for(drone)

# endregion

# region detach/fork/join-x/y
# def task(workspace): pass

def detachx(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchx(detach, task, workspace, threads)

def detachy(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchy(detach, task, workspace, threads)

def forkx(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchx(fork, task, workspace, threads)

def forky(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchy(fork, task, workspace, threads)

def joinx(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchx(join, task, workspace, threads)

def joiny(
        task, 
        workspace = utility.whole_world(), 
        threads = max_drones()):
    _wrap_and_dispatchy(join, task, workspace, threads)

def _wrap_and_dispatchx(f, task, workspace, threads):
    origin_x, origin_y, size_x, size_y = workspace
    threads = min(threads, size_x)
    by, ry = size_y // threads, size_y % threads
    def wrapper(id):
        if id < ry:
            oy, sy = id * (by + 1), by + 1
        else:
            oy, sy = ry * (by + 1) + (id - ry) * by, by
        thread_workspace = origin_x, origin_y + oy, size_x, sy
        task(thread_workspace)
    f(wrapper, threads)

def _wrap_and_dispatchy(f, task, workspace, threads):
    origin_x, origin_y, size_x, size_y = workspace
    threads = min(threads, size_x)
    bx, rx = size_x // threads, size_x % threads
    def wrapper(id):
        if id < rx:
            ox, sx = id * (bx + 1), bx + 1
        else:
            ox, sx = rx * (bx + 1) + (id - rx) * bx, bx
        thread_workspace = origin_x + ox, origin_y, sx, size_y
        task(thread_workspace)
    f(wrapper, threads)

# endregion

# region detach/fork/join-xy
# forkxy(task)
# forkxy(task, workspace, threads)
# forkxy(task, workspace, x_threads, y_threads)
# def task(workspace): pass

def forkxy(
        task, 
        workspace = utility.whole_world(), 
        x_threads = None, 
        y_threads = None):
    _wrap_and_dispatchxy(fork, task, workspace, x_threads, y_threads)

def joinxy(
        task, 
        workspace = utility.whole_world(), 
        x_threads = None, 
        y_threads = None):
    _wrap_and_dispatchxy(join, task, workspace, x_threads, y_threads)

def detachxy(
        task, 
        workspace = utility.whole_world(), 
        x_threads = None, 
        y_threads = None):
    _wrap_and_dispatchxy(detach, task, workspace, x_threads, y_threads)

def _wrap_and_dispatchxy(f, task, workspace, x_threads, y_threads):
    if y_threads == None:
        if x_threads == None:
            x_threads = max_drones()
        x_threads, y_threads = utility.factorize(x_threads)
    origin_x, origin_y, size_x, size_y = workspace
    x_threads = min(x_threads, size_x)
    y_threads = min(y_threads, size_y)
    bx, rx = size_x // x_threads, size_x % x_threads
    by, ry = size_y // y_threads, size_y % y_threads
    def axis_range(i, b, r):
        if i < r:
            return i * (b + 1), b + 1
        else:
            return r * (b + 1) + (i - r) * b, b
    def wrapper(id):
        i = id % x_threads
        j = id // x_threads
        ox, sx = axis_range(i, bx, rx)
        oy, sy = axis_range(j, by, ry)
        thread_workspace = origin_x + ox, origin_y + oy, sx, sy
        task(thread_workspace)
    f(wrapper, x_threads * y_threads)

# endregion
