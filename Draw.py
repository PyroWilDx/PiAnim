#!/usr/bin/env python3

"""
Génère une image animée représentant une simulation de Monte-Carlo pour l'approximation de π.
"""

import subprocess
import sys
import collections

import ApproximatePi

"""
Contient les propriétés pour le dessin des chiffres de π.
Ces propriétés dépendent de la taille de l'image et sont calculées dans la fonction main().
    - w_ch : Longueur d'un segment horizontal dans l'affichage 7 segment d'un chiffre.
    - h_ch : Hauteur d'un segment vertical dans l'affichage 7 segment chiffre.
    - w_espace : Longueur de l'espacement entre les chiffres.
    - w_ch_tot : Longueur totale que prend un chiffre (w_ch + w_espace).
    - epaisseur : Épaisseur d'un segment d'un chiffre.
    - x : Abscisse de la gauche du premier chiffre de π.
    - y : Ordonnée du haut d'un chiffre (ils ont tous le même).
"""
PropsDessinPI = collections.namedtuple("PropsDessinPI", "w_ch h_ch w_espace w_ch_tot epaisseur x y")


def points_to_proportions(pts_monte_carlo, size, points):
    """
    Converti les points pts_monte_carlo calculé par le module ApproximatePi.py en
    les proportions voulues pour l'image. Si deux points se retrouvent sur le même
    pixel, on prend le dernier qui a été généré. Les points convertis sont ajoutés
    dans le dictionnaire points qui servira à les afficher dans une image.
    """
    for point in pts_monte_carlo:
        x = int((point[0] + 1) * (size / 2))
        y = size - 1 - int((point[1] + 1) * (size / 2))
        points[(x, y)] = point[2]


def generate_chiffre(chiffre):
    """
    Prend en paramètre un caractère entre '0' et '9' chiffre.
    Cette fonction retourne sous la forme d'une liste, l'affichage 7 segments
    du chiffre passé en paramètre.
    Les 3 premiers éléments de la liste correspondent respectivement aux
    3 segments horizontaux de l'affichage, de haut en bas.
    Les 4 éléments suivant de la liste correspondent respectivement aux
    4 segments verticaux de l'affichage, en prenant d'abord les 2 segments de
    gauche (de haut en bas), puis les 2 segments de droite (de haut en bas).
    """
    if chiffre == "0":
        return [True, False, True, True, True, True, True]
    if chiffre == "1":
        return [False, False, False, False, False, True, True]
    if chiffre == "2":
        return [True, True, True, False, True, True, False]
    if chiffre == "3":
        return [True, True, True, False, False, True, True]
    if chiffre == "4":
        return [False, True, False, True, False, True, True]
    if chiffre == "5":
        return [True, True, True, True, False, False, True]
    if chiffre == "6":
        return [True, True, True, True, True, False, True]
    if chiffre == "7":
        return [True, False, False, False, False, True, True]
    if chiffre == "8":
        return [True, True, True, True, True, True, True]
    if chiffre == "9":
        return [True, True, True, True, False, True, True]
    return []


def trace_trait_horizontal(x1_p, x2_p, y, epaisseur, points):
    """
    Ajoute les données nécéssaires dans le dictionnaire points afin de tracer un
    segment horizontal de (x1_p, y) à (x2_p, y) avec une certaine épaisseur.
    """
    for i in range(x1_p, x2_p + epaisseur):
        for j in range(epaisseur):
            points[(i, y + j)] = -1


def trace_trait_vertical(x, y1_p, y2_p, epaisseur, points):
    """
    Ajoute les données nécéssaires dans le dictionnaire points afin de tracer un
    segment vertical de (x, y1_p) à (x, y2_p) avec une certaine épaisseur.
    """
    for j in range(y1_p, y2_p + epaisseur):
        for i in range(epaisseur):
            points[(x + i, j)] = -1


def trace_chiffre(chiffre, x, props, points):
    """
    Ajoute les données nécéssaires dans le dictionnaire points afin de tracer un
    chiffre dont le point en haut à gauche est (x, props.y).
    Les segment horizontaux dans l'affichage 7 segments d'un chiffre sont de
    longueur props.w_ch, et ceux verticaux de hauteur props.h_ch, chacun de ces segments ont
    une certaine épaisseur props.epaisseur.
    """
    if chiffre[0]:
        trace_trait_horizontal(x, x + props.w_ch, props.y,
                               props.epaisseur, points)
    if chiffre[1]:
        trace_trait_horizontal(x, x + props.w_ch, props.y + props.h_ch,
                               props.epaisseur, points)
    if chiffre[2]:
        trace_trait_horizontal(x, x + props.w_ch, props.y + 2 * props.h_ch,
                               props.epaisseur, points)
    if chiffre[3]:
        trace_trait_vertical(x, props.y, props.y + props.h_ch,
                             props.epaisseur, points)
    if chiffre[4]:
        trace_trait_vertical(x, props.y + props.h_ch, props.y + 2 * props.h_ch,
                             props.epaisseur, points)
    if chiffre[5]:
        trace_trait_vertical(x + props.w_ch, props.y, props.y + props.h_ch,
                             props.epaisseur, points)
    if chiffre[6]:
        trace_trait_vertical(x + props.w_ch, props.y + props.h_ch, props.y + 2 * props.h_ch,
                             props.epaisseur, points)


