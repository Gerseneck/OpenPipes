from util import node, color


LEVELS = {
    0: {
        'name': 'Tutorial',
        'size': 5,
        'time': 8,
        'nodes': [
            node((0, 0), color.red), node((4, 1), color.red),
            node((0, 2), color.green), node((3, 1), color.green),
            node((1, 2), color.blue), node((4, 2), color.blue),
            node((0, 4), color.yellow), node((3, 3), color.yellow),
            node((1, 4), color.orange), node((4, 3), color.orange)
        ],
    },
    1: {
        'name': '5x5 Level 1',
        'size': 5,
        'time': 8,
        'nodes': [
            node((1, 3), color.red), node((2, 2), color.red),
            node((0, 3), color.green), node((4, 3), color.green),
            node((0, 2), color.blue), node((4, 0), color.blue),
            node((3, 0), color.yellow), node((0, 1), color.yellow),
            node((3, 3), color.orange), node((4, 2), color.orange)
        ]
    },
}
