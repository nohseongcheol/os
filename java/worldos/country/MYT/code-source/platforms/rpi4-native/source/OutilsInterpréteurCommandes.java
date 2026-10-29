// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Outils intégrés à l’interpréteur partageant le VFS en RAM et les entrées-sorties standard. */
public final class OutilsInterpréteurCommandes {
    static int[] Données = new int[16384];
    static int fichierEntrée = -1;
    static int ouvrirFichier(int indiceArgument, int modeProcessus) {
        int valeurTraité = InterpréteurCommandes.chemin(indiceArgument); return valeurTraité < 0 ? valeurTraité : FichiersMémoire.ouvrir(modeProcessus);
    }
    static boolean préparerEntrée(int indiceArgument) {
        fichierEntrée = -1;
        if (indiceArgument < InterpréteurCommandes.nombreÉlémentsJeton) {
            fichierEntrée = ouvrirFichier(indiceArgument, 0);
            if (fichierEntrée < 0) { InterpréteurCommandes.erreur(fichierEntrée); return false; }
        }
        return true;
    }
    static int lire() {
        if (fichierEntrée >= 3) return FichiersMémoire.lire(fichierEntrée);
        while (true) {
            int donnéesOctet = CarteMatérielle.lireSériel(); if (donnéesOctet == -2 || donnéesOctet == 4) return 256;
            if (donnéesOctet == 3) { InterpréteurCommandes.résultat = 130; return 256; }
            if (donnéesOctet >= 0) return donnéesOctet; CarteMatérielle.céderProcesseur();
        }
    }
    static void fermer() { if (fichierEntrée >= 3) FichiersMémoire.fermer(fichierEntrée); fichierEntrée = -1; }
    static void valeurVue() {
        int positionDernier = InterpréteurCommandes.nombreÉlémentsJeton == 1 ? 2 : InterpréteurCommandes.nombreÉlémentsJeton;
        for (int indiceArgument = 1; indiceArgument < positionDernier; indiceArgument++) {
            if (!préparerEntrée(indiceArgument)) continue;
            int donnéesOctet; while ((donnéesOctet = lire()) != 256 && donnéesOctet >= 0) CarteMatérielle.écrireSériel(donnéesOctet);
            if (donnéesOctet < 0) InterpréteurCommandes.erreur(donnéesOctet); fermer();
        }
    }
    static void travailUnitéFichier(String numéroAction) {
        if (InterpréteurCommandes.nombreÉlémentsJeton != 2) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: mkdir/rmdir/touch Fichier\n"); return; }
        int valeurTraité = InterpréteurCommandes.chemin(1);
        if (valeurTraité >= 0) {
            if (numéroAction.charAt(0) == 'm') valeurTraité = FichiersMémoire.créerRépertoire();
            else if (numéroAction.charAt(0) == 'r') valeurTraité = FichiersMémoire.supprimerRépertoire();
            else { valeurTraité = FichiersMémoire.ouvrir(65); if (valeurTraité >= 3) valeurTraité = FichiersMémoire.fermer(valeurTraité); }
        }
        if (valeurTraité < 0) InterpréteurCommandes.erreur(valeurTraité);
    }
    static void copierValeur(boolean possèdeDéplacé) {
        if (InterpréteurCommandes.nombreÉlémentsJeton != 3) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: cp/mv original extrémitéDestination (Fichier)\n"); return; }
        int valeurTraité = InterpréteurCommandes.chemin(1); if (valeurTraité >= 0) valeurTraité = FichiersMémoire.normaliserValeur();
        if (valeurTraité < 0) { InterpréteurCommandes.erreur(valeurTraité); return; }
        int numéroOriginal = FichiersMémoire.trouverEntréeÉlément(); if (numéroOriginal < 0) { InterpréteurCommandes.erreur(-2); return; }
        int nombreÉlémentsEntréeÉlément = FichiersMémoire.longueur[numéroOriginal]; for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) Données[indiceBoucle] = FichiersMémoire.lireDonnées(numéroOriginal, indiceBoucle);
        valeurTraité = InterpréteurCommandes.chemin(2); if (valeurTraité >= 0) valeurTraité = FichiersMémoire.normaliserValeur();
        if (valeurTraité < 0) { InterpréteurCommandes.erreur(valeurTraité); return; }
        if (FichiersMémoire.trouverEntréeÉlément() == numéroOriginal) { if (!possèdeDéplacé) InterpréteurCommandes.erreur(-22); return; }
        if (possèdeDéplacé) { valeurTraité = FichiersMémoire.renommerEntréeÉlément(numéroOriginal); if (valeurTraité < 0) InterpréteurCommandes.erreur(valeurTraité); return; }
        int numéroFichierOuvert = FichiersMémoire.ouvrir(577); if (numéroFichierOuvert < 0) { InterpréteurCommandes.erreur(numéroFichierOuvert); return; }
        for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) { valeurTraité = FichiersMémoire.écrire(numéroFichierOuvert, Données[indiceBoucle]); if (valeurTraité < 0) { InterpréteurCommandes.erreur(valeurTraité); break; } }
        FichiersMémoire.fermer(numéroFichierOuvert);
    }
    static int valeurChiffre(int indiceArgument) {
        if (indiceArgument >= InterpréteurCommandes.nombreÉlémentsJeton) return -1;
        int nombreÉlémentsEntréeÉlément = 0; for (int indiceBoucle = 0; indiceBoucle < InterpréteurCommandes.longueur[indiceArgument]; indiceBoucle++) { int codeCaractère = InterpréteurCommandes.valeurJeton[InterpréteurCommandes.pointInitial[indiceArgument] + indiceBoucle]; if (codeCaractère < '0' || codeCaractère > '9' || nombreÉlémentsEntréeÉlément > 10000) return -1; nombreÉlémentsEntréeÉlément = nombreÉlémentsEntréeÉlément * 10 + codeCaractère - '0'; } return nombreÉlémentsEntréeÉlément;
    }
    static void valeurComptageEnCours() {
        int indiceArgument = 1, option = 0;
        if (InterpréteurCommandes.texteÉgal(1, "-c") || InterpréteurCommandes.texteÉgal(1, "-l") || InterpréteurCommandes.texteÉgal(1, "-w")) { option = InterpréteurCommandes.texteÉgal(1, "-c") ? 1 : InterpréteurCommandes.texteÉgal(1, "-l") ? 2 : 3; indiceArgument++; }
        if (InterpréteurCommandes.nombreÉlémentsJeton > indiceArgument + 1) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: wc [-c|-l|-w] [Fichier]\n"); return; }
        if (!préparerEntrée(indiceArgument)) return;
        int nombreÉlémentsOctet = 0, lignes = 0, nombreÉlémentsMotLexical = 0, donnéesOctet; boolean motLexical = false;
        while ((donnéesOctet = lire()) >= 0 && donnéesOctet != 256) { nombreÉlémentsOctet++; if (donnéesOctet == 10) lignes++; boolean espace = donnéesOctet == 32 || donnéesOctet >= 9 && donnéesOctet <= 13; if (!espace && !motLexical) nombreÉlémentsMotLexical++; motLexical = !espace; }
        fermer(); if (donnéesOctet < 0) { InterpréteurCommandes.erreur(donnéesOctet); return; }
        if (option != 0) EntréeSortieTerminal.nombre(option == 1 ? nombreÉlémentsOctet : option == 2 ? lignes : nombreÉlémentsMotLexical);
        else { EntréeSortieTerminal.nombre(lignes); EntréeSortieTerminal.Caractères(' '); EntréeSortieTerminal.nombre(nombreÉlémentsMotLexical); EntréeSortieTerminal.Caractères(' '); EntréeSortieTerminal.nombre(nombreÉlémentsOctet); } EntréeSortieTerminal.Caractères(10);
    }
    static void trouverEntréeÉlément() {
        if (InterpréteurCommandes.nombreÉlémentsJeton < 2 || InterpréteurCommandes.nombreÉlémentsJeton > 3) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: grep 찾을문구 [Fichier]\n"); return; }
        if (!préparerEntrée(2)) return;
        int nombreÉlémentsEntréeÉlément = 0, donnéesOctet, correspondances = 0;
        while (true) {
            donnéesOctet = lire();
            if (donnéesOctet == 10 || donnéesOctet == 256 || donnéesOctet < 0) {
                boolean trouvéÉtait = false;
                for (int indiceBoucle = 0; indiceBoucle <= nombreÉlémentsEntréeÉlément - InterpréteurCommandes.longueur[1]; indiceBoucle++) {
                    boolean estMême = true; for (int positionInterne = 0; positionInterne < InterpréteurCommandes.longueur[1]; positionInterne++) if (Données[indiceBoucle + positionInterne] != InterpréteurCommandes.valeurJeton[InterpréteurCommandes.pointInitial[1] + positionInterne]) estMême = false;
                    if (estMême) trouvéÉtait = true;
                }
                if (trouvéÉtait && (nombreÉlémentsEntréeÉlément > 0 || donnéesOctet == 10)) { for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) CarteMatérielle.écrireSériel(Données[indiceBoucle]); EntréeSortieTerminal.Caractères(10); correspondances++; }
                nombreÉlémentsEntréeÉlément = 0; if (donnéesOctet != 10) break;
            } else if (nombreÉlémentsEntréeÉlément < Données.length) Données[nombreÉlémentsEntréeÉlément++] = donnéesOctet;
            else { InterpréteurCommandes.erreur(-28); fermer(); return; }
        }
        fermer(); if (donnéesOctet < 0) InterpréteurCommandes.erreur(donnéesOctet); else if (InterpréteurCommandes.résultat == 0) InterpréteurCommandes.résultat = correspondances == 0 ? 1 : 0;
    }
    static void valeurTête(boolean positionArrière) {
        int indiceArgument = 1, lignes = 10;
        if (InterpréteurCommandes.texteÉgal(1, "-n")) { lignes = valeurChiffre(2); indiceArgument = 3; }
        if (lignes < 0 || InterpréteurCommandes.nombreÉlémentsJeton > indiceArgument + 1) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: head/tail [-n lignes] [Fichier]\n"); return; }
        if (!préparerEntrée(indiceArgument)) return;
        int nombreÉlémentsEntréeÉlément = 0, donnéesOctet;
        while ((donnéesOctet = lire()) != 256 && donnéesOctet >= 0) { if (nombreÉlémentsEntréeÉlément == Données.length) { InterpréteurCommandes.erreur(-28); fermer(); return; } Données[nombreÉlémentsEntréeÉlément++] = donnéesOctet; }
        fermer(); if (donnéesOctet < 0) { InterpréteurCommandes.erreur(donnéesOctet); return; }
        int démarrerLocal = 0, positionFin = nombreÉlémentsEntréeÉlément;
        if (lignes == 0) return;
        if (positionArrière) { int nombreÉlémentsTotal = 0; for (int indiceBoucle = nombreÉlémentsEntréeÉlément - 2; indiceBoucle >= 0; indiceBoucle--) if (Données[indiceBoucle] == 10 && ++nombreÉlémentsTotal == lignes) { démarrerLocal = indiceBoucle + 1; break; } }
        else { int nombreÉlémentsTotal = 0; for (int indiceBoucle = 0; indiceBoucle < nombreÉlémentsEntréeÉlément; indiceBoucle++) if (Données[indiceBoucle] == 10 && ++nombreÉlémentsTotal == lignes) { positionFin = indiceBoucle + 1; break; } }
        for (int indiceBoucle = démarrerLocal; indiceBoucle < positionFin; indiceBoucle++) CarteMatérielle.écrireSériel(Données[indiceBoucle]);
    }
    static void écrireEnsemble() {
        boolean ajouterFin = InterpréteurCommandes.texteÉgal(1, "-a"); int indiceArgument = ajouterFin ? 2 : 1;
        if (InterpréteurCommandes.nombreÉlémentsJeton != indiceArgument + 1) { InterpréteurCommandes.résultat = 2; EntréeSortieTerminal.écrire("사용법: tee [-a] Fichier\n"); return; }
        int numéroFichierOuvert = ouvrirFichier(indiceArgument, ajouterFin ? 1089 : 577); if (numéroFichierOuvert < 0) { InterpréteurCommandes.erreur(numéroFichierOuvert); return; }
        fichierEntrée = -1; int donnéesOctet;
        while ((donnéesOctet = lire()) != 256 && donnéesOctet >= 0) { int valeurTraité = FichiersMémoire.écrire(numéroFichierOuvert, donnéesOctet); if (valeurTraité < 0) { InterpréteurCommandes.erreur(valeurTraité); break; } CarteMatérielle.écrireSériel(donnéesOctet); }
        FichiersMémoire.fermer(numéroFichierOuvert);
    }
}
