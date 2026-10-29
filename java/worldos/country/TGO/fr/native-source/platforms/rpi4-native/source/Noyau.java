// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Premier portage Pi4 du noyau Java autonome, exécuté directement, sans Linux ni JVM hôte. */
public final class Noyau {
    static int[] nombreItérationsTâche = new int[3];
    static int[] sommeTâche = new int[3];
    static int ordreTâche;
    static int erreurTâche;
    static int graineAléatoire = 17;

    static void vérifier(boolean condition, int numéro) {
        if (!condition) { EntréeSortieTerminal.écrire("FAIL "); EntréeSortieTerminal.nombre(numéro); CarteMatérielle.arrêter(numéro); }
    }
    static int branche(int valeur) {
        switch (valeur) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int commuterDense(int valeur) {
        switch (valeur) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] tableauRetourner(int[] valeurTableau) { return valeurTableau; }
    static void testArithmétique() {
        int valeur = graineAléatoire;
        vérifier(valeur * 7 - valeur == 102 && valeur / 3 == 5 && valeur % 3 == 2, 1);
        int entierMinimal = 0x80000000, unNégatif = -1;
        vérifier(entierMinimal / unNégatif == entierMinimal && entierMinimal % unNégatif == 0, 2);
        vérifier(entierMinimal + entierMinimal == 0 && -entierMinimal == entierMinimal, 3);
        vérifier((-valeur >> 2) == -5 && (-valeur >>> 2) == 1073741819 && (valeur << 33) == 34, 4);
        vérifier((byte)(valeur * 16) == 16 && (short)65535 == -1 && (char)unNégatif == 65535, 5);
        int[] valeurTableau = new int[5];
        for (int indiceBoucle = 0; indiceBoucle < valeurTableau.length; indiceBoucle++) valeurTableau[indiceBoucle] = indiceBoucle * valeur;
        valeurTableau[2]++;
        vérifier(tableauRetourner(valeurTableau) == valeurTableau && valeurTableau[2] == 35 && valeurTableau[4] == 68, 6);
        vérifier(branche(valeur - 117) == 7 && branche(valeur - 15) == 9 && branche(valeur) == 3 && commuterDense(valeur - 15) == 17, 7);
        String texte = "한글 😀";
        vérifier(texte.length() == 5 && texte.charAt(0) == '한' && texte.charAt(3) == 0xd83d, 8);
        vérifier(CarteMatérielle.niveauPrivilègeCPU() == 1, 9);
        EntréeSortieTerminal.écrire("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void Tâche(int numéro) {
        // Vérifier la conservation des variables locales avant et après une cession d’exécution ; chaque tâche possède sa propre pile machine.
        int valeurLocal = numéro * 100;
        for (int indiceBoucle = 0; indiceBoucle < 10; indiceBoucle++) {
            if (ordreTâche % 2 + 1 != numéro) erreurTâche++;
            ordreTâche++;
            valeurLocal += indiceBoucle + numéro;
            sommeTâche[numéro] = valeurLocal;
            nombreItérationsTâche[numéro]++;
            CarteMatérielle.céderProcesseur();
            if (valeurLocal != sommeTâche[numéro]) erreurTâche++;
        }
    }
    static void testTâches() {
        ordreTâche = 0; erreurTâche = 0;
        nombreItérationsTâche[1] = 0; nombreItérationsTâche[2] = 0;
        vérifier(CarteMatérielle.créerTâche(1) == 0 && CarteMatérielle.créerTâche(2) == 0, 20);
        int nombreÉlémentsRotation = 0;
        while (CarteMatérielle.étatValeurTâche(1) != 0 || CarteMatérielle.étatValeurTâche(2) != 0) {
            CarteMatérielle.céderProcesseur();
            vérifier(++nombreÉlémentsRotation < 100, 21);
        }
        vérifier(nombreItérationsTâche[1] == 10 && nombreItérationsTâche[2] == 10 && ordreTâche == 20 && erreurTâche == 0, 22);
        vérifier(sommeTâche[1] == 155 && sommeTâche[2] == 265, 23);
        EntréeSortieTerminal.écrire("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rectangle(int positionHorizontal, int positionVertical, int valeurLargeur, int valeurHauteur, int valeurCouleur) {
        for (int coordonnéeCoordonnéeVerticale = positionVertical; coordonnéeCoordonnéeVerticale < positionVertical + valeurHauteur; coordonnéeCoordonnéeVerticale++)
            for (int coordonnéeCoordonnéeHorizontale = positionHorizontal; coordonnéeCoordonnéeHorizontale < positionHorizontal + valeurLargeur; coordonnéeCoordonnéeHorizontale++) CarteMatérielle.placerPixelÉcran(coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, valeurCouleur);
    }
    static void Écran() {
        if (CarteMatérielle.préparerÉcran() == 0) { EntréeSortieTerminal.écrire("FRAMEBUFFER unavailable\n"); return; }
        rectangle(0, 0, CarteMatérielle.largeurÉcran(), CarteMatérielle.hauteurÉcran(), 0x302018);
        rectangle(40, 40, 560, 400, 0xefe8e2);
        rectangle(40, 40, 560, 40, 0x905020);
        rectangle(60, 110, 240, 140, 0x90b050);
        rectangle(320, 110, 260, 140, 0xd0a040);
        rectangle(60, 290, 520, 120, 0xd8d0c8);
        EntréeSortieTerminal.écrire("FRAMEBUFFER PASS "); EntréeSortieTerminal.nombre(CarteMatérielle.largeurÉcran()); EntréeSortieTerminal.Caractères('x');
        EntréeSortieTerminal.nombre(CarteMatérielle.hauteurÉcran()); EntréeSortieTerminal.écrire(" RGB32 (drawing only)\n");
    }
    static void testC() {
        int résultat = CarteMatérielle.testCpp();
        vérifier(résultat == 0, 100 + résultat);
        EntréeSortieTerminal.écrire("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void testProgrammesUtilisateur() {
        vérifier(CarteMatérielle.contrôlerProgrammeUtilisateur() == 0, 200);
        EntréeSortieTerminal.écrire("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int résultatInitialValeur = CarteMatérielle.lancerProgrammeUtilisateur(0);
        if (résultatInitialValeur != 0) { EntréeSortieTerminal.écrire("USER DEMO RESULT "); EntréeSortieTerminal.nombre(résultatInitialValeur); EntréeSortieTerminal.Caractères(10); }
        vérifier(résultatInitialValeur == 0, 201);
        EntréeSortieTerminal.écrire("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] valeursAttendu = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int numéro = 0; numéro < valeursAttendu.length; numéro++) {
            EntréeSortieTerminal.écrire("USER CHECK "); EntréeSortieTerminal.nombre(numéro); EntréeSortieTerminal.Caractères(10);
            int résultat = CarteMatérielle.lancerProgrammeUtilisateur(numéro + 1);
            if (résultat != valeursAttendu[numéro]) { EntréeSortieTerminal.écrire("USER RESULT "); EntréeSortieTerminal.nombre(résultat); EntréeSortieTerminal.Caractères(10); }
            vérifier(résultat == valeursAttendu[numéro], 210 + numéro);
        }
        vérifier(CarteMatérielle.lancerProgrammeUtilisateur(0) == 0, 220);
        EntréeSortieTerminal.écrire("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void testMiseEnRéseau() {
        int résultat = CarteMatérielle.lancerProgrammeUtilisateur(9);
        if (résultat != 0) { EntréeSortieTerminal.écrire("UDP RESULT "); EntréeSortieTerminal.nombre(résultat); EntréeSortieTerminal.Caractères(10); }
        vérifier(résultat == 0, 230);
    }
    static void informationSystème() {
        EntréeSortieTerminal.écrire("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        EntréeSortieTerminal.écrire("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        EntréeSortieTerminal.écrire("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        EntréeSortieTerminal.écrire("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        EntréeSortieTerminal.écrire("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void lancer() {
        EntréeSortieTerminal.écrire("WorldOS fr · Bonjour · 😀\n");
        testArithmétique();
        testC();
        testTâches();
        Écran();
        testProgrammesUtilisateur();
        testMiseEnRéseau();
        EntréeSortieTerminal.écrire("NATIVE READY\n");
        InterpréteurCommandes.exécuterCommande();
    }
}
