// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lecture par interrogation du jeu traduit 1 PC/AT PS/2 ; disposition américaine de base, Shift, Backspace et Enter. */
public final class Clavier {
    static boolean gaucheDécaler = false;
    static boolean droitDécaler = false;
    static boolean valeurExtension = false;
    static String valeurDéfaut = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String valeurDécaler = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int lire() {
        int valeurÉtatValeur = Périphérique.lireOctetEntréeSortie(0x64);
        if ((valeurÉtatValeur & 1) == 0) return -1;
        int valeur = Périphérique.lireOctetEntréeSortie(0x60);
        if ((valeurÉtatValeur & 0x20) != 0) return -1;
        if (valeur == 0xe0 || valeur == 0xe1) { valeurExtension = true; return -1; }
        if (valeurExtension) { valeurExtension = false; return -1; }
        if (valeur == 42 || valeur == 170) { gaucheDécaler = valeur == 42; return -1; }
        if (valeur == 54 || valeur == 182) { droitDécaler = valeur == 54; return -1; }
        if (valeur >= valeurDéfaut.length()) return -1;
        int Caractères = (gaucheDécaler || droitDécaler) ? valeurDécaler.charAt(valeur) : valeurDéfaut.charAt(valeur);
        return Caractères == 0 ? -1 : Caractères;
    }
}
