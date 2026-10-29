// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Flux d’octets connectés dans le noyau : couche socket en boucle locale, et non pile de paquets Ethernet/TCP. */
public final class RéseauFlux {
    static int[] valeurÉtatValeur = new int[16], valeurPort = new int[16], valeurApparié = new int[16], portPairRéseau = new int[16], attendreValeur = new int[16], estAssocié = new int[16];
    static int[] valeurAvantCôté = new int[16], nombre = new int[16], Données = new int[16 * 1024];
    static int élémentListeSuivant = 50000;
    static int vérifier(int numéroFichierOuvert) { return numéroFichierOuvert >= 40 && numéroFichierOuvert < 56 && valeurÉtatValeur[numéroFichierOuvert - 40] != 0 ? numéroFichierOuvert - 40 : -1; }
    static boolean estUtiliserEntrant(int numéroPort) { for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) if (valeurÉtatValeur[indiceBoucle] != 0 && estAssocié[indiceBoucle] != 0 && valeurPort[indiceBoucle] == numéroPort) return true; return false; }
    public static int créerEntréeÉlément() {
        for (int indiceBoucle = 0; indiceBoucle < 16; indiceBoucle++) if (valeurÉtatValeur[indiceBoucle] == 0) { valeurÉtatValeur[indiceBoucle] = 1; portPairRéseau[indiceBoucle] = valeurPort[indiceBoucle] = valeurAvantCôté[indiceBoucle] = nombre[indiceBoucle] = attendreValeur[indiceBoucle] = estAssocié[indiceBoucle] = 0; valeurApparié[indiceBoucle] = -1; return indiceBoucle + 40; }
        return -24;
    }
    public static int EmballerExécutables(int numéroFichierOuvert, int AdressePriseRéseau, int numéroPort) {
        int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9;
        if (AdressePriseRéseau != 0 && AdressePriseRéseau != 0x7f000001) return -99;
        if (valeurÉtatValeur[indiceBoucle] != 1 || numéroPort < 0 || numéroPort > 65535) return -22;
        if (numéroPort == 0) { do { numéroPort = élémentListeSuivant++; if (élémentListeSuivant > 65535) élémentListeSuivant = 50000; } while (estUtiliserEntrant(numéroPort)); }
        if (estUtiliserEntrant(numéroPort)) return -98; valeurPort[indiceBoucle] = numéroPort; estAssocié[indiceBoucle] = 1; valeurÉtatValeur[indiceBoucle] = 2; return 0;
    }
    public static int écouterExtrémité(int numéroFichierOuvert, int attenteConnexions) { int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9; if (valeurÉtatValeur[indiceBoucle] != 2 || attenteConnexions < 1) return -22; valeurÉtatValeur[indiceBoucle] = 3; return 0; }
    public static int connecter(int numéroFichierOuvert, int AdressePriseRéseau, int numéroPort) {
        int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9; if (AdressePriseRéseau != 0x7f000001) return -101;
        if (numéroPort < 1 || numéroPort > 65535 || valeurÉtatValeur[indiceBoucle] > 2) return -22;
        int recevoirPage = -1; for (int positionInterne = 0; positionInterne < 16; positionInterne++) if (valeurÉtatValeur[positionInterne] == 3 && valeurPort[positionInterne] == numéroPort) recevoirPage = positionInterne;
        if (recevoirPage < 0) return -111;
        int estMisEnFile = 0; for (int positionInterne = 0; positionInterne < 16; positionInterne++) if (attendreValeur[positionInterne] == recevoirPage + 1) estMisEnFile++;
        if (estMisEnFile >= 4) return -11;
        if (valeurÉtatValeur[indiceBoucle] == 1) { int valeurTraité = EmballerExécutables(numéroFichierOuvert, 0x7f000001, 0); if (valeurTraité < 0) return valeurTraité; }
        int autre = créerEntréeÉlément(); if (autre < 0) return autre; autre -= 40;
        valeurÉtatValeur[indiceBoucle] = valeurÉtatValeur[autre] = 4; valeurApparié[indiceBoucle] = autre; valeurApparié[autre] = indiceBoucle; valeurPort[autre] = numéroPort; portPairRéseau[indiceBoucle] = numéroPort; portPairRéseau[autre] = valeurPort[indiceBoucle]; attendreValeur[autre] = recevoirPage + 1; return 0;
    }
    public static int accepterConnexion(int numéroFichierOuvert) { int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9; if (valeurÉtatValeur[indiceBoucle] != 3) return -22; for (int positionInterne = 0; positionInterne < 16; positionInterne++) if (valeurÉtatValeur[positionInterne] != 0 && attendreValeur[positionInterne] == indiceBoucle + 1) { attendreValeur[positionInterne] = 0; return positionInterne + 40; } return -11; }
    public static int écrire(int numéroFichierOuvert, int nombreÉlémentsEntréeÉlément) {
        int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9; if (valeurÉtatValeur[indiceBoucle] != 4) return -107;
        if (nombreÉlémentsEntréeÉlément < 0 || nombreÉlémentsEntréeÉlément > 512) return -22; if (nombreÉlémentsEntréeÉlément == 0) return 0;
        int positionInterne = valeurApparié[indiceBoucle]; if (positionInterne < 0) return -32; int nombreÉlémentsTotal = 1024 - nombre[positionInterne]; if (nombreÉlémentsTotal == 0) return -11; if (nombreÉlémentsTotal > nombreÉlémentsEntréeÉlément) nombreÉlémentsTotal = nombreÉlémentsEntréeÉlément;
        for (int positionComparaison = 0; positionComparaison < nombreÉlémentsTotal; positionComparaison++) Données[positionInterne * 1024 + (valeurAvantCôté[positionInterne] + nombre[positionInterne] + positionComparaison) % 1024] = RéseauBoucleRetour.valeurAvantDirection[positionComparaison]; nombre[positionInterne] += nombreÉlémentsTotal; return nombreÉlémentsTotal;
    }
    public static int lire(int numéroFichierOuvert, int nombreÉlémentsEntréeÉlément) {
        int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9; if (valeurÉtatValeur[indiceBoucle] != 4) return -107; if (nombreÉlémentsEntréeÉlément < 0 || nombreÉlémentsEntréeÉlément > 512) return -22;
        if (nombreÉlémentsEntréeÉlément == 0) return 0; if (nombre[indiceBoucle] == 0) return valeurApparié[indiceBoucle] < 0 ? 0 : -11; if (nombreÉlémentsEntréeÉlément > nombre[indiceBoucle]) nombreÉlémentsEntréeÉlément = nombre[indiceBoucle];
        for (int positionComparaison = 0; positionComparaison < nombreÉlémentsEntréeÉlément; positionComparaison++) RéseauBoucleRetour.valeurAvantDirection[positionComparaison] = Données[indiceBoucle * 1024 + (valeurAvantCôté[indiceBoucle] + positionComparaison) % 1024]; valeurAvantCôté[indiceBoucle] = (valeurAvantCôté[indiceBoucle] + nombreÉlémentsEntréeÉlément) % 1024; nombre[indiceBoucle] -= nombreÉlémentsEntréeÉlément; return nombreÉlémentsEntréeÉlément;
    }
    public static int lirePortExtrémité(int numéroFichierOuvert) { int indiceBoucle = vérifier(numéroFichierOuvert); return indiceBoucle < 0 ? -9 : valeurPort[indiceBoucle]; }
    public static int lirePortPairRéseau(int numéroFichierOuvert) { int indiceBoucle = vérifier(numéroFichierOuvert); return indiceBoucle < 0 ? -9 : portPairRéseau[indiceBoucle]; }
    public static int fermer(int numéroFichierOuvert) {
        int indiceBoucle = vérifier(numéroFichierOuvert); if (indiceBoucle < 0) return -9;
        if (valeurÉtatValeur[indiceBoucle] == 3) for (int positionInterne = 0; positionInterne < 16; positionInterne++) if (attendreValeur[positionInterne] == indiceBoucle + 1) { if (valeurApparié[positionInterne] >= 0) valeurApparié[valeurApparié[positionInterne]] = -1; valeurÉtatValeur[positionInterne] = attendreValeur[positionInterne] = estAssocié[positionInterne] = 0; }
        if (valeurApparié[indiceBoucle] >= 0) valeurApparié[valeurApparié[indiceBoucle]] = -1; valeurÉtatValeur[indiceBoucle] = estAssocié[indiceBoucle] = nombre[indiceBoucle] = attendreValeur[indiceBoucle] = 0; return 0;
    }
}
