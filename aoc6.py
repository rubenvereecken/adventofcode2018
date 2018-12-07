from functools import partial
import numpy as np

def read_lines():
    import sys
    raw = sys.stdin.read()

    for line in raw.splitlines():
        if not line: continue
        yield line

def read_coords():
    for line in read_lines():
        yield eval('({})'.format(line))


import enum
class Marker(enum.Enum):
    EMPTY = -1
    SHARED = -2

def get_neighbours(grid, cell):
    if cell[0] > 0:
        yield cell[0]-1, cell[1]
    if cell[1] > 0:
        yield cell[0], cell[1]-1
    if cell[0] < grid.shape[0]-1:
        yield cell[0]+1, cell[1]
    if cell[1] < grid.shape[1]-1:
        yield cell[0], cell[1]+1


def part_one():
    coords = list(read_coords())
    topleft = (0, 0)
    bottomright = (max(cell[0] for cell in coords)+1,
                   max(cell[1] for cell in coords)+1)
    grid = np.ones(bottomright, dtype=np.int8) * -1

    # Store here Manhattan distances
    grid_distances = np.zeros_like(grid)
    neighbours = partial(get_neighbours, grid)

    fringe = [] # Pretend this is a queue alright

    # Initialise the fringe with all distance=1
    for coord_idx, coord in enumerate(coords):
        for neighbour in neighbours(coord):
            if neighbour in coords: continue
            fringe.append((neighbour, coord_idx, 1))

    while fringe:
        cell, parent_idx, distance = fringe.pop(0)

        # Already has influence, means it's shared
        if grid[cell] >= 0 and grid_distances[cell] == distance:
            # Ignore if this is part of the same region
            if grid[cell] == parent_idx:
                continue
            grid[cell] = Marker.SHARED.value
        elif grid[cell] >= 0 and grid_distances[cell] > distance:
            assert False, "Impossible really"
        elif grid[cell] >= 0 and grid_distances[cell] < distance:
            assert grid_distances[cell] != 0, 'Havent even been'
            # This one has already been covered, abort
            pass
        elif grid[cell] == -1:
            assert grid[cell] < 0
            # Mark it with the parent
            grid[cell] = parent_idx
            grid_distances[cell] = distance

            for neighbour in neighbours(cell):
                # Skip beacons
                if neighbour in coords: continue
                # Don't re-do cells beloning to the same beacon
                if grid[neighbour] == parent_idx: continue
                fringe.append((neighbour, parent_idx, distance+1))
        else:
            # Already marked as shared
            assert grid[cell] == Marker.SHARED.value

    # The ones on the sides go on foreeeever
    infinite_idxs = np.unique(np.hstack([
        grid[0], grid[-1], grid[:,0], grid[:,-1]
    ]))
    sizes = [np.sum(grid == i) for i in range(len(coords))]
    largest = max(enumerate(sizes), key=lambda s: s[1] if s[0] not in infinite_idxs else 0)
    # idx, size
    print(largest)



if __name__ == "__main__":
    part_one()

