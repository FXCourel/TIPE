class Noeud:
    def __init__(self, data):
        """
        A smart tree node with some extra functionality over standard nodes.
        :param data: Data that is stored inside the node.
        """
        self.data = data
        self._gauche = None
        self._droite = None
        self._hauteur = None
        self.parent = None

    def __repr__(self):
        return f"Noeud({self.data}, left={self.gauche}, right={self.droite})"

    @property
    def gauche(self) -> "Noeud":
        return self._gauche

    @property
    def droite(self) -> "Noeud":
        return self._droite

    @property
    def grandparent(self):
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.parent

    def get_key(self, **kwargs):
        return self.data

    def get_value(self, **kwargs):
        return self.data

    def get_label(self, **kwargs):
        return f"{self.get_key(**kwargs)}({self.hauteur})"

    @gauche.setter
    def gauche(self, node):

        if node is not None:

            # Tell the child who its new parent is
            node.parent = self

        self._gauche = node

    @droite.setter
    def droite(self, node):

        if node is not None:

            # Tell the child who its new parent is
            node.parent = self

        self._droite = node

    @property
    def hauteur(self):
        if self._hauteur is None:
            self._hauteur = self.calculer_hauteur()
        return self._hauteur

    @property
    def equilibre(self):
        left_height = self.gauche.hauteur if self.gauche is not None else 0
        right_height = self.droite.hauteur if self.droite is not None else 0
        return left_height - right_height

    def calculer_hauteur(self):
        """
        Recursively calculate height of this node.
        Height calculated for each node will be stored, so calculations need to be done only once.
        :return: (int) Height of the current node
        """
        left_height = self.gauche.hauteur if self.gauche is not None else 0
        right_height = self.droite.hauteur if self.droite is not None else 0
        height = 1 + max(left_height, right_height)
        return height

    def maj_hauteur(self):
        """
        Recalculate the height of the node.
        """
        self._hauteur = self.calculer_hauteur()

    def maj_hauteurs(self):
        """
        Recalculate the heights of this node and all ancestor nodes.
        """

        # Calculate height
        self.maj_hauteur()

        # Update parent
        if self.parent is not None:
            self.parent.maj_hauteurs()

    def is_left_child(self):
        """
        Determines whether this node is a left child.
        :return: (bool) True if this node is a left child, False otherwise
        """
        if self.parent is None:
            return False
        return self.parent.gauche == self

    def is_right_child(self):
        """
        Determines whether this node is a right child.
        :return: (bool) True if this node is a right child, False otherwise
        """
        if self.parent is None:
            return False
        return self.parent.droite == self

    def is_leaf(self):
        """
        Determines whether this node is a leaf.
        :return: (bool) True if this node is a leaf, False otherwise
        """
        return self.gauche is None and self.droite is None

    def minimum(self):
        """
        Determines the node with the smallest key in the subtree rooted by this node.
        :return: (Noeud) Noeud with the smallest key
        """
        current = self
        while current.gauche is not None:
            current = current.gauche
        return current

    def maximum(self):
        """
        Determines the node with the largest key in the subtree rooted by this node.
        :return: (Noeud) Noeud with the largest key
        """
        current = self
        while current.droite is not None:
            current = current.droite
        return current

    @property
    def successor(self):
        """
        Returns the node with the smallest key larger than this node's key, or None
        if this node has the largest key in the tree.
        """

        # If the node has a right sub tree, take the minimum
        if self.droite is not None:
            return self.droite.minimum()

        # Walk up to the left until we are no longer a right child
        current = self
        while current.is_right_child():
            current = current.parent

        # Check there is a right branch
        if current.parent is None or current.parent.droite is None:
            return None

        # Step over to the right branch, and take the minimum
        return current.parent.droite.minimum()

    @property
    def predecessor(self):
        """
        Returns the node with the largest key smaller than this node's key, or None
        if this node has the smallest key in the tree.
        """

        # If the node has a left sub tree, take the maximum
        if self.gauche is not None:
            return self.gauche.maximum()

        # Walk up to the right until we are no longer a left child
        current = self
        while current.is_left_child():
            current = current.parent

        # Check there is a left branch
        if current.parent is None or current.parent.gauche is None:
            return None

        # Step over to the left branch, and take the maximum
        return current.parent.gauche.maximum()

    def remplacer_feuille(self, replacement, racine):
        """
        Replace the node by a replacement tree.
        Requires the current node to be a leaf.

        :param replacement: (Noeud) The root node of the replacement sub tree
        :param root: (Noeud) The root of the tree
        :return: (Noeud) The root of the updated tree
        """

        # Give the parent of the node to the replacement
        if replacement is not None:
            replacement.parent = self.parent

        # If node is left child, replace it by giving the parent a new left node
        if self.is_left_child():
            self.parent.gauche = replacement

        # If node is right child, replace it by giving the parent a new right node
        elif self.is_right_child():
            self.parent.droite = replacement

        # Otherwise, replace the root
        else:
            racine = replacement

        # For non-empty replacement, start updating heights from replacement's root
        if replacement is not None:
            replacement.maj_hauteurs()

        # For empty replacement, start updating heights from the parent
        elif self.parent is not None:
            self.parent.maj_hauteurs()

        # Return the new tree. No need to return the replacement, because the
        # reference remains the same.
        return racine

    def visualize(self):
        return self._visualize()

    def _visualize(self, depth=0):
        """
        Visualize the node and its descendants.

        :param depth: (int) Used by the recursive formula, should be left at the default value
        :return: (str) String representation of the visualization
        """
        ret = ""

        # Print right branch
        if self.droite is not None:
            ret += self.droite._visualize(depth + 1)

        # Print own value
        ret += "\n" + ("    " * depth) + str(self.get_label())

        # Print left branch
        if self.gauche is not None:
            ret += self.gauche._visualize(depth=depth + 1)

        return ret
