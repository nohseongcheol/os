// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Appel par la porte int 0x80. Vérifier tous les pointeurs et toutes les longueurs utilisateur avant accès. */
public final class AppelSystème {
    static int[] tamponTemporaire = new int[1024];

    static int longueurTableau(int adresse) {
        if (!GestionExécution.rogner(adresse, 4)) return -14;
        int longueur = GestionExécution.nombre(adresse);
        if (longueur < 0 || longueur > (GestionExécution.finUtilisateur - adresse - 4) / 4) return -14;
        return longueur;
    }

    public static int entréeÉlémentValeurProcessus(int numéro, int opérandePremier, int opérandeDeuxième, int opérandeTroisième, int opérandeQuatrième, int opérandeCinquième) {
        if (numéro == 30) return GestionDescripteursFichier.ouvrirFichier(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 31) return GestionDescripteursFichier.lireFichier(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 32) return GestionDescripteursFichier.écrireFichier(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 33) return GestionDescripteursFichier.fermerFichier(opérandePremier);
        if (numéro == 34) return GestionDescripteursFichier.positionnerFichier(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 35) return GestionDescripteursFichier.descripteurDuplicata(opérandePremier, 0, false, 0);
        if (numéro == 36) return GestionDescripteursFichier.descripteurDuplicata(opérandePremier, opérandeDeuxième, true, 0);
        if (numéro == 37) return GestionDescripteursFichier.lireÉtatFichier(opérandePremier, opérandeDeuxième);
        if (numéro == 38) return GestionDescripteursFichier.supprimerNomEntréeÉlémentFichier(opérandePremier);
        if (numéro == 39) return GestionDescripteursFichier.définirLongueurFichier(opérandePremier, opérandeDeuxième);
        if (numéro == 40) return GestionDescripteursFichier.descripteurContrôle(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 41) return GestionDescripteursFichier.créerExtrémité(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 42) return GestionDescripteursFichier.associerAdresse(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 43) return GestionDescripteursFichier.envoyerDonnéesDatagramme(opérandePremier, opérandeDeuxième, opérandeTroisième, opérandeQuatrième, opérandeCinquième);
        if (numéro == 44) return GestionDescripteursFichier.recevoirDonnéesDatagramme(opérandePremier, opérandeDeuxième, opérandeTroisième, opérandeQuatrième, opérandeCinquième);
        if (numéro == 45) return GestionDescripteursFichier.lireAdressePriseRéseau(opérandePremier, opérandeDeuxième, opérandeTroisième);
        if (numéro == 46) return GestionDescripteursFichier.définirDélaiExpirationRecevoir(opérandePremier, opérandeDeuxième);
        if (numéro == 47) {
            int valeurDescripteur = GestionDescripteursFichier.trouverDescripteur(opérandePremier);
            if (valeurDescripteur < 0) return -9;
            if (GestionDescripteursFichier.valeurGenre[valeurDescripteur] != 2) return -22;
            return PersistanceFichiers.synchroniser();
        }
        if (numéro == 1) {
            int longueur = longueurTableau(opérandePremier);
            if (longueur < 0) return longueur;
            if (longueur > 4096) return -90;
            for (int valeurCaractère = 0; valeurCaractère < longueur; valeurCaractère++) TerminalTexte.Caractères(GestionExécution.nombre(opérandePremier + 4 + valeurCaractère * 4) & 65535);
            return longueur;
        }
        if (numéro == 2) return GestionExécution.nombreÉlémentsArgument;
        if (numéro == 3) return opérandePremier >= 0 && opérandePremier < GestionExécution.nombreÉlémentsArgument ? GestionExécution.adresseArgument[opérandePremier] : 0;
        if (numéro == 10) return PileRéseau.ouvrir(opérandePremier);
        if (numéro == 11) {
            int longueur = longueurTableau(opérandeQuatrième);
            if (longueur < 0) return longueur;
            if (opérandeCinquième < 0 || opérandeCinquième > longueur || opérandeCinquième > 1024) return -90;
            for (int position = 0; position < opérandeCinquième; position++) tamponTemporaire[position] = GestionExécution.nombre(opérandeQuatrième + 4 + position * 4) & 255;
            return PileRéseau.envoyer(opérandePremier, opérandeDeuxième, opérandeTroisième, tamponTemporaire, opérandeCinquième);
        }
        if (numéro == 12) {
            int longueur = longueurTableau(opérandeDeuxième);
            if (longueur < 0) return longueur;
            if (opérandeTroisième < 0 || opérandeTroisième > 2000) return -22;
            int résultat = PileRéseau.recevoir(opérandePremier, tamponTemporaire, longueur < 1024 ? longueur : 1024, opérandeTroisième);
            if (résultat >= 0) for (int position = 0; position < résultat; position++) GestionExécution.écrireNuméro(opérandeDeuxième + 4 + position * 4, tamponTemporaire[position]);
            return résultat;
        }
        if (numéro == 13) return PileRéseau.fermer(opérandePremier);
        if (numéro == 14) return PileRéseau.adressePropre;
        if (numéro == 15) return PileRéseau.adressePairRéseau(opérandePremier);
        if (numéro == 16) return PileRéseau.numéroPortPairRéseau(opérandePremier);
        if (numéro == 22) {
            if (opérandePremier < 0 || opérandePremier > 65535) return -22;
            TerminalTexte.Caractères(opérandePremier); return 1;
        }
        if (numéro == 20 || numéro == 21) {
            int tailleNom = longueurTableau(opérandePremier), tailleDonnées = longueurTableau(opérandeDeuxième);
            if (tailleNom < 0 || tailleDonnées < 0) return -14;
            if (tailleNom < 1 || tailleNom > 64) return -22;
            int longueur = 0;
            while (longueur < tailleNom && GestionExécution.nombre(opérandePremier + 4 + longueur * 4) != 0) {
                SystèmeFichiersMémoire.nom[longueur] = GestionExécution.nombre(opérandePremier + 4 + longueur * 4);
                longueur++;
            }
            if (!SystèmeFichiersMémoire.contrôlerNom(SystèmeFichiersMémoire.nom, longueur)) return -22;
            if (numéro == 20) {
                int Fichier = SystèmeFichiersMémoire.trouverEntréeÉlément(SystèmeFichiersMémoire.nom, longueur);
                if (Fichier < 0) return Fichier;
                int taille = SystèmeFichiersMémoire.listeTaille[Fichier];
                if (taille > tailleDonnées) return -90;
                int adresse = Périphérique.mémoireFichier() + Fichier * SystèmeFichiersMémoire.tailleMaximal;
                for (int nombre = 0; nombre < taille; nombre++) GestionExécution.écrireNuméro(opérandeDeuxième + 4 + nombre * 4, Périphérique.lireMémoire(adresse + nombre));
                return taille;
            }
            if (opérandeTroisième < 0 || opérandeTroisième > tailleDonnées) return -22;
            if (opérandeTroisième > SystèmeFichiersMémoire.tailleMaximal) return -90;
            for (int nombre = 0; nombre < opérandeTroisième; nombre++) SystèmeFichiersMémoire.valeurÉditer[nombre] = GestionExécution.nombre(opérandeDeuxième + 4 + nombre * 4) & 255;
            return SystèmeFichiersMémoire.valeurStocker(SystèmeFichiersMémoire.nom, longueur, SystèmeFichiersMémoire.valeurÉditer, opérandeTroisième);
        }
        return -38;
    }
}
