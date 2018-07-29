class Node:
    def __init__(self, data):
        self.data = data 
        self.left = None
        self.right = None
    def looks(self):
        return self.data, self.left.data, self.right.data


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.left.left.left = Node(6)

def maxmum_height(node):
    if node is None:
        return 0
    else:
        lDepth = maxmum_height(node.left)
        rDepth = maxmum_height(node.right)

        if (lDepth > rDepth):
            return lDepth + 1
        else:
            return rDepth + 1

print(maxmum_height(root))

def middle_order(node):
    if node:
        middle_order(node.left)
        print(node.data)
        middle_order(node.right)


def identicalTrees(a, b):
     
    # 1. Both empty
    if a is None and b is None:
        return True
 
    # 2. Both non-empty -> Compare them
    if a is not None and b is not None:
        return ((a.data == b.data) and
                identicalTrees(a.left, b.left)and
                identicalTrees(a.right, b.right))
     
    # 3. one empty, one not -- false
    return False


def delete_tree(node):
    if node is None:
        return True
    else:
        delete_tree(node.left)
        delete_tree(node.right)
        node.data = 0 
# https://www.geeksforgeeks.org/given-a-binary-tree-print-out-all-of-its-root-to-leaf-paths-one-per-line/

def printPaths():

def printRecr(node, seq):
    if node is None:
        return ""
    else:
        seq.add(node.data)
        printRecr(node.left, seq)
        printRecr(node.right, seq)