def trace_point(x, y, taille_pts, points):
    """
    Ajoute les données nécéssaires dans le dictionnaire points afin de tracer un
    point dont les coordonnées en haut à gauche sont (x, y), ce point est de longueur taille_pts.
    """
    for i in range(x, x + taille_pts):
        for j in range(y, y + taille_pts):
            points[(i, j)] = -1


def trace_pi(str_pi, size, props, points):
    """
    Ajoute les données nécéssaires dans le dictionnaire points afin de tracer le
    paramètre str_pi qu'on a simulé avec ApproximatePi.py, puis converti comme voulu avec la
    fonction convert_pi(). Les propriétés des chiffres (comme leur longueur, epaisseur etc...) sont
    dans props et dépendant de la taille de l'image.
    """
    x = props.x
    for carac in str_pi:
        if carac == '.':
            taille_pts = 1 + size // 100
            y_pts = props.y + 2 * props.h_ch + props.epaisseur - taille_pts
            trace_point(x, y_pts, taille_pts, points)
            x += taille_pts + props.w_espace
        else:
            trace_chiffre(generate_chiffre(carac), x, props, points)
            x += props.w_ch_tot


def generate_ppm_file(img_name, size, points):
    """
    Génère une image .ppm de nom img_name et de taille size*size :
    - L'image à un fond blanc.
    - Elle contiendra les points dans le cercle
      de la simulation ApproximatePi.py en bleu et ceux qui
      ne sont pas dans le cercle en rose.
    - L'approximation de π sera affichée au milieu de l'image par
    dessus les points précédents.

    Le paramètre point contient les coordonnées de ces points à
    afficher et de l'écriture de l'approximation de π.
    """
    with open(img_name, 'w', encoding='utf-8') as f_img:
        f_img.write("P3\n")
        f_img.write(f"{size} {size}\n")
        f_img.write("255\n")
        for j in range(size):
            for i in range(size):
                if (i, j) in points:
                    if points[(i, j)] == -1:
                        f_img.write("0 0 0 ")
                    elif points[(i, j)]:
                        f_img.write("42 193 253 ")
                    else:
                        f_img.write("249 69 176 ")
                else:
                    f_img.write("255 255 255 ")
            f_img.write("\n")


def generate_gif(size, nb_pts, nb_v, props):
    """
    Génère le GIF représentant l'état courant de la simulation à chaque fois
    qu'un dixième du nombre total de points a été tiré dans la simulation de
    Monte-Carlo pour approximer π. Ce GIF contient 10 images dont les contenus
    sont spécifiés dans la fonction generate_ppm_file().
    """
    imgs = []  # Liste pour contenir le nom des 10 images.
    k = nb_pts // 10  # On simule un dixième des points à la fois.
    reste = nb_pts % 10  # Reste à ajouter à la dernière simulation s'il y en a.
    all_points = {}  # Dictionnaire pour contenir tous les points générés par les simulations.
    cpt = 0  # Compteur total de points dans le cercle pour toutes les simulations.

    for i in range(10):

        if i == 0:
            k += reste

        current_cpt, current_points = ApproximatePi.monte_carlo_pi(k)
        cpt += current_cpt
        points_to_proportions(current_points, size, all_points)

        str_pi = f"{round(4 * cpt / (k * (i + 1)), nb_v):.{nb_v}f}"

        img_name = f"img{i}_{str_pi[0]}-{str_pi[2:]}.ppm"
        imgs.append(img_name)

        points = all_points.copy()  # Copie car sinon les points pour tracer π vont rester.
        trace_pi(str_pi, size, props, points)
        generate_ppm_file(img_name, size, points)

    # Génération du GIF.
    if subprocess.call(["convert", "-delay", "80"] + imgs + ["anime.gif"]) != 0:
        raise ValueError("Erreur dans la génération du GIF")


def main():
    """
    Fonction Main qui regarde si les paramètres passé en argument dans la ligne
    de commande sont correctes ou pas.
    La fonction calcule ensuite les propriétés que doivent avoir les chiffres
    dans l'affichage de l'approximation de π et enfin appelle la fonction
    generate_gif() qui se charge de générer le GIF illustrant l'approximation
    de π par la simulation de Monte-Carlo.
    """
    args = sys.argv
    if len(args) < 4:
        raise TypeError("Utilisation : ./Draw.py <size> <n> <nb_virgule>")

    try:
        size = int(args[1])
        nb_pts = int(args[2])
        nb_v = int(args[3])
    except ValueError as error:
        raise ValueError("Les 3 paramètres doivent être des entiers !") from error

    if size < 100:
        raise ValueError(
            "La size de l'image doit être un entier supérieur ou égal à 100 !"
        )
    if nb_pts < 101:
        raise ValueError(
            "Le nombre de points utilisés dans la simulation doit être supérieur (strict) à 100 !"
        )
    if nb_v < 1 or nb_v > 5:
        raise ValueError(
            "Le nombre de chiffres après la virgule pour l'affichage de π doit être entre 1 et 5 (compris) !"
        )

    w_ch = size // 40
    h_ch = size // 24
    w_espace = 1 + size // 100
    w_ch_tot = w_ch + w_espace
    epaisseur = 1 + size // 400
    x = size // 2 - w_ch_tot * (1 + nb_v // 2)
    y = size // 2 - h_ch // 2
    props = PropsDessinPI(w_ch, h_ch, w_espace, w_ch_tot, epaisseur, x, y)

    generate_gif(size, nb_pts, nb_v, props)

    return 0


if __name__ == '__main__':
    main()
