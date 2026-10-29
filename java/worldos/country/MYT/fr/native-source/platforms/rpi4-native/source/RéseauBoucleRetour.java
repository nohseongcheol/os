// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Première couche réseau : transfert IPv4/UDP en boucle locale dans un seul noyau. Les IP externes renvoient ENETUNREACH ; cette couche ne remplace pas un pilote de paquets Ethernet/IP. Huit extrémités, quatre datagrammes par extrémité, 512 octets par datagramme. Tous les appels sont non bloquants. */
public final class RéseauBoucleRetour {
    static int[] valeurUtiliser = new int[8];
    static int[] valeurPort = new int[8];
    static int[] adresse = new int[8];
    static int[] valeurAvantCôté = new int[8];
    static int[] nombreÉlémentsÉlémentListe = new int[8];
    static int[] portReçu = new int[8];
    static int[] longueur = new int[32];
    static int[] portEnvoyé = new int[32];
    static int[] Données = new int[32 * 512];
    static int[] valeurAvantDirection = new int[512];
    static int extrémitéSuivant = 49152;
    static int vérifier(int numéro) { return numéro >= 32 && numéro < 40 && valeurUtiliser[numéro - 32] != 0 ? numéro - 32 : -1; }
    static boolean chevauchements(int numéro) {
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 8; entréeÉlémentEmplacement++) if (valeurUtiliser[entréeÉlémentEmplacement] != 0 && valeurPort[entréeÉlémentEmplacement] == numéro) return true;
        return false;
    }
    static int portTemporaire() {
        for (int valeurTentative = 0; valeurTentative < 16; valeurTentative++) {
            int candidat = extrémitéSuivant++;
            if (extrémitéSuivant > 65535) extrémitéSuivant = 49152;
            if (!chevauchements(candidat)) return candidat;
        }
        return -98;
    }
    public static int créerEntréeÉlément(int valeurRégion, int valeurGenre, int valeurContrat) {
        if (valeurRégion != 2) return -97;
        if (valeurGenre != 2 || (valeurContrat != 0 && valeurContrat != 17)) return -93;
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 8; entréeÉlémentEmplacement++) if (valeurUtiliser[entréeÉlémentEmplacement] == 0) {
            valeurUtiliser[entréeÉlémentEmplacement] = 1; valeurPort[entréeÉlémentEmplacement] = 0; adresse[entréeÉlémentEmplacement] = 0; valeurAvantCôté[entréeÉlémentEmplacement] = 0; nombreÉlémentsÉlémentListe[entréeÉlémentEmplacement] = 0; portReçu[entréeÉlémentEmplacement] = 0;
            return entréeÉlémentEmplacement + 32;
        }
        return -24;
    }
    public static int EmballerExécutables(int numéro, int adresseRéseau, int numéroPortExtrémité) {
        int entréeÉlémentEmplacement = vérifier(numéro);
        if (entréeÉlémentEmplacement < 0) return -9;
        if (adresseRéseau != 0 && adresseRéseau != 0x7f000001) return -99;
        if (valeurPort[entréeÉlémentEmplacement] != 0 || numéroPortExtrémité < 0 || numéroPortExtrémité > 65535) return -22;
        if (numéroPortExtrémité == 0) numéroPortExtrémité = portTemporaire();
        if (numéroPortExtrémité < 0) return numéroPortExtrémité;
        if (chevauchements(numéroPortExtrémité)) return -98;
        valeurPort[entréeÉlémentEmplacement] = numéroPortExtrémité; adresse[entréeÉlémentEmplacement] = adresseRéseau; return 0;
    }
    public static int placerDonnées(int numéro, int valeur) {
        if (numéro < 0 || numéro >= 512) return -22;
        valeurAvantDirection[numéro] = valeur & 255; return 0;
    }
    public static int lireDonnées(int numéro) { return numéro >= 0 && numéro < 512 ? valeurAvantDirection[numéro] : -22; }
    public static int envoyer(int numéro, int adresseRéseau, int numéroPortExtrémité, int taille) {
        int entréeÉlémentEmplacement = vérifier(numéro);
        if (entréeÉlémentEmplacement < 0) return -9;
        if (adresseRéseau != 0x7f000001) return -101;
        if (numéroPortExtrémité < 1 || numéroPortExtrémité > 65535) return -22;
        if (taille < 0 || taille > 512) return -90;
        if (valeurPort[entréeÉlémentEmplacement] == 0) {
            int résultat = EmballerExécutables(numéro, 0x7f000001, 0);
            if (résultat < 0) return résultat;
        }
        int valeurDestination = -1;
        for (int candidat = 0; candidat < 8; candidat++) if (valeurUtiliser[candidat] != 0 && valeurPort[candidat] == numéroPortExtrémité) valeurDestination = candidat;
        if (valeurDestination < 0) return -111;
        if (nombreÉlémentsÉlémentListe[valeurDestination] == 4) return -11;
        int indicePosition = valeurDestination * 4 + (valeurAvantCôté[valeurDestination] + nombreÉlémentsÉlémentListe[valeurDestination]) % 4;
        for (int valeurOctet = 0; valeurOctet < taille; valeurOctet++) Données[indicePosition * 512 + valeurOctet] = valeurAvantDirection[valeurOctet];
        longueur[indicePosition] = taille; portEnvoyé[indicePosition] = valeurPort[entréeÉlémentEmplacement]; nombreÉlémentsÉlémentListe[valeurDestination]++;
        return taille;
    }
    public static int recevoir(int numéro, int valeurCapacité) {
        int entréeÉlémentEmplacement = vérifier(numéro);
        if (entréeÉlémentEmplacement < 0) return -9;
        if (valeurCapacité < 0 || valeurCapacité > 512) return -22;
        if (nombreÉlémentsÉlémentListe[entréeÉlémentEmplacement] == 0) return -11;
        int indicePosition = entréeÉlémentEmplacement * 4 + valeurAvantCôté[entréeÉlémentEmplacement];
        int taille = longueur[indicePosition] < valeurCapacité ? longueur[indicePosition] : valeurCapacité;
        for (int valeurOctet = 0; valeurOctet < taille; valeurOctet++) valeurAvantDirection[valeurOctet] = Données[indicePosition * 512 + valeurOctet];
        portReçu[entréeÉlémentEmplacement] = portEnvoyé[indicePosition]; valeurAvantCôté[entréeÉlémentEmplacement] = (valeurAvantCôté[entréeÉlémentEmplacement] + 1) % 4; nombreÉlémentsÉlémentListe[entréeÉlémentEmplacement]--;
        return taille;
    }
    public static int lirePortExtrémité(int numéro) { int entréeÉlémentEmplacement = vérifier(numéro); return entréeÉlémentEmplacement < 0 ? -9 : valeurPort[entréeÉlémentEmplacement]; }
    public static int lireAdresse(int numéro) { int entréeÉlémentEmplacement = vérifier(numéro); return entréeÉlémentEmplacement < 0 ? -9 : adresse[entréeÉlémentEmplacement]; }
    public static int extrémitéÉmetteur(int numéro) { int entréeÉlémentEmplacement = vérifier(numéro); return entréeÉlémentEmplacement < 0 ? -9 : portReçu[entréeÉlémentEmplacement]; }
    public static int fermer(int numéro) {
        int entréeÉlémentEmplacement = vérifier(numéro); if (entréeÉlémentEmplacement < 0) return -9;
        valeurUtiliser[entréeÉlémentEmplacement] = 0; nombreÉlémentsÉlémentListe[entréeÉlémentEmplacement] = 0; valeurPort[entréeÉlémentEmplacement] = 0; return 0;
    }
}
