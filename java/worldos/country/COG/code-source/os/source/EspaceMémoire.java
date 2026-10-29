// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Consultation des informations de démarrage et allocation/libération de zones de tâche fixes de 4 KiB ; pas un gestionnaire général de pages physiques. */
public final class EspaceMémoire {
    static int[] valeurSection = new int[8192];
    static int[] valeurUtiliser = new int[8];

    static int analyserEntier(int adresse) {
        return Périphérique.lireMémoire(adresse) | (Périphérique.lireMémoire(adresse + 1) << 8)
            | (Périphérique.lireMémoire(adresse + 2) << 16) | (Périphérique.lireMémoire(adresse + 3) << 24);
    }

    static int tailleMémoireSupérieur() {
        int informationSystème = Périphérique.informationAmorçage();
        if (Périphérique.marqueurAmorçage() != 0x2badb002 || informationSystème == 0 || (analyserEntier(informationSystème) & 1) == 0) return -1;
        return analyserEntier(informationSystème + 8);
    }

    static int allouerStockage() {
        for (int numéro = 0; numéro < valeurUtiliser.length; numéro++) {
            if (valeurUtiliser[numéro] == 0) {
                valeurUtiliser[numéro] = 1;
                for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 1024; entréeÉlémentEmplacement++) valeurSection[numéro * 1024 + entréeÉlémentEmplacement] = 0;
                return numéro;
            }
        }
        return -1;
    }

    static boolean résultatRetourner(int numéro) {
        if (numéro < 0 || numéro >= valeurUtiliser.length || valeurUtiliser[numéro] == 0) return false;
        valeurUtiliser[numéro] = 0;
        return true;
    }

    static int nombreÉlémentsEntréeÉlémentUtilisé() {
        int nombreÉlémentsÉlémentListe = 0;
        for (int numéro = 0; numéro < valeurUtiliser.length; numéro++) nombreÉlémentsÉlémentListe += valeurUtiliser[numéro];
        return nombreÉlémentsÉlémentListe;
    }
}
