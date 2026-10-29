// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Petit lanceur sur le tampon d’image, piloté par TAB/ENTER/Q sur UART. Interface limitée avec une police latine 5x7 définie par le projet, sans Swing, USB HID ni méthode de saisie complète. */
public final class Bureau {
    static String valeursCaractère = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // Sept lignes par glyphe, chacune exprimée par deux chiffres hexadécimaux. Police 5x7 propre au projet.
    static String listeFormes =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int valeurChiffre(int valeurCaractère) { return valeurCaractère <= '9' ? valeurCaractère - '0' : valeurCaractère - 'A' + 10; }
    static void texte(int positionHorizontal, int positionVertical, String valeurContenuValeur, int valeurCouleur) {
        for (int valeurCaractère = 0; valeurCaractère < valeurContenuValeur.length(); valeurCaractère++) {
            int valeurTrouvé = -1;
            for (int candidat = 0; candidat < valeursCaractère.length(); candidat++) if (valeursCaractère.charAt(candidat) == valeurContenuValeur.charAt(valeurCaractère)) valeurTrouvé = candidat;
            if (valeurTrouvé < 0) continue;
            for (int valeurRangée = 0; valeurRangée < 7; valeurRangée++) {
                int position = valeurTrouvé * 14 + valeurRangée * 2;
                int valeurBit = valeurChiffre(listeFormes.charAt(position)) * 16 + valeurChiffre(listeFormes.charAt(position + 1));
                for (int valeurColonne = 0; valeurColonne < 5; valeurColonne++) if ((valeurBit & (16 >> valeurColonne)) != 0)
                    Noyau.rectangle(positionHorizontal + valeurCaractère * 12 + valeurColonne * 2, positionVertical + valeurRangée * 2, 2, 2, valeurCouleur);
            }
        }
    }
    static void écranPeindre(int valeurSélection, String valeurÉtatValeur) {
        Noyau.rectangle(0, 0, CarteMatérielle.largeurÉcran(), CarteMatérielle.hauteurÉcran(), 0x302018);
        Noyau.rectangle(32, 24, 576, 432, 0xefe8e2);
        Noyau.rectangle(32, 24, 576, 48, 0x905020);
        texte(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int numéro = 0; numéro < 5; numéro++) {
            Noyau.rectangle(64, 112 + numéro * 52, 512, 40, numéro == valeurSélection ? 0xd0a040 : 0xd8d0c8);
            texte(84, 128 + numéro * 52, numéro == 0 ? "RUN C++ FILE PROGRAM" : numéro == 1 ? "RUN UDP LOOPBACK" : numéro == 2 ? "COMPILE AND RUN JAVA" : numéro == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        texte(68, 384, valeurÉtatValeur, 0x205020);
        texte(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void exécuterCommande() {
        if (CarteMatérielle.préparerÉcran() == 0) { EntréeSortieTerminal.écrire("GUI unavailable\n"); return; }
        int valeurSélection = 0;
        String valeurÉtatValeur = "READY";
        boolean lignePrécédentÉlément = InterpréteurCommandes.lignePrécédentÉlément;
        écranPeindre(valeurSélection, valeurÉtatValeur);
        EntréeSortieTerminal.écrire("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int valeurEntrée = CarteMatérielle.lireSériel();
            if (valeurEntrée < 0) { CarteMatérielle.céderProcesseur(); continue; }
            if (valeurEntrée == 10 && lignePrécédentÉlément) { lignePrécédentÉlément = false; continue; }
            lignePrécédentÉlément = valeurEntrée == 13;
            if (valeurEntrée >= '1' && valeurEntrée <= '5') { valeurSélection = valeurEntrée - '1'; valeurEntrée = 13; }
            if (valeurEntrée == 't' || valeurEntrée == 'T') { InterpréteurCommandes.terminal(false); return; }
            if (valeurEntrée == 'q' || valeurEntrée == 'Q' || valeurEntrée == 27) break;
            if (valeurEntrée == 9 || valeurEntrée == 'j') {
                valeurSélection = (valeurSélection + 1) % 5; écranPeindre(valeurSélection, valeurÉtatValeur); EntréeSortieTerminal.écrire("GUI FOCUS "); EntréeSortieTerminal.nombre(valeurSélection); EntréeSortieTerminal.Caractères(10);
            } else if (valeurEntrée == 13 || valeurEntrée == 10) {
                if (valeurSélection == 4) { InterpréteurCommandes.terminal(false); return; }
                int résultat;
                if (valeurSélection < 2) résultat = CarteMatérielle.lancerProgrammeUtilisateur(valeurSélection == 0 ? 0 : 9);
                else if (valeurSélection == 2) {
                    résultat = InterpréteurCommandes.lancerExemple(10, "Hello.java");
                    if (résultat == 0) résultat = InterpréteurCommandes.lancerExemple(11, "Hello");
                } else résultat = InterpréteurCommandes.lancerExemple(12, "hello.py");
                valeurÉtatValeur = résultat != 0 ? "PROGRAM FAILED" : valeurSélection == 0 ? "C++ FILE OK" : valeurSélection == 1 ? "UDP LOOPBACK OK" : valeurSélection == 2 ? "JAVA OK" : "MICROPYTHON OK";
                écranPeindre(valeurSélection, valeurÉtatValeur);
                EntréeSortieTerminal.écrire("GUI ACTION "); EntréeSortieTerminal.nombre(valeurSélection); EntréeSortieTerminal.écrire(" RESULT "); EntréeSortieTerminal.nombre(résultat); EntréeSortieTerminal.Caractères(10);
            }
        }
        Noyau.Écran();
        EntréeSortieTerminal.écrire("GUI EXIT\n");
    }
}
