from robots.geometrie.point import Point

class Algos:

    @staticmethod
    # parcours_de_graham permet de déterminer une enveloppe convexe à partir d'un ensemble de points
    def parcours_de_graham(nuage: list[Point], points_redondants_possibles: bool = True):

        if len(nuage) <= 1:
            return nuage

        if points_redondants_possibles:
            nuage = list(set(nuage))
            
        assert len (nuage) >= 3, "Il faut au moins 3 points pour déterminer une enveloppe convexe"

        # Trouver le point le plus bas à gauche
        pivot = nuage[0]
        for point in nuage:
            if point.y < pivot.y:
                pivot = point
            elif point.y == pivot.y:
                if point.x < pivot.x:
                    pivot = point

        nuage.remove(pivot)
        nuage.sort(key=lambda point: point.angle(pivot))
        nuage.insert(0, pivot)

        # Recherche du parcours de Graham
        poly_convexe = [nuage[0], nuage[1]]

        for i in range(2, len(nuage)):
            while len(poly_convexe) >= 2 and nuage[i].est_a_droite(poly_convexe[-2], poly_convexe[-1]):
                poly_convexe.pop()
            poly_convexe.append(nuage[i])
        return poly_convexe

    @staticmethod
    def sur_segment(p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False
    
    @staticmethod
    def orientation(p, q, r):      
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            # orientation sens horaire
            return 1
        elif (val < 0):
            return 2 # orientation sens anti-horaire
        else:
            return 0 # Colinéaires

    @staticmethod
    def se_coupent(p1,q1,p2,q2):
        
        # Trouve les 4 orientations requises pour
        # les cas généraux et spéciaux
        o1 = Algos.orientation(p1, q1, p2)
        o2 = Algos.orientation(p1, q1, q2)
        o3 = Algos.orientation(p2, q2, p1)
        o4 = Algos.orientation(p2, q2, q1)
    
        if ((o1 != o2) and (o3 != o4)):
            return True
        
        # p1 , q1 et p2 sont colineaires p2 se situe sur le segment p1q1
        if ((o1 == 0) and Algos.sur_segment(p1, p2, q1)):
            return True
        # p1 , q1 et q2 sont colineaires q2 se situe sur le segment p1q1
        if ((o2 == 0) and Algos.sur_segment(p1, q2, q1)):
            return True
        # p2 , q2 et p1 sont colineaires p1 se situe sur le segment p2q2
        if ((o3 == 0) and Algos.sur_segment(p2, p1, q2)):
            return True
        # p2 , q2 et q1 sont colineaires q1 se situe sur le segment p2q2
        if ((o4 == 0) and Algos.sur_segment(p2, q1, q2)):
            return True
        return False



if __name__ == "__main__":
    print("Ce fichier ne peut pas être exécuté directement, éxécuter le fichier main.py")