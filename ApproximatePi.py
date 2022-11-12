#!/usr/bin/env python3

"""
Module qui se charge de faire la simulation de Monte-Carlo pour obtenir une approximation de π.
"""

from random import random
import sys


def monte_carlo_pi(nb_pts):
    """
    Fonction faisant la simulation de Monte-Carlo en tirant nb_pts points aléatoires pour approximer π.
    Cette fonction retourne le nombre de points qui sont dans le cercle, ainsi
    qu'une liste de tuples de 3 éléments : les 2 premiers éléments représentent
    le point générés et le dernier si le point appartient au cercle ou non.
    """
    points = []
    cpt = 0
    for _ in range(nb_pts):
        x = random() * 2 - 1
        y = random() * 2 - 1
        appartient = x ** 2 + y ** 2 <= 1
        if appartient:
            cpt += 1
        points.append((x, y, appartient))
    return cpt, points


def monte_carlo_pi_fast(nb_pts):
    """
    Fait la même chose que monte_carlo_pi() sans ajouter les points dans une liste.
    Utile dans le cas où on exécute en tant que programme principal.
    Retourne directement une approximation de π.
    """
    cpt = 0
    for _ in range(nb_pts):
        x = random() * 2 - 1
        y = random() * 2 - 1
        cpt += x ** 2 + y ** 2 <= 1
    return 4 * cpt / nb_pts


def main():
    """
    Calcule une approximation de π grâce à une simulation de Monte-Carlo avec un
    nombre de points nb_points passé en argument dans la ligne de commande.
    """
    args = sys.argv
    if len(args) < 2:
        print("Utilisation : ./ApproximatePi.py <nb_pts>")
        return 0

    try:
        nb_pts = int(args[1])
    except ValueError:
        print("Le paramètre doit être un entier !")
        return 0

    if nb_pts < 1:
        print("La paramètre doit être un entier supérieur ou égal à 1 !")
        return 0

    print(monte_carlo_pi_fast(nb_pts))

    return 0


if __name__ == '__main__':
    main()
