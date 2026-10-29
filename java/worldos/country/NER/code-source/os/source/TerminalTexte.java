// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Sortie série COM1 et affichage texte VGA 80x25. Le texte Unicode est envoyé au terminal série en UTF-8. */
public final class TerminalTexte {
    static int entréeÉlémentEmplacement = 0;
    static int valeurCouleur = 7;

    static void préparer() {
        Périphérique.écrireOctetEntréeSortie(0x3f9, 0);
        Périphérique.écrireOctetEntréeSortie(0x3fb, 0x80);
        Périphérique.écrireOctetEntréeSortie(0x3f8, 1);
        Périphérique.écrireOctetEntréeSortie(0x3f9, 0);
        Périphérique.écrireOctetEntréeSortie(0x3fb, 3);
        Périphérique.écrireOctetEntréeSortie(0x3fa, 0xc7);
        Périphérique.écrireOctetEntréeSortie(0x3fc, 0x0b);
        effacerEntréeÉlément();
    }

    static void octetSériel(int valeur) {
        int nombreÉlémentsRépétition = 100000;
        while ((Périphérique.lireOctetEntréeSortie(0x3fd) & 0x20) == 0 && nombreÉlémentsRépétition > 0) nombreÉlémentsRépétition--;
        if (nombreÉlémentsRépétition > 0) Périphérique.écrireOctetEntréeSortie(0x3f8, valeur);
    }

    static void effacerEntréeÉlément() {
        for (int numéro = 0; numéro < 2000; numéro++) {
            Périphérique.écrireMémoire(0xb8000 + numéro * 2, 32);
            Périphérique.écrireMémoire(0xb8001 + numéro * 2, valeurCouleur);
        }
        entréeÉlémentEmplacement = 0;
        valeurCurseur();
    }

    static void valeurCurseur() {
        Périphérique.écrireOctetEntréeSortie(0x3d4, 14);
        Périphérique.écrireOctetEntréeSortie(0x3d5, entréeÉlémentEmplacement >> 8);
        Périphérique.écrireOctetEntréeSortie(0x3d4, 15);
        Périphérique.écrireOctetEntréeSortie(0x3d5, entréeÉlémentEmplacement & 255);
    }

    static void caractèreÉcran(int valeur) {
        if (valeur == 13) return;
        if (valeur == 10) {
            entréeÉlémentEmplacement = (entréeÉlémentEmplacement / 80 + 1) * 80;
        } else if (valeur == 8) {
            if (entréeÉlémentEmplacement > 0) {
                entréeÉlémentEmplacement--;
                Périphérique.écrireMémoire(0xb8000 + entréeÉlémentEmplacement * 2, 32);
            }
        } else {
            Périphérique.écrireMémoire(0xb8000 + entréeÉlémentEmplacement * 2, valeur < 128 ? valeur : '?');
            Périphérique.écrireMémoire(0xb8001 + entréeÉlémentEmplacement * 2, valeurCouleur);
            entréeÉlémentEmplacement++;
        }
        if (entréeÉlémentEmplacement >= 2000) {
            for (int numéro = 0; numéro < 3840; numéro++)
                Périphérique.écrireMémoire(0xb8000 + numéro, Périphérique.lireMémoire(0xb80a0 + numéro));
            for (int numéro = 1920; numéro < 2000; numéro++) {
                Périphérique.écrireMémoire(0xb8000 + numéro * 2, 32);
                Périphérique.écrireMémoire(0xb8001 + numéro * 2, valeurCouleur);
            }
            entréeÉlémentEmplacement = 1920;
        }
        valeurCurseur();
    }

    static void Caractères(int valeur) {
        if (valeur < 128) {
            if (valeur == 10) octetSériel(13);
            octetSériel(valeur);
        } else if (valeur < 2048) {
            octetSériel(0xc0 | (valeur >> 6));
            octetSériel(0x80 | (valeur & 63));
        } else {
            octetSériel(0xe0 | (valeur >> 12));
            octetSériel(0x80 | ((valeur >> 6) & 63));
            octetSériel(0x80 | (valeur & 63));
        }
        caractèreÉcran(valeur);
    }

    static void écrire(String valeurContenuValeur) {
        for (int numéro = 0; numéro < valeurContenuValeur.length(); numéro++) Caractères(valeurContenuValeur.charAt(numéro));
    }

    static void écrireNuméro(int valeur) {
        // Ne convertit pas en valeur positive : Integer.MIN_VALUE reste donc sûr.
        if (valeur < 0) Caractères('-');
        else valeur = -valeur;
        int indicePosition = 1000000000;
        boolean lancer = false;
        while (indicePosition > 0) {
            int valeurChiffre = -(valeur / indicePosition);
            if (valeurChiffre != 0 || lancer || indicePosition == 1) {
                Caractères('0' + valeurChiffre);
                lancer = true;
            }
            valeur %= indicePosition;
            indicePosition /= 10;
        }
    }

    static int lireSériel() {
        if ((Périphérique.lireOctetEntréeSortie(0x3fd) & 1) != 0) return Périphérique.lireOctetEntréeSortie(0x3f8);
        return -1;
    }
}
