// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Secteurs logiques de 512 octets du premier périphérique IDE. Cette couche ne formate ni n’efface de périphérique arbitraire. */
public final class ConnexionStockage {
    static boolean estDisponible = false;
    static int[] donnéesSection = new int[512];
    static void attendreBrièvement() {
        for (int numéro = 0; numéro < 4; numéro++) Périphérique.lireOctetEntréeSortie(0x3f6);
    }
    static int attendrePrêtJusquÀ(boolean requisDonnées) {
        int lancer = Périphérique.millisecondes();
        while (Périphérique.millisecondes() - lancer < 500) {
            int valeurÉtatValeur = Périphérique.lireOctetEntréeSortie(0x1f7);
            if (valeurÉtatValeur == 0 || valeurÉtatValeur == 255) return -19;
            if ((valeurÉtatValeur & 128) == 0) {
                if ((valeurÉtatValeur & 33) != 0) return -5;
                if (!requisDonnées || (valeurÉtatValeur & 8) != 0) return 0;
            }
            Périphérique.céderBrièvement();
        }
        return -110;
    }
    static int requête(int valeurSection, int commande) {
        if (valeurSection < 0 || valeurSection >= 2048) return -22;
        Périphérique.écrireOctetEntréeSortie(0x3f6, 2); // Interrogation ; l’IRQ IDE n’est pas utilisée.
        Périphérique.écrireOctetEntréeSortie(0x1f6, 0xe0); attendreBrièvement();
        int résultat = attendrePrêtJusquÀ(false);
        if (résultat < 0) return résultat;
        Périphérique.écrireOctetEntréeSortie(0x1f2, 1);
        Périphérique.écrireOctetEntréeSortie(0x1f3, valeurSection & 255);
        Périphérique.écrireOctetEntréeSortie(0x1f4, (valeurSection >>> 8) & 255);
        Périphérique.écrireOctetEntréeSortie(0x1f5, 0);
        Périphérique.écrireOctetEntréeSortie(0x1f7, commande); attendreBrièvement();
        return attendrePrêtJusquÀ(true);
    }
    static int lire(int valeurSection) {
        int résultat = requête(valeurSection, 0x20);
        if (résultat < 0) return résultat;
        for (int numéro = 0; numéro < 256; numéro++) {
            int valeur = Périphérique.lireCourtEntréeSortie(0x1f0);
            donnéesSection[numéro * 2] = valeur & 255; donnéesSection[numéro * 2 + 1] = valeur >>> 8;
        }
        attendreBrièvement(); return attendrePrêtJusquÀ(false);
    }
    static int écrire(int valeurSection) {
        if (!estDisponible || valeurSection < 1 || valeurSection > 518) return -19;
        int résultat = requête(valeurSection, 0x30);
        if (résultat < 0) return résultat;
        for (int numéro = 0; numéro < 256; numéro++)
            Périphérique.écrireCourtEntréeSortie(0x1f0, donnéesSection[numéro * 2] | donnéesSection[numéro * 2 + 1] << 8);
        attendreBrièvement(); return attendrePrêtJusquÀ(false);
    }
    static int sortieViderTampon() {
        if (!estDisponible) return -19;
        Périphérique.écrireOctetEntréeSortie(0x1f7, 0xe7); attendreBrièvement();
        return attendrePrêtJusquÀ(false);
    }
    static int analyserEntier(int position) {
        return donnéesSection[position] | donnéesSection[position + 1] << 8 | donnéesSection[position + 2] << 16 | donnéesSection[position + 3] << 24;
    }
    static void écrireValeurEntier(int position, int valeur) {
        for (int numéro = 0; numéro < 4; numéro++) donnéesSection[position + numéro] = (valeur >>> (numéro * 8)) & 255;
    }
}
