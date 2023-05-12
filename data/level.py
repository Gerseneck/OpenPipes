from util import color


LEVELS = {
    0: {
        'name': 'Tutorial',
        'size': 5,
        'time': 8,
        'nodes': [
            ((0, 0), color.red), ((4, 1), color.red),
            ((0, 2), color.green), ((3, 1), color.green),
            ((1, 2), color.blue), ((4, 2), color.blue),
            ((0, 4), color.yellow), ((3, 3), color.yellow),
            ((1, 4), color.orange), ((4, 3), color.orange),
        ],
    },
    1: {
        'name': '5x5 Level 1',
        'size': 5,
        'time': 8,
        'nodes': [
            ((1, 3), color.red), ((2, 2), color.red),
            ((0, 3), color.green), ((4, 3), color.green),
            ((0, 2), color.blue), ((4, 0), color.blue),
            ((3, 0), color.yellow), ((0, 1), color.yellow),
            ((3, 3), color.orange), ((4, 2), color.orange),
        ],
    },
    2: {
        'name': '5x5 Level 2',
        'size': 5,
        'time': 7,
        'nodes': [
            ((0, 0), color.red), ((4, 0), color.red),
            ((2, 3), color.green), ((4, 2), color.green),
            ((0, 4), color.blue), ((4, 4), color.blue),
            ((1, 2), color.yellow), ((4, 3), color.yellow),
        ],
    },
    3: {
        'name': '7x7 Level 1', 
        'size': 7, 
        'nodes': [
            ((1, 0), color.blue), ((6, 0), color.blue), 
            ((4, 2), color.green), ((5, 5), color.green), 
            ((1, 1), color.red), ((4, 1), color.red), 
            ((2, 4), color.orange), ((5, 4), color.orange), 
            ((2, 0), color.yellow), ((2, 3), color.yellow),
        ],
    },
}
