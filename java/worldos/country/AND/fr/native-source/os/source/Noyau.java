// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Point d’entrée Java appelé après le véritable démarrage, indépendant d’une JVM et du système hôte. */
public final class Noyau {
    static int valeurTotal(int terminaison) {
        int valeurSomme = 0;
        for (int numéro = 1; numéro <= terminaison; numéro++) valeurSomme += numéro;
        return valeurSomme;
    }

    static boolean Tests() {
        int[] valeurs = new int[4];
        valeurs[2] = valeurTotal(10);
        int valeurNégatif = -7;
        int valeurMinimal = 0x80000000;
        int résultatDivision = -1;
        int numéro = EspaceMémoire.allouerStockage();
        boolean valeurPassage = valeurs[0] == 0 && valeurs[2] == 55 && valeurs.length == 4
            && valeurNégatif / 3 == -2 && valeurNégatif % 3 == -1 && valeurMinimal / résultatDivision == valeurMinimal
            && valeurMinimal % résultatDivision == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && numéro >= 0 && EspaceMémoire.résultatRetourner(numéro) && !EspaceMémoire.résultatRetourner(numéro);
        TerminalTexte.écrire(valeurPassage ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return valeurPassage;
    }

    public static void lancer() {
        TerminalTexte.préparer();
        TerminalTexte.écrire("JKOROS NATIVE JAVA\n");
        TerminalTexte.écrire("Java 기계어 valeurNoyau lancer\n");
        if (Périphérique.marqueurAmorçage() != 0x2badb002) {
            TerminalTexte.écrire("BAD MULTIBOOT MAGIC\n");
            Périphérique.exécutionArrêterMachine();
        }
        if (!Tests()) Périphérique.exécutionArrêterMachine();
        if (EspaceMémoire.tailleMémoireSupérieur() < 15360) {
            TerminalTexte.écrire("At least 16 MiB RAM required\n");
            Périphérique.exécutionArrêterMachine();
        }
        Périphérique.préparerProgrammeUtilisateur();
        TerminalTexte.écrire("USER ELF: ring 3 / paging / int 0x80\n");
        PiloteRéseau.préparer();
        PileRéseau.processusNettoyer();
        SystèmeFichiersMémoire.préparer();
        PersistanceFichiers.préparer();
        InterpréteurCommandes.lancer();
    }
}
