import utility
import thread

fps = 30
res = 32
entity_0 = Entities.Grass
entity_1 = None

def task(y):
    utility.move_to(0, y)
    spf = 1 / fps
    for i in range(len(vedio)):
        frame = vedio[i]
        row = frame[y]
        mask = 2 ** (res - 1)
        for _ in range(res):
            if row // mask:
                utility.set_entity_type(entity_1)
            else:
                utility.set_entity_type(entity_0)
            row %= mask
            mask //= 2
            move(East)
        while get_time() < start + spf * (i + 1):
            pass

set_world_size(res)

import bad_apple_data_1
vedio = bad_apple_data_1.data
start = get_time()
thread.join(task, res)

import bad_apple_data_2
vedio = bad_apple_data_2.data
start = get_time()
thread.join(task, res)

import bad_apple_data_3
vedio = bad_apple_data_3.data
start = get_time()
thread.join(task, res)

import bad_apple_data_4
vedio = bad_apple_data_4.data
start = get_time()
thread.join(task, res)

import bad_apple_data_5
vedio = bad_apple_data_5.data
start = get_time()
thread.join(task, res)

import bad_apple_data_6
vedio = bad_apple_data_6.data
start = get_time()
thread.join(task, res)

import bad_apple_data_7
vedio = bad_apple_data_7.data
start = get_time()
thread.join(task, res)

import bad_apple_data_8
vedio = bad_apple_data_8.data
start = get_time()
thread.join(task, res)

import bad_apple_data_9
vedio = bad_apple_data_9.data
start = get_time()
thread.join(task, res)

import bad_apple_data_10
vedio = bad_apple_data_10.data
start = get_time()
thread.join(task, res)

import bad_apple_data_11
vedio = bad_apple_data_11.data
start = get_time()
thread.join(task, res)

import bad_apple_data_12
vedio = bad_apple_data_12.data
start = get_time()
thread.join(task, res)

import bad_apple_data_13
vedio = bad_apple_data_13.data
start = get_time()
thread.join(task, res)
