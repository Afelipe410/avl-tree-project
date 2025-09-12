class AVLNode:
    def __init__(self, key, obstacle=None):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.obstacle = obstacle

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, key, obstacle=None):
        self.root = self._insert(self.root, key, obstacle)

    def _insert(self, node, key, obstacle):
        if not node:
            return AVLNode(key, obstacle)
        elif key < node.key:
            node.left = self._insert(node.left, key, obstacle)
        else:
            node.right = self._insert(node.right, key, obstacle)

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        bf = self.balance_factor(node)

        # Rotaciones
        if bf > 1 and key < node.left.key:
            return self.rotate_right(node)
        if bf < -1 and key > node.right.key:
            return self.rotate_left(node)
        if bf > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if bf < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def inorder(self):
        res = []
        def _in(n):
            if not n: return
            _in(n.left)
            res.append(n)
            _in(n.right)
        _in(self.root)
        return res

    def to_obstacles(self):
        nodes = self.inorder()
        return [n.obstacle for n in nodes if n.obstacle]
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """Imprime el árbol en consola con formato jerárquico"""
        node = node or self.root
        if not node:
            print("Árbol vacío")
            return
        print(" " * (level * 4) + prefix + f"({node.key})")
        if node.left:
            self.print_tree(node.left, level + 1, "L--- ")
        if node.right:
            self.print_tree(node.right, level + 1, "R--- ")