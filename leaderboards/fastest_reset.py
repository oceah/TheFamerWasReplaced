import common_crops
import pumpkin
import cactus
import dinosaur
import maze
import sunflower

K = 1000
M = 1000 * K
B = 1000 * M

parent_of_unlock = {
    Unlocks.Expand:Unlocks.Speed,
    Unlocks.Plant:Unlocks.Speed,
    Unlocks.Carrots:Unlocks.Plant,
    Unlocks.Watering:Unlocks.Carrots,
    Unlocks.Trees:Unlocks.Carrots,
    Unlocks.Fertilizer:Unlocks.Watering,
    Unlocks.Sunflowers:Unlocks.Watering,
    Unlocks.Pumpkins:Unlocks.Trees,
    Unlocks.Mazes:Unlocks.Fertilizer,
    Unlocks.Cactus:Unlocks.Pumpkins,
    Unlocks.Polyculture:Unlocks.Pumpkins,
    Unlocks.Megafarm:Unlocks.Mazes,
    Unlocks.Dinosaurs:Unlocks.Cactus,
}

unlocks = {
    Unlocks.Speed,
    Unlocks.Grass,
    Unlocks.Expand,
    Unlocks.Plant,
    Unlocks.Carrots,
    Unlocks.Watering,
    Unlocks.Trees,
    Unlocks.Fertilizer,
    Unlocks.Sunflowers,
    Unlocks.Pumpkins,
    Unlocks.Mazes,
    Unlocks.Cactus,
    Unlocks.Polyculture,
    Unlocks.Megafarm,
    Unlocks.Dinosaurs,
    Unlocks.Leaderboard,
}

def item_to_unlock(item):
    if item == Items.Wood:
        return Unlocks.Plant
    if item == Items.Carrot:
        return Unlocks.Carrots
    if item == Items.Pumpkin:
        return Unlocks.Pumpkins
    if item == Items.Cactus:
        return Unlocks.Cactus
    if item == Items.Bone:
        return Unlocks.Dinosaurs
    if item == Items.Weird_Substance:
        return Unlocks.Fertilizer
    if item == Items.Gold:
        return Unlocks.Mazes
    if item == Items.Water:
        return Unlocks.Watering
    if item == Items.Fertilizer:
        return Unlocks.Fertilizer
    if item == Items.Power:
        return Unlocks.Sunflowers
    return None

def is_unlockable(thing):
    if thing in parent_of_unlock:
        parent = parent_of_unlock[thing]
        if not num_unlocked(parent):
            return False
    cost = get_cost(thing)
    for item in cost:
        if item == Items.Weird_Substance:
            if num_items(item) < cost[item]:
                return False
        elif item == Items.Gold:
            substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
            if num_items(Items.Weird_Substance) < substance * 300:
                return False
        thing = item_to_unlock(item)
        if thing and not num_unlocked(thing):
            return False
    return True

def auto_unlock(thing, power_threshold):
    if unlock(thing):
        return

    cost = get_cost(thing)
    num_crops = {}
    if Items.Hay in cost:
        num_crops[Items.Hay] = cost[Items.Hay]
    if Items.Wood in cost:
        num_crops[Items.Wood] = cost[Items.Wood]
    if Items.Carrot in cost:
        num_crops[Items.Carrot] = cost[Items.Carrot]

    def pred():
        for item in cost:
            if num_items(item) < cost[item]:
                return True
        return False
    def assert_power():
        if num_items(Items.Power) < power_threshold:
            sunflower.run(cost[Items.Power])

    while pred():
        assert_power()
        if Items.Bone in cost:
            dinosaur.run(cost[Items.Bone])
        assert_power()
        if Items.Cactus in cost:
            cactus.run(cost[Items.Cactus])
        assert_power()
        if Items.Pumpkin in cost:
            pumpkin.run(cost[Items.Pumpkin])
        assert_power()
        if len(num_crops) > 0:
            common_crops.run(num_crops)
        assert_power()
        if Items.Gold in cost:
            maze.run(cost[Items.Gold])

    unlock(thing)

def choose_unlock(unlocks):
    choosed = None
    min_cost = B
    min_nmlk = B
    for thing in unlocks:
        if is_unlockable(thing):
            cost = get_cost(thing)
            c = 0
            for item in cost:
                c += cost[item]
            nmlk = num_unlocked(thing)
            if c < min_cost:
                choosed = thing
                min_cost = c
                min_nmlk = nmlk
            elif c == min_cost and nmlk < min_nmlk:
                choosed = thing
                min_nmlk = nmlk
    return choosed

def step():
    thing = choose_unlock(unlocks)
    if num_unlocked(Unlocks.Sunflowers):
        world_size = get_world_size()
        world_area = world_size * world_size
        power_threshold = world_area
    else:
        power_threshold = 0
    auto_unlock(thing, power_threshold)
    if not get_cost(thing):
        unlocks.remove(thing)

while Unlocks.Leaderboard in unlocks:
    step()
