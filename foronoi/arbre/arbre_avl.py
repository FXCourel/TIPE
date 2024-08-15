from foronoi.noeud import Arc, Breakpoint
from foronoi.arbre.noeud import Noeud


class Arbre_AVL:
    """
    Arbre auto-équilibré.
    """

    @staticmethod
    def chercher(root: Noeud, key, **kwargs):

        node = root
        while node is not None:
            if key == node.get_key(**kwargs):
                break
            elif key < node.get_key(**kwargs):
                node = node.gauche
            else:
                node = node.droite
        return node

    @staticmethod
    def chercher_valeur(racine: Noeud, requete: Noeud, compare=lambda x, y: x == y, **kwargs):
        """
        Cherche un noeud dans l'arbre en utilisant une requête. La fonction compare est utilisée pour comparer les valeurs.
        """
        cle = requete.get_key(**kwargs)
        noeud = racine
        while noeud is not None:
            if cle == noeud.get_key(**kwargs):

                if compare(noeud.data, requete.data):
                    return noeud

                gauche = Arbre_AVL.chercher_valeur(noeud.gauche, requete, compare, **kwargs)
                if gauche is None:
                    droite = Arbre_AVL.chercher_valeur(noeud.droite, requete, compare, **kwargs)
                    return droite

                return gauche

            elif cle < noeud.get_key(**kwargs):
                return Arbre_AVL.chercher_valeur(noeud.gauche, requete, compare, **kwargs) or \
                       Arbre_AVL.chercher_valeur(noeud.droite, requete, compare, **kwargs)
            else:
                return Arbre_AVL.chercher_valeur(noeud.droite, requete, compare, **kwargs) or \
                       Arbre_AVL.chercher_valeur(noeud.gauche, requete, compare, **kwargs)

    @staticmethod
    def chercher_noeud_feuille(racine: Noeud, cle, **kwargs):
        """
        Suit un chemin entre les noeuds internes de l'arbre jusqu'à trouver une feuille.
        """

        noeud = racine
        while noeud is not None:

            if noeud.is_leaf():
                return noeud

            # If we found the key, we choose a direction
            elif cle == noeud.get_key(**kwargs) and not noeud.is_leaf():

                # Chemin de gauche si possible
                if noeud.gauche is not None:
                    return noeud.gauche.maximum()

                # Sinon on va à droite
                return noeud.droite.minimum()

            # Recherche du noeud en fonction de la clé
            elif cle < noeud.get_key(**kwargs):
                noeud = noeud.gauche
            else:
                noeud = noeud.droite

        return noeud

    @staticmethod
    def inserer(racine: Noeud, noeud: Noeud, **kwargs):

        node_key = noeud.get_key(**kwargs) if noeud is not None else None
        root_key = racine.get_key(**kwargs) if racine is not None else None

        # Insertion avec direction
        if racine is None:
            return noeud
        elif node_key < root_key:
            racine.gauche = Arbre_AVL.inserer(racine.gauche, noeud, **kwargs)
        else:
            racine.droite = Arbre_AVL.inserer(racine.droite, noeud, **kwargs)

        # Mise à jour de la hauteur du noeud
        racine.maj_hauteur()

        # Si l'arbre est deséquilibré alors on le rééquilibre
        equilibre = racine.equilibre
        # root = Arbre_AVL.balance(root)

        # Cas 1 - Gauche Gauche
        if equilibre > 1 and node_key < racine.gauche.get_key(**kwargs):
            return Arbre_AVL.rotation_droite(racine)

        # Cas 2 - Droite Droite
        if equilibre < -1 and node_key > racine.droite.get_key(**kwargs):
            return Arbre_AVL.rotation_gauche(racine)

        # Cas 3 - Gauche Droite
        if equilibre > 1 and node_key > racine.gauche.get_key(**kwargs):
            racine.gauche = Arbre_AVL.rotation_gauche(racine.gauche)
            return Arbre_AVL.rotation_droite(racine)

        # Cas 4 - Droite Gauche
        if equilibre < -1 and node_key < racine.droite.get_key(**kwargs):
            racine.droite = Arbre_AVL.rotation_droite(racine.droite)
            return Arbre_AVL.rotation_gauche(racine)

        return racine

    @staticmethod
    def supprimer(racine: Noeud, key: int, **kwargs):

        if racine is None:
            return racine

        elif key < racine.get_key():
            racine.gauche = Arbre_AVL.supprimer(racine.gauche, key)

        elif key > racine.get_key():
            racine.droite = Arbre_AVL.supprimer(racine.droite, key)

        else:
            if racine.gauche is None:
                return racine.droite

            elif racine.droite is None:
                return racine.gauche

            temp = racine.droite.minimum()
            racine.data = temp.data
            racine.droite = Arbre_AVL.supprimer(racine.droite, temp.value.get_key(**kwargs))

        if racine is None:
            return racine

        racine.maj_hauteur()
        racine = Arbre_AVL.equilibrer(racine)

        return racine

    @staticmethod
    def equilibrer_et_propager(noeud):

        noeud = Arbre_AVL.equilibrer(noeud)

        if noeud.parent is None:
            return noeud

        return Arbre_AVL.equilibrer_et_propager(noeud.parent)

    @staticmethod
    def equilibrer(noeud: Noeud):

        # Si l'arbre est deséquilibré alors on le rééquilibre

        # Case 1 - Gauche Gauche
        if noeud.equilibre > 1 and noeud.gauche.equilibre >= 0:
            return Arbre_AVL.rotation_droite(noeud)

        # Case 2 - Droite Droite
        if noeud.equilibre < -1 and noeud.droite.equilibre <= 0:
            return Arbre_AVL.rotation_gauche(noeud)

        # Case 3 - Gauche Droite
        if noeud.equilibre > 1 and noeud.gauche.equilibre < 0:
            noeud.gauche = Arbre_AVL.rotation_gauche(noeud.gauche)
            return Arbre_AVL.rotation_droite(noeud)

        # Case 4 - Droite Gauche
        if noeud.equilibre < -1 and noeud.droite.equilibre > 0:
            noeud.droite = Arbre_AVL.rotation_droite(noeud.droite)
            return Arbre_AVL.rotation_gauche(noeud)

        return noeud

    @staticmethod
    def rotation_gauche(z):

        grandparent = z.parent
        y = z.droite
        T2 = y.gauche

        y.parent = grandparent

        if grandparent is not None:
            if z.is_left_child():
                grandparent.gauche = y
            else:
                grandparent.droite = y

        y.gauche = z
        z.droite = T2

        z.maj_hauteur()
        y.maj_hauteur()

        return y

    @staticmethod
    def rotation_droite(z):
        """
        Rotate tree to the right.
        """
        grandparent = z.parent
        y = z.gauche
        T3 = y.droite

        y.parent = grandparent

        if grandparent is not None:
            if z.is_left_child():
                grandparent.gauche = y
            else:
                grandparent.droite = y

        y.droite = z
        z.gauche = T3

        z.maj_hauteur()
        y.maj_hauteur()

        return y

    @staticmethod
    def get_leaves(root: Noeud, leaves=None):
        if leaves is None:
            leaves = []

        # Base case
        if root.is_leaf():
            leaves.append(root)
            return leaves

        # Step
        if root.gauche is not None:
            leaves += Arbre_AVL.get_leaves(root.gauche, None)
        if root.droite is not None:
            leaves += Arbre_AVL.get_leaves(root.droite, None)
        return leaves
