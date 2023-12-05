import random

class Node:
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

class TreeNetwork:
    def __init__(self):
        self.root = None

    def find_path(self, node, target_val):
        path = []
        while node is not None:
            path.append(node)
            if node.val == target_val:
                break
            elif target_val < node.val:
                node = node.left
            else:
                node = node.right
        return path

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def splay(self, node):
        while node != self.root:
            if node.parent == self.root:
                # Perform one rotation (Zig step)
                if node == node.parent.left:
                    self.right_rotate(node.parent)
                else:
                    self.left_rotate(node.parent)
            else:
                grandparent = node.parent.parent
                if (node == node.parent.left) == (node.parent == grandparent.left):
                    # Zig-Zig step
                    self.right_rotate(grandparent)
                    self.right_rotate(node.parent)
                else:
                    # Zig-Zag step
                    if node == node.parent.left:
                        self.right_rotate(node.parent)
                        self.left_rotate(grandparent)
                    else:
                        self.left_rotate(node.parent)
                        self.right_rotate(grandparent)

    def adaptive_splay(self, path, p):
        for node in reversed(path):
            if random.random() <= p:
                self.splay(node)
                break

class RanDiSplayNet:
    def __init__(self, network):
        self.network = network
        self.p_min = 0.01  # Set minimum splaying probability

    def update_splay_prob(self, current_dest, previous_dest, p):
        if current_dest != previous_dest:
            return self.p_min
        else:
            return min(1, p * 2)

    def send_message(self, source_val, destination_val, previous_dest, p):
        # Find path from source to destination
        path = self.network.find_path(self.network.root, destination_val)

        # Update splay probability
        p = self.update_splay_prob(destination_val, previous_dest, p)

        # Perform adaptive splay
        self.network.adaptive_splay(path, p)

        # Return the updated splay probability and the total cost (length of the path)
        return p, len(path)

def main():
    network = TreeNetwork()

    # Input nodes for the tree
    nodes_input = input("Enter nodes for the tree (space-separated): ")
    nodes_list = list(map(int, nodes_input.split()))

    # Creating nodes for the tree
    for node_val in nodes_list:
        if network.root is None:
            network.root = Node(node_val)
        else:
            current = network.root
            while True:
                if node_val < current.val:
                    if current.left is None:
                        current.left = Node(node_val, parent=current)
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = Node(node_val, parent=current)
                        break
                    current = current.right

    rds_net = RanDiSplayNet(network)
    p_min = 0.01
    p = p_min
    previous_dest = None

    # Input message node pairs
    message_input = input("Enter message node pairs (e.g., '1 3, 4 2, 3 5'): ")
    message_pairs = [tuple(map(int, pair.split())) for pair in message_input.split(',')]

    total_cost = 0

    for source, destination in message_pairs:
        p, cost = rds_net.send_message(source, destination, previous_dest, p)
        previous_dest = destination
        total_cost += cost

    print(f"Total splay cost: {total_cost}")
    return 

# Execute the main function
main()
