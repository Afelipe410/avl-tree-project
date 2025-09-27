class AVLNode:
    def __init__(self, key, obstacle):
        self.key = key
        self.obstacle = obstacle
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # ---------- rotaciones ----------
    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    # ---------- inserción ----------
    def insert(self, key, obstacle):
        self.root = self._insert(self.root, key, obstacle)

    def _insert(self, node, key, obstacle):
        if not node:
            return AVLNode(key, obstacle)
        if key < node.key:
            node.left = self._insert(node.left, key, obstacle)
        elif key > node.key:
            node.right = self._insert(node.right, key, obstacle)
        else:
            return node
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    # ---------- eliminación ----------
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self.get_min(node.right)
            node.key = temp.key
            node.obstacle = temp.obstacle
            node.right = self._delete(node.right, temp.key)
        if not node:
            return node
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def get_min(self, node):
        while node.left:
            node = node.left
        return node

    # ---------- limpieza de pasados ----------
    def remove_passed_obstacles(self, world_offset, margin=100):
        """Elimina del árbol los obstáculos que ya han sido superados por el jugador."""
        threshold = world_offset - margin
        self.root = self._remove_passed_recursive(self.root, threshold)

    def _remove_passed_recursive(self, node, threshold):
        """Recorre y elimina nodos recursivamente si su clave es menor que el umbral."""
        if not node:
            return None

        node.right = self._remove_passed_recursive(node.right, threshold)

        # Comparamos solo con la coordenada X de la clave
        if node.key[0] < threshold:
            return node.right
        else:
            node.left = self._remove_passed_recursive(node.left, threshold)
            return self._delete_balance(node)

    def _delete_balance(self, node):
        """Función auxiliar para rebalancear un nodo después de una eliminación."""
        if not node:
            return node

        self.update_height(node)
        balance = self.get_balance(node)

        # Caso Izquierda-Izquierda
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Caso Izquierda-Derecha
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Caso Derecha-Derecha
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Caso Derecha-Izquierda
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # ---------- recorridos ----------
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def bfs(self):
        if not self.root:
            return []
        result, queue = [], [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def _inorder(self, node, result):
        if not node:
            return
        self._inorder(node.left, result)
        result.append(node)
        self._inorder(node.right, result)

    def _preorder(self, node, result):
        if node:
            result.append(node)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node)

    # ---------- conversión ----------
    def to_obstacles(self):
        """Devuelve lista de dicts con obstáculos en orden por x_world."""
        return [n.obstacle for n in self.inorder()]
