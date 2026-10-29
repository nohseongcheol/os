// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Sépare les descripteurs d’un processus utilisateur des descriptions de fichiers ouverts. Les numéros d’appel sont documentés dans l’ABI POSIX. */
public final class GestionDescripteursFichier {
    static final int limiteDescripteur = 32;
    static final int lireDrapeauÉcrire = 2, créerEntréeÉlément = 64, créerExclusivement = 128, effacerContenuContenu = 512;
    static final int ajouterFinContinuation = 1024, attendrePasFaire = 2048, fermerOpérationExécutionActivé = 524288;
    static int[] ouvrirPoignée = new int[limiteDescripteur], définirDescripteur = new int[limiteDescripteur];
    static int[] valeurGenre = new int[limiteDescripteur], valeurCible = new int[limiteDescripteur];
    static int[] positionFichier = new int[limiteDescripteur], ouvrirRéglages = new int[limiteDescripteur], nombreÉlémentsRéférence = new int[limiteDescripteur];
    static int[] poignéeRéseau = new int[limiteDescripteur], recevoirMillisecondesDélaiExpiration = new int[limiteDescripteur];
    static int[] nomChemin = new int[64], donnéesTransfert = new int[1024];

    static int trouverDescripteur(int descripteurFichier) {
        if (descripteurFichier < 0 || descripteurFichier >= limiteDescripteur) return -9;
        return ouvrirPoignée[descripteurFichier] - 1;
    }
    static int descripteurVide(int lancer) {
        for (int numéro = lancer; numéro < limiteDescripteur; numéro++) if (ouvrirPoignée[numéro] == 0) return numéro;
        return -24;
    }
    static int poignéeVide() {
        for (int numéro = 0; numéro < limiteDescripteur; numéro++) if (nombreÉlémentsRéférence[numéro] == 0) return numéro;
        return -24;
    }
    static int connecter(int entréeÉlémentDescripteur, int valeurDescripteur, int genreFichier, int valeurCibleFichier, int réglages) {
        ouvrirPoignée[entréeÉlémentDescripteur] = valeurDescripteur + 1; définirDescripteur[entréeÉlémentDescripteur] = (réglages & fermerOpérationExécutionActivé) != 0 ? 1 : 0;
        valeurGenre[valeurDescripteur] = genreFichier; valeurCible[valeurDescripteur] = valeurCibleFichier; nombreÉlémentsRéférence[valeurDescripteur] = 1;
        ouvrirRéglages[valeurDescripteur] = réglages & (3 | ajouterFinContinuation | attendrePasFaire); positionFichier[valeurDescripteur] = 0;
        poignéeRéseau[valeurDescripteur] = 0; recevoirMillisecondesDélaiExpiration[valeurDescripteur] = 0;
        return entréeÉlémentDescripteur;
    }
    static void démarrerProcessus() {
        processusNettoyer();
        for (int numéro = 0; numéro < 3; numéro++) connecter(numéro, numéro, 1, numéro, numéro == 0 ? 0 : 1);
    }
    static void processusNettoyer() {
        for (int numéro = 0; numéro < limiteDescripteur; numéro++) if (ouvrirPoignée[numéro] != 0) fermerFichier(numéro);
    }
    static int fermerFichier(int entréeÉlémentDescripteur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        ouvrirPoignée[entréeÉlémentDescripteur] = 0; définirDescripteur[entréeÉlémentDescripteur] = 0;
        nombreÉlémentsRéférence[valeurDescripteur]--;
        if (nombreÉlémentsRéférence[valeurDescripteur] == 0) {
            if (valeurGenre[valeurDescripteur] == 2) SystèmeFichiersMémoire.ouvrirNombreÉléments[valeurCible[valeurDescripteur]]--;
            if (valeurGenre[valeurDescripteur] == 3 && poignéeRéseau[valeurDescripteur] != 0) PileRéseau.fermer(poignéeRéseau[valeurDescripteur]);
            valeurGenre[valeurDescripteur] = 0;
        }
        return 0;
    }
    // Les chemins C sont des chaînes d’octets terminées par NUL. Un seul nom directement sous la racine est pris en charge.
    static int lireChemin(int adresse) {
        if (!GestionExécution.rogner(adresse, 1)) return -14;
        int position = Périphérique.lireMémoire(adresse) == '/' ? 1 : 0;
        for (int longueur = 0; longueur < 64; longueur++) {
            if (!GestionExécution.rogner(adresse + position + longueur, 1)) return -14;
            int valeur = Périphérique.lireMémoire(adresse + position + longueur);
            nomChemin[longueur] = valeur;
            if (valeur == 0) return longueur == 0 ? -2 : (SystèmeFichiersMémoire.contrôlerNom(nomChemin, longueur) ? longueur : -22);
            if (valeur == '/') return -20;
        }
        return -36;
    }
    static int ouvrirFichier(int adresseNom, int réglages, int accorderPermission) {
        int longueur = lireChemin(adresseNom);
        if (longueur < 0) return longueur;
        if ((réglages & ~(3 | créerEntréeÉlément | créerExclusivement | effacerContenuContenu | ajouterFinContinuation | attendrePasFaire | fermerOpérationExécutionActivé)) != 0) return -95;
        if ((réglages & 3) == 3 || ((réglages & effacerContenuContenu) != 0 && (réglages & 3) == 0)) return -22;
        int Fichier = SystèmeFichiersMémoire.trouverEntréeÉlément(nomChemin, longueur);
        if (Fichier >= 0 && (réglages & (créerEntréeÉlément | créerExclusivement)) == (créerEntréeÉlément | créerExclusivement)) return -17;
        if (Fichier == -2 && (réglages & créerEntréeÉlément) == 0) return -2;
        int entréeÉlémentDescripteur = descripteurVide(0), valeurDescripteur = poignéeVide();
        if (entréeÉlémentDescripteur < 0 || valeurDescripteur < 0) return -24;
        if (Fichier == -2) {
            int résultat = SystèmeFichiersMémoire.valeurStocker(nomChemin, longueur, nomChemin, 0);
            if (résultat < 0) return résultat;
            Fichier = SystèmeFichiersMémoire.trouverEntréeÉlément(nomChemin, longueur);
            SystèmeFichiersMémoire.autorisationsPermission[Fichier] = accorderPermission & 511;
        }
        if (Fichier < 0) return Fichier;
        if ((réglages & effacerContenuContenu) != 0) SystèmeFichiersMémoire.listeTaille[Fichier] = 0;
        SystèmeFichiersMémoire.ouvrirNombreÉléments[Fichier]++;
        return connecter(entréeÉlémentDescripteur, valeurDescripteur, 2, Fichier, réglages);
    }
    static int lireFichier(int entréeÉlémentDescripteur, int adresseDonnées, int longueur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0 || (ouvrirRéglages[valeurDescripteur] & 3) == 1) return -9;
        if (longueur < 0) return -22;
        if (longueur == 0) return 0;
        if (!GestionExécution.rogner(adresseDonnées, longueur)) return -14;
        if (valeurGenre[valeurDescripteur] == 3) return recevoirDonnéesDatagramme(entréeÉlémentDescripteur, adresseDonnées, longueur, 0, 0);
        if (valeurGenre[valeurDescripteur] == 1) {
            int nombreÉlémentsReçu = 0;
            while (nombreÉlémentsReçu < longueur) {
                int valeur = TerminalTexte.lireSériel();
                if (valeur < 0) valeur = Clavier.lire();
                if (valeur < 0) {
                    if (nombreÉlémentsReçu > 0) return nombreÉlémentsReçu;
                    if ((ouvrirRéglages[valeurDescripteur] & attendrePasFaire) != 0) return -11;
                    if (Périphérique.millisecondesRestantUtilisateur() <= 10) return -11;
                    PileRéseau.vérifier(); Périphérique.céderBrièvement();
                } else {
                    Périphérique.écrireMémoire(adresseDonnées + nombreÉlémentsReçu, valeur); nombreÉlémentsReçu++;
                }
            }
            return nombreÉlémentsReçu;
        }
        int Fichier = valeurCible[valeurDescripteur], position = positionFichier[valeurDescripteur];
        if (position >= SystèmeFichiersMémoire.listeTaille[Fichier]) return 0;
        if (longueur > SystèmeFichiersMémoire.listeTaille[Fichier] - position) longueur = SystèmeFichiersMémoire.listeTaille[Fichier] - position;
        int adresseOriginal = Périphérique.mémoireFichier() + Fichier * SystèmeFichiersMémoire.tailleMaximal + position;
        for (int numéro = 0; numéro < longueur; numéro++) Périphérique.écrireMémoire(adresseDonnées + numéro, Périphérique.lireMémoire(adresseOriginal + numéro));
        positionFichier[valeurDescripteur] += longueur;
        return longueur;
    }
    static int écrireFichier(int entréeÉlémentDescripteur, int adresseDonnées, int longueur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0 || (ouvrirRéglages[valeurDescripteur] & 3) == 0) return -9;
        if (longueur < 0) return -22;
        if (longueur == 0) return 0;
        if (!GestionExécution.rogner(adresseDonnées, longueur)) return -14;
        if (valeurGenre[valeurDescripteur] == 3) return -89; // Une extrémité de datagramme non connectée nécessite une adresse de destination.
        if (valeurGenre[valeurDescripteur] == 1) {
            if (longueur > 16384) longueur = 16384;
            for (int numéro = 0; numéro < longueur; numéro++) {
                int valeur = Périphérique.lireMémoire(adresseDonnées + numéro);
                TerminalTexte.octetSériel(valeur); TerminalTexte.caractèreÉcran(valeur);
            }
            return longueur;
        }
        int Fichier = valeurCible[valeurDescripteur], taille = SystèmeFichiersMémoire.listeTaille[Fichier];
        int position = (ouvrirRéglages[valeurDescripteur] & ajouterFinContinuation) != 0 ? taille : positionFichier[valeurDescripteur];
        if (position >= SystèmeFichiersMémoire.tailleMaximal) return -27;
        if (longueur > SystèmeFichiersMémoire.tailleMaximal - position) longueur = SystèmeFichiersMémoire.tailleMaximal - position;
        int adresseDestination = Périphérique.mémoireFichier() + Fichier * SystèmeFichiersMémoire.tailleMaximal;
        for (int numéro = taille; numéro < position; numéro++) Périphérique.écrireMémoire(adresseDestination + numéro, 0);
        for (int numéro = 0; numéro < longueur; numéro++) Périphérique.écrireMémoire(adresseDestination + position + numéro, Périphérique.lireMémoire(adresseDonnées + numéro));
        positionFichier[valeurDescripteur] = position + longueur;
        if (position + longueur > taille) SystèmeFichiersMémoire.listeTaille[Fichier] = position + longueur;
        return longueur;
    }
    static int positionnerFichier(int entréeÉlémentDescripteur, int valeurDécalage, int racineProjet) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        if (valeurGenre[valeurDescripteur] != 2) return -29;
        if (racineProjet < 0 || racineProjet > 2) return -22;
        int valeurArrièrePlan = racineProjet == 0 ? 0 : (racineProjet == 1 ? positionFichier[valeurDescripteur] : SystèmeFichiersMémoire.listeTaille[valeurCible[valeurDescripteur]]);
        if (valeurDécalage > 0 && valeurArrièrePlan > 2147483647 - valeurDécalage) return -75;
        if (valeurDécalage < 0 && valeurDécalage < -valeurArrièrePlan) return -22;
        positionFichier[valeurDescripteur] = valeurArrièrePlan + valeurDécalage;
        return positionFichier[valeurDescripteur];
    }
    static int descripteurDuplicata(int entréeÉlémentDescripteur, int descripteurNouveau, boolean valeurAffecter, int réglages) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        if (descripteurNouveau < 0 || descripteurNouveau >= limiteDescripteur) return valeurAffecter ? -9 : -22;
        if (valeurAffecter && entréeÉlémentDescripteur == descripteurNouveau) return descripteurNouveau;
        if (valeurAffecter) { if (ouvrirPoignée[descripteurNouveau] != 0) fermerFichier(descripteurNouveau); }
        else { descripteurNouveau = descripteurVide(descripteurNouveau); if (descripteurNouveau < 0) return descripteurNouveau; }
        ouvrirPoignée[descripteurNouveau] = valeurDescripteur + 1; définirDescripteur[descripteurNouveau] = réglages; nombreÉlémentsRéférence[valeurDescripteur]++;
        return descripteurNouveau;
    }
    static int supprimerNomEntréeÉlémentFichier(int adresseNom) {
        int longueur = lireChemin(adresseNom);
        if (longueur < 0) return longueur;
        int Fichier = SystèmeFichiersMémoire.trouverEntréeÉlément(nomChemin, longueur);
        if (Fichier < 0) return Fichier;
        SystèmeFichiersMémoire.listeNoms[Fichier * 64] = 0;
        return 0;
    }
    static int définirLongueurFichier(int entréeÉlémentDescripteur, int longueur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        if (valeurGenre[valeurDescripteur] != 2 || (ouvrirRéglages[valeurDescripteur] & 3) == 0 || longueur < 0) return -22;
        if (longueur > SystèmeFichiersMémoire.tailleMaximal) return -27;
        int Fichier = valeurCible[valeurDescripteur], adresse = Périphérique.mémoireFichier() + Fichier * SystèmeFichiersMémoire.tailleMaximal;
        for (int numéro = SystèmeFichiersMémoire.listeTaille[Fichier]; numéro < longueur; numéro++) Périphérique.écrireMémoire(adresse + numéro, 0);
        SystèmeFichiersMémoire.listeTaille[Fichier] = longueur;
        return 0;
    }
    static int lireÉtatFichier(int entréeÉlémentDescripteur, int adresse) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        if (!GestionExécution.rogner(adresse, 48)) return -14;
        for (int numéro = 0; numéro < 12; numéro++) GestionExécution.écrireNuméro(adresse + numéro * 4, 0);
        int Fichier = valeurCible[valeurDescripteur], taille = valeurGenre[valeurDescripteur] == 2 ? SystèmeFichiersMémoire.listeTaille[Fichier] : 0;
        int accorderPermission = valeurGenre[valeurDescripteur] == 2 ? SystèmeFichiersMémoire.autorisationsPermission[Fichier] : 438;
        GestionExécution.écrireNuméro(adresse, 1);
        GestionExécution.écrireNuméro(adresse + 4, valeurGenre[valeurDescripteur] == 2 ? Fichier + 1 : 100 + valeurDescripteur);
        GestionExécution.écrireNuméro(adresse + 8, (valeurGenre[valeurDescripteur] == 2 ? 32768 : (valeurGenre[valeurDescripteur] == 1 ? 8192 : 49152)) | accorderPermission);
        GestionExécution.écrireNuméro(adresse + 12, valeurGenre[valeurDescripteur] == 2 && SystèmeFichiersMémoire.listeNoms[Fichier * 64] == 0 ? 0 : 1);
        GestionExécution.écrireNuméro(adresse + 28, taille); GestionExécution.écrireNuméro(adresse + 32, 512);
        GestionExécution.écrireNuméro(adresse + 36, (taille + 511) / 512);
        return 0;
    }
    static int descripteurContrôle(int entréeÉlémentDescripteur, int commande, int valeur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        if (commande == 0 || commande == 1030) return descripteurDuplicata(entréeÉlémentDescripteur, valeur, false, commande == 1030 ? 1 : 0);
        if (commande == 1) return définirDescripteur[entréeÉlémentDescripteur];
        if (commande == 2) { if ((valeur & ~1) != 0) return -22; définirDescripteur[entréeÉlémentDescripteur] = valeur; return 0; }
        if (commande == 3) return ouvrirRéglages[valeurDescripteur];
        if (commande == 4) {
            if ((valeur & ~(3 | ajouterFinContinuation | attendrePasFaire)) != 0) return -95;
            ouvrirRéglages[valeurDescripteur] = (ouvrirRéglages[valeurDescripteur] & 3) | (valeur & (ajouterFinContinuation | attendrePasFaire)); return 0;
        }
        return -95;
    }
    static int créerExtrémité(int schémaAdresse, int genreRéseau, int numéroContrat) {
        if (schémaAdresse != 2) return -97;
        if (genreRéseau != 2) return -93;
        if (numéroContrat != 0 && numéroContrat != 17) return -93;
        int entréeÉlémentDescripteur = descripteurVide(0), valeurDescripteur = poignéeVide();
        if (entréeÉlémentDescripteur < 0 || valeurDescripteur < 0) return -24;
        return connecter(entréeÉlémentDescripteur, valeurDescripteur, 3, 0, lireDrapeauÉcrire);
    }
    static int descripteurExtrémité(int entréeÉlémentDescripteur) {
        int valeurDescripteur = trouverDescripteur(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return -9;
        return valeurGenre[valeurDescripteur] == 3 ? valeurDescripteur : -88;
    }
    static int adresse32(int adresse) {
        return Périphérique.lireMémoire(adresse) << 24 | Périphérique.lireMémoire(adresse + 1) << 16
            | Périphérique.lireMémoire(adresse + 2) << 8 | Périphérique.lireMémoire(adresse + 3);
    }
    static int contrôlerAdresse(int adresse, int longueur) {
        if (longueur < 16) return -22;
        if (!GestionExécution.rogner(adresse, 16)) return -14;
        return GestionExécution.valeurCourt(adresse) == 2 ? 0 : -97;
    }
    static int associerAdresse(int entréeÉlémentDescripteur, int adresse, int longueur) {
        int valeurDescripteur = descripteurExtrémité(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return valeurDescripteur;
        int résultat = contrôlerAdresse(adresse, longueur);
        if (résultat < 0) return résultat;
        if (poignéeRéseau[valeurDescripteur] != 0) return -22;
        int adresseRéseau = adresse32(adresse + 4);
        if (adresseRéseau != 0 && adresseRéseau != PileRéseau.adressePropre) return -99;
        int numéroPort = Périphérique.lireMémoire(adresse + 2) << 8 | Périphérique.lireMémoire(adresse + 3);
        résultat = PileRéseau.ouvrir(numéroPort);
        if (résultat < 0) return résultat;
        poignéeRéseau[valeurDescripteur] = résultat; valeurCible[valeurDescripteur] = adresseRéseau;
        return 0;
    }
    static int associerAutoMode(int valeurDescripteur) {
        if (poignéeRéseau[valeurDescripteur] != 0) return 0;
        int résultat = PileRéseau.ouvrir(0);
        if (résultat < 0) return résultat;
        poignéeRéseau[valeurDescripteur] = résultat;
        return 0;
    }
    // Les deux derniers arguments de sendto/recvfrom sont transmis dans une structure de requête de 8 octets.
    static int envoyerDonnéesDatagramme(int entréeÉlémentDescripteur, int adresseDonnées, int longueur, int réglages, int adresseDemandé) {
        int valeurDescripteur = descripteurExtrémité(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return valeurDescripteur;
        if (réglages != 0) return -95;
        if (longueur < 0 || longueur > 1024) return -90;
        if (longueur != 0 && !GestionExécution.rogner(adresseDonnées, longueur)) return -14;
        if (!GestionExécution.rogner(adresseDemandé, 8)) return -14;
        int adresse = GestionExécution.nombre(adresseDemandé);
        int résultat = contrôlerAdresse(adresse, GestionExécution.nombre(adresseDemandé + 4));
        if (résultat < 0) return résultat;
        int numéroPort = Périphérique.lireMémoire(adresse + 2) << 8 | Périphérique.lireMémoire(adresse + 3);
        if (numéroPort == 0) return -22;
        résultat = associerAutoMode(valeurDescripteur);
        if (résultat < 0) return résultat;
        for (int numéro = 0; numéro < longueur; numéro++) donnéesTransfert[numéro] = Périphérique.lireMémoire(adresseDonnées + numéro);
        return PileRéseau.envoyer(poignéeRéseau[valeurDescripteur], adresse32(adresse + 4), numéroPort, donnéesTransfert, longueur);
    }
    static void écrireAdresse(int adresse, int longueur, int adresseRéseau, int numéroPort) {
        for (int numéro = 0; numéro < longueur && numéro < 16; numéro++) {
            int valeur = 0;
            if (numéro == 0) valeur = 2;
            if (numéro == 2) valeur = numéroPort >>> 8;
            if (numéro == 3) valeur = numéroPort;
            if (numéro >= 4 && numéro < 8) valeur = adresseRéseau >>> (56 - numéro * 8);
            Périphérique.écrireMémoire(adresse + numéro, valeur & 255);
        }
    }
    static int recevoirDonnéesDatagramme(int entréeÉlémentDescripteur, int adresseDonnées, int longueur, int réglages, int adresseDemandé) {
        int valeurDescripteur = descripteurExtrémité(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return valeurDescripteur;
        if ((réglages & ~64) != 0) return -95;
        if (longueur < 0) return -22;
        if (longueur != 0 && !GestionExécution.rogner(adresseDonnées, longueur)) return -14;
        int adresse = 0, adresseLongueurAdresse = 0, longueurAdresse = 0;
        if (adresseDemandé != 0) {
            if (!GestionExécution.rogner(adresseDemandé, 8)) return -14;
            adresse = GestionExécution.nombre(adresseDemandé); adresseLongueurAdresse = GestionExécution.nombre(adresseDemandé + 4);
            if (adresse != 0) {
                if (!GestionExécution.rogner(adresseLongueurAdresse, 4)) return -14;
                longueurAdresse = GestionExécution.nombre(adresseLongueurAdresse);
                if (longueurAdresse < 0) return -22;
                if (!GestionExécution.rogner(adresse, longueurAdresse < 16 ? longueurAdresse : 16)) return -14;
            }
        }
        int résultat = associerAutoMode(valeurDescripteur);
        if (résultat < 0) return résultat;
        int lancer = Périphérique.millisecondes();
        while (true) {
            résultat = PileRéseau.recevoir(poignéeRéseau[valeurDescripteur], donnéesTransfert, 1024, 0);
            if (résultat != -11) break;
            if ((réglages & 64) != 0 || (ouvrirRéglages[valeurDescripteur] & attendrePasFaire) != 0) return -11;
            if (recevoirMillisecondesDélaiExpiration[valeurDescripteur] > 0 && Périphérique.millisecondes() - lancer >= recevoirMillisecondesDélaiExpiration[valeurDescripteur]) return -11;
            if (Périphérique.millisecondesRestantUtilisateur() <= 10) return -11;
            Périphérique.céderBrièvement();
        }
        if (résultat < 0) return résultat;
        if (résultat > longueur) résultat = longueur;
        for (int numéro = 0; numéro < résultat; numéro++) Périphérique.écrireMémoire(adresseDonnées + numéro, donnéesTransfert[numéro]);
        if (adresse != 0) {
            écrireAdresse(adresse, longueurAdresse, PileRéseau.adressePairRéseau(poignéeRéseau[valeurDescripteur]), PileRéseau.numéroPortPairRéseau(poignéeRéseau[valeurDescripteur]));
            GestionExécution.écrireNuméro(adresseLongueurAdresse, 16);
        }
        return résultat;
    }
    static int lireAdressePriseRéseau(int entréeÉlémentDescripteur, int adresse, int adresseLongueur) {
        int valeurDescripteur = descripteurExtrémité(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return valeurDescripteur;
        if (!GestionExécution.rogner(adresseLongueur, 4)) return -14;
        int longueur = GestionExécution.nombre(adresseLongueur);
        if (longueur < 0) return -22;
        if (!GestionExécution.rogner(adresse, longueur < 16 ? longueur : 16)) return -14;
        int entréeÉlémentEmplacement = PileRéseau.numéro(poignéeRéseau[valeurDescripteur]);
        écrireAdresse(adresse, longueur, valeurCible[valeurDescripteur], entréeÉlémentEmplacement < 0 ? 0 : PileRéseau.ports[entréeÉlémentEmplacement]);
        GestionExécution.écrireNuméro(adresseLongueur, 16);
        return 0;
    }
    static int définirDélaiExpirationRecevoir(int entréeÉlémentDescripteur, int millisecondes) {
        int valeurDescripteur = descripteurExtrémité(entréeÉlémentDescripteur);
        if (valeurDescripteur < 0) return valeurDescripteur;
        if (millisecondes < 0 || millisecondes > 2000) return -22;
        recevoirMillisecondesDélaiExpiration[valeurDescripteur] = millisecondes;
        return 0;
    }
}
