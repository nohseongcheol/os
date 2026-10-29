// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Petit interpréteur de commandes série/PS2 n’écrivant pas sur disque. */
public final class InterpréteurCommandes {
    static int[] valeurEntrée = new int[128];
    static int longueur = 0;
    static boolean lignePrécédentÉlémentVersRetourner = false;
    static boolean débordementLigne = false;

    static boolean commande(String nom) {
        if (longueur < nom.length()) return false;
        for (int numéro = 0; numéro < nom.length(); numéro++)
            if (valeurEntrée[numéro] != nom.charAt(numéro)) return false;
        return longueur == nom.length() || valeurEntrée[nom.length()] == ' ';
    }

    static void afficherAide() {
        TerminalTexte.écrire("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        TerminalTexte.écrire("apps | run NAME [ARGS] | net\n");
        TerminalTexte.écrire("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        TerminalTexte.écrire("sync (연결된 JKSTORE1 valeurStocker 장치에 Fichier 보존)\n");
    }

    static void entréeÉlémentValeurProcessus() {
        if (longueur == 0) return;
        if (commande("help")) afficherAide();
        else if (commande("sync")) {
            int résultat = PersistanceFichiers.synchroniser();
            TerminalTexte.écrire("Sync: "); TerminalTexte.écrireNuméro(résultat); TerminalTexte.Caractères(10);
        }
        else if (commande("ls")) SystèmeFichiersMémoire.listeEntréeÉlément();
        else if (commande("edit")) SystèmeFichiersMémoire.commande(valeurEntrée, 4, longueur, 0);
        else if (commande("cat")) SystèmeFichiersMémoire.commande(valeurEntrée, 3, longueur, 1);
        else if (commande("rm")) SystèmeFichiersMémoire.commande(valeurEntrée, 2, longueur, 2);
        else if (commande("java") || commande("javac")) {
            int résultat = GestionExécution.exécuterCommande(valeurEntrée, 0, longueur);
            TerminalTexte.écrire("Exit: "); TerminalTexte.écrireNuméro(résultat); TerminalTexte.Caractères(10);
        }
        else if (commande("apps")) GestionExécution.listeEntréeÉlément();
        else if (commande("net")) PileRéseau.valeurÉtatValeur();
        else if (commande("run")) {
            int résultat = GestionExécution.exécuterCommande(valeurEntrée, 3, longueur);
            TerminalTexte.écrire("Exit: "); TerminalTexte.écrireNuméro(résultat); TerminalTexte.écrire("\n");
        } else if (commande("info")) {
            TerminalTexte.écrire("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (commande("mem")) {
            TerminalTexte.écrire("côtéSupérieur Mémoire régionAdresse(KiB): "); TerminalTexte.écrireNuméro(EspaceMémoire.tailleMémoireSupérieur());
            TerminalTexte.écrire("\n배열 동적 Mémoire régionAdresse(valeurOctet): "); TerminalTexte.écrireNuméro(Périphérique.utilisationTableau());
            TerminalTexte.écrire(" / 262144\n작업 régionAdresse valeurSection: "); TerminalTexte.écrireNuméro(EspaceMémoire.nombreÉlémentsEntréeÉlémentUtilisé());
            TerminalTexte.écrire(" / 8 (각 4096바이트)\n");
        } else if (commande("alloc")) {
            int numéro = EspaceMémoire.allouerStockage();
            TerminalTexte.écrire("valeurSection numéro: "); TerminalTexte.écrireNuméro(numéro); TerminalTexte.écrire("\n");
        } else if (commande("free")) {
            if (longueur == 6 && valeurEntrée[4] == ' ' && valeurEntrée[5] >= '0' && valeurEntrée[5] <= '7') {
                TerminalTexte.écrire(EspaceMémoire.résultatRetourner(valeurEntrée[5] - '0') ? "반환됨\n" : "할당되지 않은 valeurSection\n");
            } else TerminalTexte.écrire("사용법: free 0..7\n");
        } else if (commande("echo")) {
            for (int numéro = 5; numéro < longueur; numéro++) TerminalTexte.Caractères(valeurEntrée[numéro]);
            TerminalTexte.Caractères(10);
        } else if (commande("clear")) TerminalTexte.effacerEntréeÉlément();
        else if (commande("test")) Noyau.Tests();
        else if (commande("halt")) {
            TerminalTexte.écrire("HALTED\n");
            Périphérique.exécutionArrêterMachine();
        } else TerminalTexte.écrire("알 nombre 없는 명령입니다. help를 입력하세요.\n");
    }

    static void accepterÉcrireEt(int valeur) {
        if (valeur == 10 && lignePrécédentÉlémentVersRetourner) { lignePrécédentÉlémentVersRetourner = false; return; }
        lignePrécédentÉlémentVersRetourner = valeur == 13;
        if (valeur == 10 || valeur == 13) {
            TerminalTexte.Caractères(10);
            if (SystèmeFichiersMémoire.estÉditionEnCours) SystèmeFichiersMémoire.ligneÉdité(valeurEntrée, longueur, débordementLigne);
            else entréeÉlémentValeurProcessus();
            longueur = 0;
            débordementLigne = false;
            TerminalTexte.écrire(SystèmeFichiersMémoire.estÉditionEnCours ? "...> " : "jkoros> ");
        } else if (valeur == 8 || valeur == 127) {
            if (longueur > 0) {
                longueur--;
                TerminalTexte.octetSériel(8); TerminalTexte.octetSériel(32); TerminalTexte.octetSériel(8);
                TerminalTexte.caractèreÉcran(8);
            }
        } else if (valeur >= 32 && valeur < 127 && longueur < valeurEntrée.length) {
            valeurEntrée[longueur++] = valeur;
            TerminalTexte.Caractères(valeur);
        } else if (valeur >= 32 && valeur < 127) débordementLigne = true;
    }

    static void lancer() {
        afficherAide();
        TerminalTexte.écrire("READY\njkoros> ");
        while (true) {
            int valeur = TerminalTexte.lireSériel();
            if (valeur < 0) valeur = Clavier.lire();
            if (valeur >= 0) accepterÉcrireEt(valeur);
            else { PileRéseau.vérifier(); Périphérique.céderBrièvement(); }
        }
    }
}
