// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Les tubes s’exécutent successivement par blocs de 16 KiB. Aucune simulation de processus ou de tubes concurrents. */
public final class EntréeSortieInterpréteurCommandes {
    static int[] donnéesEntrée = new int[16384], donnéesSortie = new int[16384];
    static int longueurEntrée, positionEntrée, longueurSortie, fichierEntrée = -1, fichierSortie = -1;
    static boolean entréeConduit, sortieConduit;
    static int valeurÉchec;
    static boolean autoriserInteractif = true;
    public static int estInteractif() { return autoriserInteractif && fichierEntrée < 3 && fichierSortie < 3 && !entréeConduit && !sortieConduit ? 1 : 0; }
    public static int Sortie(int valeurCanal, int valeur) {
        if (valeurCanal != 1) return 0;
        if (fichierSortie >= 3) { int valeurTraité = FichiersMémoire.écrire(fichierSortie, valeur); if (valeurTraité < 0) valeurÉchec = valeurTraité; return 1; }
        if (!sortieConduit) return 0;
        if (longueurSortie == donnéesSortie.length) valeurÉchec = -28;
        else donnéesSortie[longueurSortie++] = valeur;
        return 1;
    }
    public static int valeurEntrée() {
        if (fichierEntrée >= 3) { int valeurTraité = FichiersMémoire.lire(fichierEntrée); return valeurTraité == 256 ? -2 : valeurTraité; }
        if (entréeConduit) return positionEntrée < longueurEntrée ? donnéesEntrée[positionEntrée++] : -2;
        return -3; // Transmettre à l’UART.
    }
    static void lancer(boolean conduitPréalable, boolean conduitFinalPosition) {
        entréeConduit = conduitPréalable; sortieConduit = conduitFinalPosition;
        positionEntrée = 0; longueurSortie = 0; fichierEntrée = -1; fichierSortie = -1; valeurÉchec = 0;
    }
    static void terminaison() {
        CarteMatérielle.entréeSortieCommuter(0);
        if (fichierEntrée >= 3) FichiersMémoire.fermer(fichierEntrée);
        if (fichierSortie >= 3) FichiersMémoire.fermer(fichierSortie);
        if (sortieConduit) { longueurEntrée = longueurSortie; for (int indiceBoucle = 0; indiceBoucle < longueurSortie; indiceBoucle++) donnéesEntrée[indiceBoucle] = donnéesSortie[indiceBoucle]; }
        fichierEntrée = -1; fichierSortie = -1; entréeConduit = false; sortieConduit = false;
    }
}
