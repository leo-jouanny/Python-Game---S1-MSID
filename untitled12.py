#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 18:16:21 2024

@author: leo
"""

import random

class Combattant:
    def __init__(self, pseudo, pv, attaque):
        self.pseudo = pseudo
        self.pv = pv
        self.attaque = attaque
        self.arme = None  # Aucune arme au début

    def subi(self, attaquant):
        degats_totaux = attaquant.attaque
        if attaquant.arme and attaquant.arme.duree > 0:
            degats_totaux += attaquant.arme.appliquer_effet(attaquant)
        self.pv -= degats_totaux
        print(f"{attaquant.pseudo} attaque {self.pseudo} avec {degats_totaux} de dégâts. {self.pseudo} perd {degats_totaux} pv, il lui en reste {self.pv}.")

    def acheter_arme(self, arme):
        self.arme = arme
        print(f"{self.pseudo} a acheté {arme.nom} qui fait {arme.degats_supplementaires} dégâts supplémentaires pendant {arme.duree} tours.")

    def potion_magique(self):
        chance = random.randint(1, 100)
        if chance <= 70:
            vie_gagnee = random.randint(5, 10)
            self.pv += vie_gagnee
            print(f"La potion magique de druide toxicomane régénère {vie_gagnee} pv à {self.pseudo}.")
        else:
            vie_perdue = random.randint(1, 5)
            self.pv -= vie_perdue
            print(f"La potion magique de druide toxicomane fait perdre {vie_perdue} pv à {self.pseudo}. Attention aux effets secondaires !")

class Arme:
    def __init__(self, nom, degats_supplementaires, duree, effet_global=False):
        self.nom = nom
        self.degats_supplementaires = degats_supplementaires
        self.duree = duree
        self.effet_global = effet_global

    def appliquer_effet(self, attaquant):
        if self.duree > 0:
            self.duree -= 1
            return self.degats_supplementaires
        else:
            return 0

class PNJ:
    def __init__(self, nom, pv):
        self.nom = nom
        self.pv = pv

    def subi(self, degats):
        self.pv -= degats
        print(f"{self.nom} a subi {degats} de dégâts, il lui reste {self.pv} PV.")
        if self.pv <= 0:
            print(f"{self.nom} est vaincu!")
            return True  # Le PNJ est tué
        return False


# Initialisation des combattants
guerrier = Combattant("Conan", 100, 10)
magicien = Combattant("Gandalf", 50, 20)
geant = Combattant("Hagrid", 200, 5)
liste_combattant = [guerrier, magicien, geant]
dictionnaire_combattant = {1: guerrier, 2: magicien, 3: geant}
compteur = 0
bombe_nucleaire_utilisee = False  # Contrôle l'utilisation unique de la bombe nucléaire
pnjs = [PNJ("Gobelin", 30), PNJ("Troll", 50), PNJ("Dragon", 100)]

def combat_pnj(combattant_actif):
    pnj = random.choice(pnjs)  # Sélectionne un PNJ aléatoire pour le combat
    print(f"{combattant_actif.pseudo} a choisi de combattre {pnj.nom} qui a {pnj.pv} PV.")

    if pnj.subi(combattant_actif.attaque):
        # Le PNJ est tué, appliquez les récompenses ou pénalités ici
        # Exemple de loot:
        loot = random.choice(["babouches", "skinny jeans", "crop top", "oreilles de Mickey"])
        print(f"{combattant_actif.pseudo} gagne {loot}!")
        # Vous pouvez étendre cette logique pour appliquer l'effet du loot au combattant
    else:
        # Le PNJ survit, le joueur subit potentiellement des dégâts
        if random.randint(1, 3) == 1:  # 1 chance sur 3 de subir des dégâts
            degats_subis = random.randint(5, 50)
            combattant_actif.pv -= degats_subis
            print(f"{combattant_actif.pseudo} subit {degats_subis} de dégâts en contre-attaque!")

def demander():
    while True:
        try:
            choix = int(input("Combatant : "))
            if choix in dictionnaire_combattant:
                return choix
            else:
                print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")

def cibler(liste, combattant_actif):
    for e in dictionnaire_combattant:
        if dictionnaire_combattant[e] in liste and dictionnaire_combattant[e] != combattant_actif:
            print(f"Pour attaquer {dictionnaire_combattant[e].pseudo}, tapez {e}")
    return demander()

def appeler_dealer(compteur, combattant_actif):
    global bombe_nucleaire_utilisee
    # Modifier ici pour que cela corresponde à un appel tous les trois tours, dès le premier tour
    if (compteur - 1) % 3 == 0:
        print(f"{combattant_actif.pseudo}, voulez-vous appeler le dealer d'armes à feu ? (oui/non)")
        choix = input().lower()
        if choix == 'oui':
            print("1. Laceaux (5 dégâts supplémentaires pendant 10 tours)")
            print("2. Fusil à pompe (20 dégâts supplémentaires pendant 4 tours)")
            print("3. Bombe nucléaire (50 dégâts instantanément à tous, utilisable une fois)")
            choix_arme = int(input("Choisissez votre arme : "))
            if choix_arme == 1:
                combattant_actif.acheter_arme(Arme("Laceaux", 5, 10))
            elif choix_arme == 2:
                combattant_actif.acheter_arme(Arme("Fusil à pompe", 20, 4))
            elif choix_arme == 3 and not bombe_nucleaire_utilisee:
                for combattant in liste_combattant:
                    combattant.pv -= 50
                print("Bombe nucléaire utilisée, tous les joueurs perdent 50 pv!")
                bombe_nucleaire_utilisee = True


while True:
    if len(liste_combattant) <= 1:
        break
    combattant_actif = liste_combattant[compteur % len(liste_combattant)]
    print(f"c'est au tour de : {combattant_actif.pseudo}")
    compteur += 1

    combat_choix = input(f"{combattant_actif.pseudo}, voulez-vous combattre un PNJ ? (o/n) ")
    if combat_choix.lower() == 'o':
        combat_pnj(combattant_actif)
    else:
        # Option pour utiliser la potion magique
        utiliser_potion = input(f"Voulez-vous utiliser la potion magique pour {combattant_actif.pseudo} ? (o/n) ")
        if utiliser_potion.lower() == 'o':
            combattant_actif.potion_magique()

        # Option pour appeler le dealer d'armes
        appeler_dealer(compteur, combattant_actif)

        # Passer le combattant actif comme argument pour éviter l'auto-attaque
        clef_cible = cibler(liste_combattant, combattant_actif)
        cible = dictionnaire_combattant[clef_cible]
        cible.subi(combattant_actif)
        if cible.pv <= 0:
            print(f"{cible.pseudo} est KO.")
            liste_combattant.remove(cible)

    # Cette vérification doit rester à l'extérieur de la boucle while principale
    if len(liste_combattant) == 1:
        print(f"Le vainqueur est {liste_combattant[0].pseudo}.")
        break  # Ajouté pour sortir explicitement de la boucle après avoir déterminé le vainqueur
