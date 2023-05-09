from util import node, color


LEVELS = {
    1: {
        'size': 5,
        'nodes': [
            node((0, 0), color.red), node((4, 1), color.red),
            node((0, 2), color.green), node((3, 1), color.green),
            node((1, 2), color.blue), node((4, 2), color.blue),
            node((0, 4), color.yellow), node((3, 3), color.yellow),
            node((1, 4), color.orange), node((4, 3), color.orange)
        ],
    }
}
