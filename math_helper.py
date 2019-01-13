import math

def get_vector_rot(vector):
    if vector[0] != 0:
        degress = int(math.degrees(math.atan2(vector[1] / vector[0], 1)))
        if vector[0] < 0:
            if vector[1] > 0:
                return degress - 180
            return degress + 180
        return degress
    else:
        return 90 if vector[1] > 0 else -90

def direction_vec(start, end, normalize=True):
    """ return the direction between 2 points """
    vector = (end.x - start.x, end.y - start.y)
    if normalize and math.trunc(vector[0]) or math.trunc(vector[1]):
        hypot = (vector[0]**2+vector[1]**2) ** 0.5
        return vector[0]/hypot, vector[1]/hypot
    return vector

def euclid_distance(start=(0,0), end=(0,0)):
    return ((start[0]-end[0])**2 + (start[1]-end[1])**2) ** 0.5

if __name__ == "__main__":
    print(get_vector_rot((-1,-1)))