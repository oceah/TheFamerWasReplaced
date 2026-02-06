import utility
import thread

num_hay = 2000000000

def cell():
    harvest()
    while True:
        entity, (x, y) = get_companion()
        if entity == Entities.Bush and (x + y) % 2:
            break
        harvest()

def task(id):
    utility.set_pos_y(id)
    if id % 2 == 0:
        move(East)
    for _ in range(15):
        plant(Entities.Bush)
        move(East)
        move(East)
    plant(Entities.Bush)
    move(East)
    while num_items(Items.Hay) < num_hay:
        cell()
        move(East)
        move(East)

thread.fork(task, 32)
