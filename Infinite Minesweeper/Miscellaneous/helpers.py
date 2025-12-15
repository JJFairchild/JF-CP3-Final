def area(x,y):
    """Function used to find the coordinates of a tile's neighbors."""
    area = []
    for x_off in range(-1, 2):
        for y_off in range(-1, 2):
            if (x_off,y_off) != (0,0):
                area.append((x+x_off,y+y_off))
    return area


def difficulty(prob):
    """Return a human-friendly difficulty string for a mine probability."""
    try:
        prob = float(prob)
    except Exception:
        return "unknown"

    if prob <= 0.15:
        return 'easy'
    elif prob <= 0.2:
        return 'intermediate'
    elif prob <= 0.25:
        return 'hard'
    elif prob <= 0.3:
        return 'expert'
    else:
        return 'impossible'