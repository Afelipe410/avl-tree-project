class AVLNode:
    def __init__(self, key, obstacle=None):
        """
        Inicializa un nodo del árbol AVL.

        Args:
            key: Clave para ordenar el nodo en el árbol.
            obstacle: Objeto obstáculo asociado al nodo (opcional).
        """
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.obstacle = obstacle

class AVLTree:
    def __init__(self):
        """
        Inicializa un árbol AVL vacío.
        """
        self.root = None

    def height(self, node):
        """
        Devuelve la altura de un nodo.

        Args:
            node: Nodo del árbol.

        Returns:
            int: Altura del nodo, 0 si es None.
        """
        return node.height if node else 0

    def balance_factor(self, node):
        """
        Calcula el factor de balance de un nodo.

        Args:
            node: Nodo del árbol.

        Returns:
            int: Diferencia de alturas entre los subárboles izquierdo y derecho.
        """
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        """
        Realiza una rotación simple a la derecha.

        Args:
            y: Nodo raíz del subárbol a rotar.

        Returns:
            AVLNode: Nueva raíz tras la rotación.
        """
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        return x

    def rotate_left(self, x):
        """
        Realiza una rotación simple a la izquierda.

        Args:
            x: Nodo raíz del subárbol a rotar.

        Returns:
            AVLNode: Nueva raíz tras la rotación.
        """
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, key, obstacle=None):
        """
        Inserta un nuevo nodo en el árbol AVL.

        Args:
            key: Clave del nodo.
            obstacle: Objeto obstáculo asociado (opcional).
        """
        self.root = self._insert(self.root, key, obstacle)

    def _insert(self, node, key, obstacle):
        """
        Inserta recursivamente un nodo en el árbol AVL y realiza balanceo.

        Args:
            node: Nodo actual.
            key: Clave del nuevo nodo.
            obstacle: Objeto obstáculo asociado.

        Returns:
            AVLNode: Nodo actualizado tras la inserción y balanceo.
        """
        if not node:
            return AVLNode(key, obstacle)
        elif key < node.key:
            node.left = self._insert(node.left, key, obstacle)
        else:
            node.right = self._insert(node.right, key, obstacle)

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        bf = self.balance_factor(node)

        # Rotaciones para mantener el balance
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
        """
        Realiza un recorrido en orden del árbol.

        Returns:
            list: Lista de nodos en orden ascendente por clave.
        """
        res = []
        def _in(n):
            if not n: return
            _in(n.left)
            res.append(n)
            _in(n.right)
        _in(self.root)
        return res

    def to_obstacles(self):
        """
        Obtiene una lista de los obstáculos almacenados en el árbol.

        Returns:
            list: Lista de objetos obstáculo.
        """
        nodes = self.inorder()
        return [n.obstacle for n in nodes if n.obstacle]
    
    def print_tree(self, node=None, level=0, prefix="Root: "):
        """
        Imprime el árbol en consola con formato jerárquico.

        Args:
            node: Nodo actual (por defecto la raíz).
            level: Nivel de profundidad para la indentación.
            prefix: Prefijo para mostrar la posición del nodo.
        """
        node = node or self.root
        if not node:
            print("Árbol vacío")
            return
        print(" " * (level * 4) + prefix + f"({node.key})")
        if node.left:
            self.print_tree(node.left, level + 1, "L--- ")
        if node.right:
            self.print_tree(node.right, level + 1, "R--- ")