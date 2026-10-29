// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** État de l’interpréteur pour quatre terminaux. Le stockage des fichiers est partagé ; chemins, variables, historique et saisie sont séparés. */
public final class sessionFenêtre {
    static int[] préserverValeur = new int[4 * 30000], préparer = new int[4];
    static int élémentListeActuel, position;
    static boolean lireContinuation;
    static void valeurTableau(int[] Données, boolean valeurStocker) {
        for (int indiceBoucle = 0; indiceBoucle < Données.length; indiceBoucle++) { if (valeurStocker) préserverValeur[position++] = Données[indiceBoucle]; else Données[indiceBoucle] = préserverValeur[position++]; }
    }
    static int valeur(int valeurDonnées, boolean stockéÉtait) { if (stockéÉtait) { préserverValeur[position++] = valeurDonnées; return valeurDonnées; } return préserverValeur[position++]; }
    static void positionnerPosition(int emplacementPréservé, boolean stockéÉtait) {
        position = emplacementPréservé * 30000;
        valeurTableau(FichiersMémoire.élémentListeActuel, stockéÉtait); FichiersMémoire.longueurActuel = valeur(FichiersMémoire.longueurActuel, stockéÉtait);
        valeurTableau(SyntaxeInterpréteurCommandes.nomVariable, stockéÉtait); valeurTableau(SyntaxeInterpréteurCommandes.donnéesVariable, stockéÉtait); valeurTableau(SyntaxeInterpréteurCommandes.longueurNom, stockéÉtait); valeurTableau(SyntaxeInterpréteurCommandes.longueurValeur, stockéÉtait);
        SyntaxeInterpréteurCommandes.valeurÉtatValeur = valeur(SyntaxeInterpréteurCommandes.valeurÉtatValeur, stockéÉtait);
        valeurTableau(ÉditeurLigne.enregistrementJournal, stockéÉtait); valeurTableau(ÉditeurLigne.longueurJournal, stockéÉtait); valeurTableau(ÉditeurLigne.valeurStocker, stockéÉtait); valeurTableau(InterpréteurCommandes.ligne, stockéÉtait);
        ÉditeurLigne.nombreÉlémentsJournal = valeur(ÉditeurLigne.nombreÉlémentsJournal, stockéÉtait); ÉditeurLigne.finEnregistrementJournal = valeur(ÉditeurLigne.finEnregistrementJournal, stockéÉtait);
        ÉditeurLigne.chercherValeur = valeur(ÉditeurLigne.chercherValeur, stockéÉtait); ÉditeurLigne.longueurStocké = valeur(ÉditeurLigne.longueurStocké, stockéÉtait);
        ÉditeurLigne.taille = valeur(ÉditeurLigne.taille, stockéÉtait); ÉditeurLigne.valeurCurseur = valeur(ÉditeurLigne.valeurCurseur, stockéÉtait); ÉditeurLigne.démarrerFenêtre = valeur(ÉditeurLigne.démarrerFenêtre, stockéÉtait);
        préparer[emplacementPréservé] = 1;
    }
    static void entréeÉlémentValeurProcessus() {
        int numéroÉvènement = CarteMatérielle.terminal(12); if (numéroÉvènement == 0) return;
        positionnerPosition(élémentListeActuel, true);
        for (int indiceBoucle = 0; indiceBoucle < 4; indiceBoucle++) {
            if ((numéroÉvènement & (1 << (8 + indiceBoucle))) != 0) { CarteMatérielle.programmeUtilisateurContrôle(32 + indiceBoucle); préparer[indiceBoucle] = 0; }
            if ((numéroÉvènement & (1 << (4 + indiceBoucle))) != 0 && indiceBoucle != élémentListeActuel) préparer[indiceBoucle] = 0;
        }
        int positionSuivant = (numéroÉvènement & 15) - 1; if (positionSuivant < 0) positionSuivant = 0;
        if (préparer[positionSuivant] == 0) for (int indiceBoucle = 0; indiceBoucle < 30000; indiceBoucle++) préserverValeur[positionSuivant * 30000 + indiceBoucle] = 0;
        élémentListeActuel = positionSuivant; positionnerPosition(élémentListeActuel, false); CarteMatérielle.terminal(100 + élémentListeActuel); lireContinuation = true;
        EntréeSortieTerminal.écrire("\nTERMINAL FOCUS "); EntréeSortieTerminal.nombre(élémentListeActuel + 1); EntréeSortieTerminal.Caractères(10);
    }
    static boolean exécutionReprendre() {
        if (CarteMatérielle.programmeUtilisateurContrôle(16 + élémentListeActuel) == 0) return false;
        EntréeSortieInterpréteurCommandes.autoriserInteractif = true; EntréeSortieInterpréteurCommandes.lancer(false, false); CarteMatérielle.entréeSortieCommuter(1);
        int valeurTraité = CarteMatérielle.programmeUtilisateurContrôle(élémentListeActuel); EntréeSortieInterpréteurCommandes.terminaison();
        if (valeurTraité != -1005) { lireContinuation = false; SyntaxeInterpréteurCommandes.valeurÉtatValeur = valeurTraité < 0 ? 126 : valeurTraité; EntréeSortieTerminal.écrire("exit "); EntréeSortieTerminal.nombre(valeurTraité); EntréeSortieTerminal.Caractères(10); CarteMatérielle.terminal(3); }
        return true;
    }
}
