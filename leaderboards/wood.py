import utility
import thread

num_wood = 10000000000
water_threshold = 0.75

## Strategy - Tree and Bush
# P(companion) = 1/6
# E(ops per cell) = 12
# E(ticks per cell) = 2400
# E(ticks per loop) = 76800
# ticks per second = xxx
# E(loop time) = 76800/xxx s
# max grouth time = 6.6 s

def await_harvest():
    utility.set_water(water_threshold)
    while not can_harvest():
        pass
    harvest()

def task(id):
    utility.set_pos_y(id)
    if id % 2:
        move(East)
    while num_items(Items.Wood) < num_wood:
        await_harvest()
        while True:
            plant(Entities.Tree)
            entity, (x, y) = get_companion()
            if entity == Entities.Bush and (x + y) % 2:
                break
            harvest()
        move(East)
        await_harvest()
        while True:
            plant(Entities.Bush)
            entity, (x, y) = get_companion()
            if entity == Entities.Tree and (x + y) % 2 == 0:
                break
            harvest()
        move(East)

thread.fork(task, 32)
