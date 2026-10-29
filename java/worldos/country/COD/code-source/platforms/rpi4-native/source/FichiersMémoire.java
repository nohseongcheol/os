// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 64 fichiers en RAM de 16384 octets chacun, 16 descripteurs. Toutes les données et règles sont en Java. Les appels ne cèdent pas l’exécution : ils sont donc atomiques entre tâches coopératives sur l’unique cœur actuel. Il ne s’agit ni d’un stockage sur disque ni d’une réalisation complète de POSIX. Les retours négatifs sont des numéros d’erreur. */
public final class FichiersMémoire {
    static final int nombreÉlémentsFichier = 64;
    static int[] nom = new int[nombreÉlémentsFichier * 64];
    static int[] longueurNom = new int[nombreÉlémentsFichier];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] valeurContenuValeur = new int[nombreÉlémentsFichier * 4096];
    static int[] longueur = new int[nombreÉlémentsFichier];
    static int[] nombreÉlémentsRéférence = new int[nombreÉlémentsFichier];
    static int[] valeurUtiliser = new int[16];
    static int[] valeurCible = new int[16];
    static int[] position = new int[16];
    static int[] modeMéthode = new int[16];
    static int[] chemin = new int[64];
    static int longueurChemin;

    public static int limiteFichier() { return nombreÉlémentsFichier; }
    static int lireDonnées(int Fichier, int indicePosition) { return (valeurContenuValeur[Fichier * 4096 + indicePosition / 4] >>> ((indicePosition & 3) * 8)) & 255; }
    static void écrireDonnées(int Fichier, int indicePosition, int valeur) {
        int entréeÉlémentEmplacement = Fichier * 4096 + indicePosition / 4, valeurDéplacer = (indicePosition & 3) * 8;
        valeurContenuValeur[entréeÉlémentEmplacement] = (valeurContenuValeur[entréeÉlémentEmplacement] & ~(255 << valeurDéplacer)) | ((valeur & 255) << valeurDéplacer);
    }

    public static int démarrerChemin(int taille) {
        longueurChemin = 0;
        if (taille < 1 || taille > 63) return -36;
        longueurChemin = taille;
        for (int indiceBoucle = 0; indiceBoucle < taille; indiceBoucle++) chemin[indiceBoucle] = 0;
        return 0;
    }
    public static int octetChemin(int numéro, int valeur) {
        if (numéro < 0 || numéro >= longueurChemin || valeur < 1 || valeur > 255) return -22;
        chemin[numéro] = valeur; return 0;
    }
    static int trouverEntréeÉlément() {
        for (int indiceFichier = 0; indiceFichier < nombreÉlémentsFichier; indiceFichier++) if (longueurNom[indiceFichier] > 0 && longueurNom[indiceFichier] == longueurCanonique && valeurPréfixe(nom, indiceFichier * 64, longueurNom[indiceFichier], valeurCanonique, longueurCanonique)) return indiceFichier;
        return -1;
    }
    public static int ouvrir(int valeurDrapeaux) {
        if (longueurChemin == 0 || (valeurDrapeaux & ~0x6c3) != 0 || (valeurDrapeaux & 3) == 3) return -22;
        for (int indiceBoucle = 0; indiceBoucle < longueurChemin; indiceBoucle++) if (chemin[indiceBoucle] == 0) return -22;
        if ((valeurDrapeaux & 0x200) != 0 && (valeurDrapeaux & 3) == 0) return -22;
        int résultat = normaliserValeur(); if (résultat < 0) return résultat;
        if (trouverRépertoire(longueurCanonique) >= 0) return -21;
        résultat = contrôlerParent(); if (résultat < 0) return résultat;
        int Fichier = trouverEntréeÉlément();
        if (Fichier >= 0 && (valeurDrapeaux & 0xc0) == 0xc0) return -17;
        if (Fichier < 0 && (valeurDrapeaux & 0x40) == 0) return -2;
        int entréeÉlémentDescripteur = -1;
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) if (valeurUtiliser[indiceBoucle] == 0) { entréeÉlémentDescripteur = indiceBoucle; break; }
        if (entréeÉlémentDescripteur < 0) return -24;
        if (Fichier < 0) {
            for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsFichier; indiceBoucle++) if (longueurNom[indiceBoucle] == 0 && nombreÉlémentsRéférence[indiceBoucle] == 0) { Fichier = indiceBoucle; break; }
            if (Fichier < 0) return -28;
            longueurNom[Fichier] = longueurCanonique;
            for (int indiceBoucle = 0; indiceBoucle < longueurCanonique; indiceBoucle++) nom[Fichier * 64 + indiceBoucle] = valeurCanonique[indiceBoucle];
            longueur[Fichier] = 0;
        }
        if ((valeurDrapeaux & 0x200) != 0) longueur[Fichier] = 0;
        valeurUtiliser[entréeÉlémentDescripteur] = 1; valeurCible[entréeÉlémentDescripteur] = Fichier; position[entréeÉlémentDescripteur] = 0; modeMéthode[entréeÉlémentDescripteur] = valeurDrapeaux;
        nombreÉlémentsRéférence[Fichier]++;
        return entréeÉlémentDescripteur + 3;
    }
    static int vérifier(int entréeÉlémentDescripteur) {
        return entréeÉlémentDescripteur >= 3 && entréeÉlémentDescripteur < 19 && valeurUtiliser[entréeÉlémentDescripteur - 3] != 0 ? entréeÉlémentDescripteur - 3 : -1;
    }
    public static int lire(int entréeÉlémentDescripteur) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur);
        if (entréeÉlémentEmplacement < 0 || (modeMéthode[entréeÉlémentEmplacement] & 3) == 1) return -9;
        int Fichier = valeurCible[entréeÉlémentEmplacement];
        if (position[entréeÉlémentEmplacement] >= longueur[Fichier]) return 256; // Distinguer EOF des véritables octets 0x00..0xff.
        return lireDonnées(Fichier, position[entréeÉlémentEmplacement]++);
    }
    public static int écrire(int entréeÉlémentDescripteur, int valeur) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur);
        if (entréeÉlémentEmplacement < 0 || (modeMéthode[entréeÉlémentEmplacement] & 3) == 0) return -9;
        int Fichier = valeurCible[entréeÉlémentEmplacement];
        if ((modeMéthode[entréeÉlémentEmplacement] & 0x400) != 0) position[entréeÉlémentEmplacement] = longueur[Fichier];
        if (position[entréeÉlémentEmplacement] >= 16384) return -28;
        while (longueur[Fichier] < position[entréeÉlémentEmplacement]) écrireDonnées(Fichier, longueur[Fichier]++, 0);
        écrireDonnées(Fichier, position[entréeÉlémentEmplacement]++, valeur);
        if (longueur[Fichier] < position[entréeÉlémentEmplacement]) longueur[Fichier] = position[entréeÉlémentEmplacement];
        return 1;
    }
    public static int positionnerPosition(int entréeÉlémentDescripteur, int valeurDistance, int racineProjet) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur);
        if (entréeÉlémentEmplacement < 0) return -9;
        if (racineProjet < 0 || racineProjet > 2 || valeurDistance < -16384 || valeurDistance > 16384) return -22;
        int positionNouveau = valeurDistance + (racineProjet == 0 ? 0 : racineProjet == 1 ? position[entréeÉlémentEmplacement] : longueur[valeurCible[entréeÉlémentEmplacement]]);
        if (positionNouveau < 0 || positionNouveau > 16384) return -22;
        position[entréeÉlémentEmplacement] = positionNouveau; return positionNouveau;
    }
    public static int fermer(int entréeÉlémentDescripteur) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur);
        if (entréeÉlémentEmplacement < 0) return -9;
        nombreÉlémentsRéférence[valeurCible[entréeÉlémentEmplacement]]--; valeurUtiliser[entréeÉlémentEmplacement] = 0; return 0;
    }
    public static int taille(int entréeÉlémentDescripteur) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur); return entréeÉlémentEmplacement < 0 ? -9 : longueur[valeurCible[entréeÉlémentEmplacement]];
    }
    public static int définirLongueur(int entréeÉlémentDescripteur, int taille) {
        int entréeÉlémentEmplacement = vérifier(entréeÉlémentDescripteur);
        if (entréeÉlémentEmplacement < 0 || (modeMéthode[entréeÉlémentEmplacement] & 3) == 0) return -9;
        if (taille < 0 || taille > 16384) return -22;
        int Fichier = valeurCible[entréeÉlémentEmplacement];
        while (longueur[Fichier] < taille) écrireDonnées(Fichier, longueur[Fichier]++, 0);
        longueur[Fichier] = taille; return 0;
    }
    public static int effacerEntréeÉlément() {
        if (longueurChemin == 0) return -22;
        int résultat = normaliserValeur(); if (résultat < 0) return résultat;
        if (trouverRépertoire(longueurCanonique) >= 0) return -21;
        résultat = contrôlerParent(); if (résultat < 0) return résultat;
        int Fichier = trouverEntréeÉlément();
        if (Fichier < 0) return -2;
        longueurNom[Fichier] = 0; return 0; // Conserver un fichier ouvert jusqu’au dernier close.
    }
    static void listeEntréeÉlément() {
        démarrerChemin(1); octetChemin(0, '.'); entréesListeChemin();
    }
    public static int longueurNomExporté(int numéro) {
        if (numéro < 0 || numéro >= nombreÉlémentsFichier || longueurNom[numéro] == 0) return 0;
        for (int indiceBoucle = 0; indiceBoucle < longueurNom[numéro]; indiceBoucle++) if (nom[numéro * 64 + indiceBoucle] == '/') return 0;
        return longueurNom[numéro];
    }
    public static int octetNomExporté(int numéro, int indicePosition) {
        return numéro >= 0 && numéro < nombreÉlémentsFichier && indicePosition >= 0 && indicePosition < longueurNom[numéro] ? nom[numéro * 64 + indicePosition] : -22;
    }
    public static int tailleFichierExporté(int numéro) { return numéro >= 0 && numéro < nombreÉlémentsFichier ? longueur[numéro] : -22; }
    static int[] valeurCanonique = new int[64], élémentListeActuel = new int[64], nomRépertoire = new int[16 * 64], longueurRépertoire = new int[16];
    static int longueurCanonique, longueurActuel;
    static boolean valeurPréfixe(int[] listeNoms, int lancer, int valeurChemin, int[] valeurAvantCôté, int cheminPréalable) {
        if (valeurChemin < cheminPréalable) return false;
        for (int indiceBoucle = 0; indiceBoucle < cheminPréalable; indiceBoucle++) if (listeNoms[lancer + indiceBoucle] != valeurAvantCôté[indiceBoucle]) return false;
        return true;
    }
    static int normaliserValeur() {
        if (longueurChemin == 0) return -22;
        longueurCanonique = chemin[0] == '/' ? 0 : longueurActuel;
        for (int indiceBoucle = 0; indiceBoucle < longueurCanonique; indiceBoucle++) valeurCanonique[indiceBoucle] = élémentListeActuel[indiceBoucle];
        int lireCurseur = 0;
        while (lireCurseur < longueurChemin) {
            while (lireCurseur < longueurChemin && chemin[lireCurseur] == '/') lireCurseur++;
            int démarrerPosition = lireCurseur; while (lireCurseur < longueurChemin && chemin[lireCurseur] != '/') { if (chemin[lireCurseur] == 0) return -22; lireCurseur++; }
            int nombreÉlémentsEntréeÉlément = lireCurseur - démarrerPosition; if (nombreÉlémentsEntréeÉlément == 0 || nombreÉlémentsEntréeÉlément == 1 && chemin[démarrerPosition] == '.') continue;
            if (nombreÉlémentsEntréeÉlément == 2 && chemin[démarrerPosition] == '.' && chemin[démarrerPosition + 1] == '.') {
                while (longueurCanonique > 0 && valeurCanonique[longueurCanonique - 1] != '/') longueurCanonique--;
                if (longueurCanonique > 0) longueurCanonique--;
                continue;
            }
            if (longueurCanonique + nombreÉlémentsEntréeÉlément + (longueurCanonique == 0 ? 0 : 1) > 63) return -36;
            if (longueurCanonique > 0) valeurCanonique[longueurCanonique++] = '/';
            for (int indiceBoucle = démarrerPosition; indiceBoucle < lireCurseur; indiceBoucle++) valeurCanonique[longueurCanonique++] = chemin[indiceBoucle];
        }
        return 0;
    }
    static int trouverRépertoire(int nombreÉlémentsEntréeÉlément) {
        if (nombreÉlémentsEntréeÉlément == 0) return 0;
        for (int indiceBoucle = 1; indiceBoucle < 16; indiceBoucle++) if (longueurRépertoire[indiceBoucle] == nombreÉlémentsEntréeÉlément && valeurPréfixe(nomRépertoire, indiceBoucle * 64, nombreÉlémentsEntréeÉlément, valeurCanonique, nombreÉlémentsEntréeÉlément)) return indiceBoucle;
        return -1;
    }
    static int contrôlerParent() {
        int nombreÉlémentsEntréeÉlément = longueurCanonique; while (nombreÉlémentsEntréeÉlément > 0 && valeurCanonique[nombreÉlémentsEntréeÉlément - 1] != '/') nombreÉlémentsEntréeÉlément--;
        return trouverRépertoire(nombreÉlémentsEntréeÉlément == 0 ? 0 : nombreÉlémentsEntréeÉlément - 1) < 0 ? -2 : 0;
    }
    public static int créerRépertoire() {
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        if (trouverRépertoire(longueurCanonique) >= 0 || trouverEntréeÉlément() >= 0) return -17;
        valeurTraité = contrôlerParent(); if (valeurTraité < 0) return valeurTraité;
        for (int indiceBoucle = 1; indiceBoucle < 16; indiceBoucle++) if (longueurRépertoire[indiceBoucle] == 0) {
            longueurRépertoire[indiceBoucle] = longueurCanonique; for (int positionInterne = 0; positionInterne < longueurCanonique; positionInterne++) nomRépertoire[indiceBoucle * 64 + positionInterne] = valeurCanonique[positionInterne]; return 0;
        }
        return -28;
    }
    public static int genreEntréeÉlément() {
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        if (trouverRépertoire(longueurCanonique) >= 0) return 2;
        return trouverEntréeÉlément() >= 0 ? 1 : 0;
    }
    public static int changerRépertoire() {
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        if (trouverRépertoire(longueurCanonique) < 0) return -2;
        longueurActuel = longueurCanonique; for (int indiceBoucle = 0; indiceBoucle < longueurActuel; indiceBoucle++) élémentListeActuel[indiceBoucle] = valeurCanonique[indiceBoucle]; return 0;
    }
    public static int supprimerRépertoire() {
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        int numéroRépertoire = trouverRépertoire(longueurCanonique); if (numéroRépertoire < 0) return -2; if (numéroRépertoire == 0) return -16;
        if (longueurActuel == longueurCanonique && valeurPréfixe(élémentListeActuel, 0, longueurActuel, valeurCanonique, longueurCanonique)) return -16;
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsFichier; indiceBoucle++) {
            if (longueurNom[indiceBoucle] > longueurCanonique && valeurPréfixe(nom, indiceBoucle * 64, longueurNom[indiceBoucle], valeurCanonique, longueurCanonique) && nom[indiceBoucle * 64 + longueurCanonique] == '/') return -39;
        }
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) {
            if (longueurRépertoire[indiceBoucle] > longueurCanonique && valeurPréfixe(nomRépertoire, indiceBoucle * 64, longueurRépertoire[indiceBoucle], valeurCanonique, longueurCanonique) && nomRépertoire[indiceBoucle * 64 + longueurCanonique] == '/') return -39;
        }
        longueurRépertoire[numéroRépertoire] = 0; return 0;
    }
    public static int renommerEntréeÉlément(int numéroOriginal) {
        if (numéroOriginal < 0 || numéroOriginal >= nombreÉlémentsFichier || longueurNom[numéroOriginal] == 0) return -2;
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        if (trouverRépertoire(longueurCanonique) >= 0) return -21;
        valeurTraité = contrôlerParent(); if (valeurTraité < 0) return valeurTraité;
        int valeurPrécédentÉlément = trouverEntréeÉlément(); if (valeurPrécédentÉlément == numéroOriginal) return 0;
        if (valeurPrécédentÉlément >= 0) longueurNom[valeurPrécédentÉlément] = 0;
        longueurNom[numéroOriginal] = longueurCanonique; for (int indiceBoucle = 0; indiceBoucle < longueurCanonique; indiceBoucle++) nom[numéroOriginal * 64 + indiceBoucle] = valeurCanonique[indiceBoucle]; return 0;
    }
    static int démarrerEntréeÉlément(int[] tableauDonnées, int pointInitial, int nombreÉlémentsEntréeÉlément) {
        if (!valeurPréfixe(tableauDonnées, pointInitial, nombreÉlémentsEntréeÉlément, valeurCanonique, longueurCanonique)) return -1;
        int démarrerPosition = longueurCanonique;
        if (démarrerPosition > 0) { if (nombreÉlémentsEntréeÉlément <= démarrerPosition || tableauDonnées[pointInitial + démarrerPosition] != '/') return -1; démarrerPosition++; }
        if (nombreÉlémentsEntréeÉlément <= démarrerPosition) return -1;
        for (int indiceBoucle = démarrerPosition; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) if (tableauDonnées[pointInitial + indiceBoucle] == '/') return -1;
        return démarrerPosition;
    }
    static void écrireActuel() { EntréeSortieTerminal.Caractères('/'); for (int indiceBoucle = 0; indiceBoucle < longueurActuel; indiceBoucle++) CarteMatérielle.écrireSériel(élémentListeActuel[indiceBoucle]); }
    static int entréesListeChemin() {
        int valeurTraité = normaliserValeur(); if (valeurTraité < 0) return valeurTraité;
        int valeurCibleFichier = trouverEntréeÉlément();
        if (valeurCibleFichier >= 0) { for (int indiceBoucle = 0; indiceBoucle < longueurCanonique; indiceBoucle++) CarteMatérielle.écrireSériel(valeurCanonique[indiceBoucle]); EntréeSortieTerminal.écrire("  "); EntréeSortieTerminal.nombre(longueur[valeurCibleFichier]); EntréeSortieTerminal.écrire("valeurOctet(주기억 Fichier)\n"); return 0; }
        if (trouverRépertoire(longueurCanonique) < 0) return -2;
        for (int valeurFinalPosition = 1; valeurFinalPosition < 16; valeurFinalPosition++) if (longueurRépertoire[valeurFinalPosition] > 0) {
            int démarrerPosition = démarrerEntréeÉlément(nomRépertoire, valeurFinalPosition * 64, longueurRépertoire[valeurFinalPosition]); if (démarrerPosition < 0) continue;
            for (int indiceBoucle = démarrerPosition; indiceBoucle < longueurRépertoire[valeurFinalPosition]; indiceBoucle++) CarteMatérielle.écrireSériel(nomRépertoire[valeurFinalPosition * 64 + indiceBoucle]); EntréeSortieTerminal.écrire("/\n");
        }
        for (int indiceFichier = 0; indiceFichier < nombreÉlémentsFichier; indiceFichier++) if (longueurNom[indiceFichier] > 0) {
            int démarrerPosition = démarrerEntréeÉlément(nom, indiceFichier * 64, longueurNom[indiceFichier]); if (démarrerPosition < 0) continue;
            for (int indiceBoucle = démarrerPosition; indiceBoucle < longueurNom[indiceFichier]; indiceBoucle++) CarteMatérielle.écrireSériel(nom[indiceFichier * 64 + indiceBoucle]);
            EntréeSortieTerminal.écrire("  "); EntréeSortieTerminal.nombre(longueur[indiceFichier]); EntréeSortieTerminal.écrire("valeurOctet(주기억 Fichier)\n");
        }
        return 0;
    }
}
