from queue import PriorityQueue
from typing import List

from foronoi.observers.message import Message
from foronoi.observers.subject import Subject
from foronoi.graphe.point import Point
from foronoi.graphe.half_edge import HalfEdge
from foronoi.graphe.vertex import Vertex
from foronoi.graphe.geometrie import Geometrie
from foronoi.graphe.polygon import Polygon
from foronoi.noeud.noeud_feuille import NoeudFeuille
from foronoi.noeud.arc import Arc
from foronoi.noeud.breakpoint import Breakpoint
from foronoi.noeud.noeud_interne import NoeudInterne
from foronoi.events.circle_event import CircleEvent
from foronoi.events.site_event import SiteEvent
from foronoi.arbre.noeud import Noeud
from foronoi.arbre.arbre_avl import Arbre_AVL


class Algorithm(Subject):
    def __init__(self, bounding_poly: Polygon = None, remove_zero_length_edges=True):
        super().__init__()

        # La bounding box
        self.bounding_poly: Polygon = bounding_poly
        self.bounding_poly.inherit_observers_from(self)

        self.event_queue = PriorityQueue()
        self.event = None

        self.status_tree: Noeud = None

        self.doubly_connected_edge_list = []

        self.sweep_line = float("inf")

        self._arcs = set()

        self.sites = None

        self.edges = list()

        self._vertices = set()
        self.remove_zero_length_edges = remove_zero_length_edges

    @property
    def arcs(self) -> List[Arc]:
        return list(self._arcs)

    @property
    def vertices(self) -> List[Vertex]:
        return list(self._vertices)

    def initialize(self, points):
        """
        Initialisation de la file de priorité avec tous les éléments.
        """

        # Store the points for visualization
        self.sites = points

        # Initialize event queue with all site events.
        for index, point in enumerate(points):
            # Create site event
            site_event = SiteEvent(point=point)
            self.event_queue.put(site_event)

        return self.event_queue

    def create_diagram(self, points: list):
        """
        Create the Voronoi diagram.

        The overall structure of the algorithm is as follows.

        1. Initialize the event queue `event_queue` with all site events, initialize an empty status structure
           `status_tree` and an empty doubly-connected edge list `D`.
        2. **while** `event_queue` is not empty.
        3.  **do** Remove the event with largest `y`-coordinate from `event_queue`.
        4.   **if** the event is a site event, occurring at site `point`
        5.    **then** :func:`~handle_site_event`
        6.    **else** :func:`handle_circle_event`
        7. The internal nodes still present in `status_tree` correspond to the half-infinite edges of the Voronoi
           diagram. Compute a bounding box (or polygon) that contains all vertices of  bounding box by updating the
           doubly-connected edge list appropriately.
        8. **If** `remove_zero_length_edges` is true.
        9.  Call :func:`~clean_up_zero_length_edges` which removes zero length edges and combines vertices with the same location into one.

        Parameters
        ----------
        points: list(Point)
            A set of point sites in the plane.

        Returns
        -------
        Output. The Voronoi diagram `Vor(P)` given inside a bounding box in a doublyconnected edge list `D`.
        """

        points = [Point(x, y) for x, y in points]

        # Initialize all points
        self.initialize(points)
        index = 0

        # The first point (needed for bounding box)
        genesis_point = None

        while not self.event_queue.empty():

            # Pop the event queue with the highest priority
            event = self.event_queue.get()

            # Set genesis point
            genesis_point = genesis_point or event.point

            # Handle circle events
            if isinstance(event, CircleEvent) and event.est_valide:
                # Update sweep line position
                self.sweep_line = event.yd

                # Debugging
                self.notify_observers(
                    Message.DEBUG,
                    payload=f"# Handle circle event at {event.yd:.3f} with center= {event.centre} and arcs= {event.point_triple}"
                )

                # Handle the event
                self.handle_circle_event(event)

            # Handle site events
            elif isinstance(event, SiteEvent):

                # Give the points a simple name
                event.point.nom = index
                index += 1

                # Update sweep line position
                self.sweep_line = event.yd

                # Debugging
                self.notify_observers(
                    Message.DEBUG,
                    payload=f"# Handle site event at y={event.yd:.3f} with point {event.point}"
                )

                # Handle the event
                self.handle_site_event(event)
            else:
                # Skip the step if circle event is no longer valid
                continue

            self.event = event
            self.notify_observers(Message.STEP_FINISHED)

        self.notify_observers(Message.DEBUG, payload="# Sweep finished")
        self.notify_observers(Message.SWEEP_FINISHED)

        # Finish with the bounding box
        self.edges = self.bounding_poly.finish_edges(
            edges=self.edges, vertices=self._vertices, points=self.sites, event_queue=self.event_queue
        )
        self.edges, self._vertices = self.bounding_poly.finish_polygon(self.edges, self._vertices, self.sites)

        if self.remove_zero_length_edges:
            self.clean_up_zero_length_edges()

        # Final visualization
        self.notify_observers(Message.DEBUG, payload="# Voronoi finished")
        self.notify_observers(Message.VORONOI_FINISHED)

    def handle_site_event(self, event: SiteEvent):
        """
        Handle a site event.

        1. Let :obj:`point_i = event.point`. If :attr:`status_tree` is empty, insert :obj:`point_i` into it (so that
           :attr:`status_tree` consists of a single leaf storing :obj:`point_i`) and return. Otherwise, continue with
           steps 2– 5.
        2. Search in :attr:`status_tree` for the arc :obj:`α` vertically above :obj:`point_i`. If the leaf
           representing :obj:`α` has a pointer to a circle event in :attr:`event_queue`, then this circle event is a
           false alarm and it must be deleted from :attr:`status_tree`.
        3. Replace the leaf of :attr:`status_tree` that represents :obj:`α` with a subtree having three leaves.
           The middle leaf stores the new site :obj:`point_i` and the other two leaves store the site
           :obj:`point_j` that was originally stored with :obj:`α`. Store the breakpoints
           (:obj:`point_j`, :obj:`point_i`) and (:obj:`point_i`, :obj:`point_j`) representing the new breakpoints at the
           two new internal nodes. Perform rebalancing operations on :attr:`status_tree` if necessary.
        4. Create new half-edge records in the Voronoi diagram structure for the
           edge separating the faces for :obj:`point_i` and :obj:`point_j`, which will be traced out by the two new
           breakpoints.
        5. Check the triple of consecutive arcs where the new arc for pi is the left arc
           to see if the breakpoints converge. If so, insert the circle event into :attr:`status_tree` and
           add pointers between the node in :attr:`status_tree` and the node in :attr:`event_queue`. Do the same for the
           triple where the new arc is the right arc.

        Parameters
        ----------
        event: SiteEvent
            The site event to handle.
        """

        # Create a new arc
        point_i = event.point
        new_arc = Arc(origine=point_i)
        self._arcs.add(new_arc)

        # 1. If the beach line tree is empty, we insert point
        if self.status_tree is None:
            self.status_tree = NoeudFeuille(new_arc)
            return

        # 2. Search the beach line tree for the arc above the point
        arc_node_above_point = Arbre_AVL.chercher_noeud_feuille(self.status_tree, cle=point_i.xd, sweep_line=self.sweep_line)
        arc_above_point = arc_node_above_point.get_value()

        # Remove potential false alarm
        if arc_above_point.circle_event is not None:
            arc_above_point.circle_event.fausse_alerte()

        # 3. Replace leaf with new sub tree that represents the two new intersections on the arc above the point
        #
        #            (p_j, p_i)
        #              /     \
        #             /       \
        #           p_j    (p_i, p_j)
        #                   /     \
        #                  /       \
        #                p_i       p_j
        point_j = arc_above_point.origine
        breakpoint_left = Breakpoint(breakpoint=(point_j, point_i))
        breakpoint_right = Breakpoint(breakpoint=(point_i, point_j))

        root = NoeudInterne(breakpoint_left)
        root.gauche = NoeudFeuille(Arc(origine=point_j, circle_event=None))

        # Only insert right breakpoint into the tree if it actually intersects
        if breakpoint_right.s_intersectent():
            root.droite = NoeudInterne(breakpoint_right)
            root.droite.gauche = NoeudFeuille(new_arc)
            root.droite.droite = NoeudFeuille(Arc(origine=point_j, circle_event=None))
        else:
            root.droite = NoeudFeuille(new_arc)

        self.status_tree = arc_node_above_point.remplacer_feuille(replacement=root, racine=self.status_tree)

        # 4. Create half edge records
        A, B = point_j, point_i
        AB = breakpoint_left
        BA = breakpoint_right

        # Edge AB -> BA with incident point B
        AB.edge = HalfEdge(B, origine=AB)

        # Edge BA -> AB with incident point A
        BA.edge = HalfEdge(A, origine=BA, jumelle=AB.edge)

        # Append one of the edges to the list (we can get the other by using jumelle)
        self.edges.append(AB.edge)

        # Add first edges
        B.arete_entree = B.arete_entree or AB.edge
        A.arete_entree = A.arete_entree or BA.edge

        # 5. Check if breakpoints are going to converge with the arcs to the left and to the right
        #
        #            (p_j, p_i)
        #  \           /     \
        #   \         /       \
        # node_a ... node_b   (p_i, p_j)
        #                   /     \              /
        #                  /       \            /
        #              node_c    node_d ... node_e
        #

        # If the right breakpoint does not intersect, we don't need to insert circle events.
        if not breakpoint_right.s_intersectent():
            return

        node_a, node_b, node_c = root.gauche.predecessor, root.gauche, root.droite.gauche
        node_c, node_d, node_e = node_c, root.droite.droite, root.droite.droite.successor

        self._check_circles((node_a, node_b, node_c), (node_c, node_d, node_e))

        # X. Rebalance the tree
        self.status_tree = Arbre_AVL.equilibrer_et_propager(root)

    def handle_circle_event(self, event: CircleEvent):
        """
        Handle a circle event.

        1. Delete the leaf :obj:`γ` that represents the disappearing arc :obj:`α` from :attr:`status_tree`. Update
           the tuples representing the breakpoints at the internal nodes. Perform
           rebalancing operations on :attr:`status_tree` if necessary. Delete all circle events involving
           :obj:`α` from :attr:`event_queue`; these can be found using the pointers from the predecessor and
           the successor of :obj:`γ` in :attr:`status_tree`. (The circle event where :obj:`α` is the middle arc is
           currently being handled, and has already been deleted from :attr:`event_queue`.)
        2. Add the center of the circle causing the event as a vertex record to the
           doubly-connected edge list :obj:`D` storing the Voronoi diagram under construction. Create two half-edge
           records corresponding to the new breakpoint
           of the beach line. Set the pointers between them appropriately. Attach the
           three new records to the half-edge records that end at the vertex.
        3. Check the new triple of consecutive arcs that has the former left neighbor
           of :obj:`α` as its middle arc to see if the two breakpoints of the triple converge.
           If so, insert the corresponding circle event into :attr:`event_queue`. and set pointers between
           the new circle event in :attr:`event_queue` and the corresponding leaf of :attr:`status_tree`. Do the same
           for the triple where the former right neighbor is the middle arc.

        Parameters
        ----------
        event

        Returns
        -------

        """

        # 1. Delete the leaf γ that represents the disappearing arc α from T.
        arc = event.arc_pointer.data
        if arc in self._arcs:
            self._arcs.remove(arc)
        arc_node: NoeudFeuille = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor

        # Update breakpoints
        self.status_tree, updated, removed, left, right = self._update_breakpoints(
            self.status_tree, self.sweep_line, arc_node, predecessor, successor)

        if updated is None:
            # raise Exception("Oh.")
            return

        # Delete all circle events involving arc from the event queue.
        def remove(neighbor_event):
            if neighbor_event is None:
                return None
            self.notify_observers(Message.DEBUG, payload=f"Circle event for {neighbor_event.yd} removed.")
            return neighbor_event.fausse_alerte()

        remove(predecessor.get_value().circle_event)
        remove(successor.get_value().circle_event)

        # 2. Create half-edge records

        # Get the location where the breakpoints converge
        convergence_point = event.centre

        # Create a new edge for the new breakpoint, where the edge originates in the new breakpoint
        # Note: we only create the new edge if the vertex is still inside the bounding box
        # if self.bounding_poly.inside(event.center):
        # Create a vertex
        v = Vertex(convergence_point.xd, convergence_point.yd)
        self._vertices.add(v)

        # Connect the two old edges to the vertex
        updated.edge.origine = v
        removed.edge.origine = v
        v.connected_edges.append(updated.edge)
        v.connected_edges.append(removed.edge)

        # Get the incident points
        breakpoint_a = updated.breakpoint[0]
        breakpoint_b = updated.breakpoint[1]

        # Create a new edge that originates from the new vertex v,
        # and points towards the newly updated (moving) breakpoint.
        new_edge = HalfEdge(breakpoint_a, origine=v, jumelle=HalfEdge(breakpoint_b, origine=updated))

        # Set previous and next
        left.edge.jumelle.set_suiv(new_edge)  # yellow
        right.edge.jumelle.set_suiv(left.edge)  # orange
        new_edge.jumelle.set_suiv(right.edge)  # blue

        # Add to list for visualization
        self.edges.append(new_edge)

        # Add the new_edge to the list of connected edges of the vertex
        v.connected_edges.append(new_edge)

        # Let the updated breakpoint point back to the new edge
        updated.edge = new_edge.jumelle

        # 3. Check if breakpoints converge for the triples with former left and former right as middle arcs
        former_left = predecessor
        former_right = successor

        node_a, node_b, node_c = former_left.predecessor, former_left, former_left.successor
        node_d, node_e, node_f = former_right.predecessor, former_right, former_right.successor

        self._check_circles((node_a, node_b, node_c), (node_d, node_e, node_f))

    def _check_circles(self, triple_left, triple_right):
        node_a, node_b, node_c = triple_left
        node_d, node_e, node_f = triple_right

        left_event = CircleEvent.creer_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line)
        right_event = CircleEvent.creer_circle_event(node_d, node_e, node_f, sweep_line=self.sweep_line)

        # Check if the circles converge
        if left_event:
            if not Geometrie.angle_est_horaire(node_a.data.origine, node_b.data.origine, node_c.data.origine,
                                           left_event.centre):
                self.notify_observers(Message.DEBUG, payload=f"Circle {left_event.point_triple} not clockwise.")
                left_event = None

        if right_event:
            if not Geometrie.angle_est_horaire(node_d.data.origine, node_e.data.origine, node_f.data.origine,
                                           right_event.centre):
                self.notify_observers(Message.DEBUG, payload=f"Circle {right_event.point_triple} not clockwise.")
                right_event = None

        if left_event is not None:
            self.event_queue.put(left_event)
            node_b.data.circle_event = left_event

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)
            node_e.data.circle_event = right_event

        if left_event is not None:
            self.notify_observers(Message.DEBUG,
                                  payload=f"Left circle event created for {left_event.yd}. Arcs: {left_event.point_triple}")
        if right_event is not None:
            self.notify_observers(Message.DEBUG,
                                  payload=f"Right circle event created for {right_event.yd}. Arcs: {right_event.point_triple}")

        return left_event, right_event

    @staticmethod
    def _update_breakpoints(root, sweep_line, arc_node, predecessor, successor):

        # If the arc node is a left child, then its parent is the node with right_breakpoint
        if arc_node.is_left_child():

            # Replace the right breakpoint by the right node
            root = arc_node.parent.remplacer_feuille(arc_node.parent.droite, root)

            # Mark the right breakpoint as removed and right breakpoint
            removed = arc_node.parent.data
            right = removed

            # Rebalance the tree
            root = Arbre_AVL.equilibrer_et_propager(root)

            # Find the left breakpoint
            left_breakpoint = Breakpoint(breakpoint=(predecessor.get_value().origine, arc_node.get_value().origine))
            query = NoeudInterne(left_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint: NoeudInterne = Arbre_AVL.chercher_valeur(root, query, compare, sweep_line=sweep_line)

            # Update the breakpoint
            # assert(breakpoint is not None)
            if breakpoint is not None:
                breakpoint.data.breakpoint = (breakpoint.get_value().breakpoint[0], successor.get_value().origine)

            # Mark this breakpoint as updated and left breakpoint
            updated = breakpoint.data if breakpoint is not None else None
            left = updated

        # If the arc node is a right child, then its parent is the breakpoint on the left
        else:

            # Replace the left breakpoint by the left node
            root = arc_node.parent.remplacer_feuille(arc_node.parent.gauche, root)

            # Mark the left breakpoint as removed
            removed = arc_node.parent.data
            left = removed

            # Rebalance the tree
            root = Arbre_AVL.equilibrer_et_propager(root)

            # Find the right breakpoint
            right_breakpoint = Breakpoint(breakpoint=(arc_node.get_value().origine, successor.get_value().origine))
            query = NoeudInterne(right_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint: NoeudInterne = Arbre_AVL.chercher_valeur(root, query, compare, sweep_line=sweep_line)

            # Update the breakpoint
            # assert(breakpoint is not None)
            if breakpoint is not None:
                breakpoint.data.breakpoint = (predecessor.get_value().origine, breakpoint.get_value().breakpoint[1])

            # Mark this breakpoint as updated and right breakpoint
            updated = breakpoint.data if breakpoint is not None else None
            right = updated

        return root, updated, removed, left, right

    def clean_up_zero_length_edges(self):
        """
        Removes zero length edges and vertices with the same coordinate
        that are produced when two site-events happen at the same time.
        """

        resulting_edges = []
        for edge in self.edges:
            start = edge.get_origine()
            end = edge.jumelle.get_origine()
            if start.xd == end.xd and start.yd == end.yd:

                # Combine the vertices
                v1: Vertex = edge.origine
                v2: Vertex = edge.jumelle.origine

                # Move connected edges from v1 to v2
                for connected in v1.connected_edges:
                    connected.origine = v2
                    v1.connected_edges.remove(connected)
                    v2.connected_edges.append(connected)

                # Remove vertex v1
                self._vertices.remove(v1)

                # Delete the edge
                edge.supprimer()
                edge.jumelle.supprimer()

            else:
                resulting_edges.append(edge)
            self.edges = resulting_edges
