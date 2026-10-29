// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Huit fichiers conservés pendant la session. Un échec d’édition ou de compilation préserve les fichiers existants. */
public final class SystèmeFichiersMémoire {
    static final int tailleMaximal = 16384;
    static int[] listeNoms = new int[8 * 64];
    static int[] listeTaille = new int[8];
    static int[] ouvrirNombreÉléments = new int[8], autorisationsPermission = new int[8];
    static int[] nom = new int[64];
    static int[] valeurÉditer = new int[tailleMaximal];
    static boolean estÉditionEnCours = false;
    static boolean valeurDébordement = false;
    static int tailleÉditer = 0;

    static boolean contrôlerNom(int[] valeurCaractère, int longueur) {
        if (longueur < 1 || longueur > 63) return false;
        for (int nombre = 0; nombre < longueur; nombre++) {
            int valeur = valeurCaractère[nombre];
            if (!(valeur >= 'a' && valeur <= 'z') && !(valeur >= 'A' && valeur <= 'Z')
                && !(valeur >= '0' && valeur <= '9') && valeur != '_' && valeur != '-' && valeur != '.') return false;
        }
        return valeurCaractère[0] != '.';
    }

    static int trouverEntréeÉlément(int[] valeurCaractère, int longueur) {
        if (!contrôlerNom(valeurCaractère, longueur)) return -22;
        for (int nombre = 0; nombre < 8; nombre++) {
            boolean texteÉgal = listeNoms[nombre * 64 + longueur] == 0;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) if (listeNoms[nombre * 64 + entréeÉlémentEmplacement] != valeurCaractère[entréeÉlémentEmplacement]) texteÉgal = false;
            if (texteÉgal) return nombre;
        }
        return -2;
    }

    static int valeurStocker(int[] valeurCaractère, int longueur, int[] Données, int taille) {
        if (!contrôlerNom(valeurCaractère, longueur) || taille < 0 || taille > Données.length) return -22;
        if (taille > tailleMaximal) return -90;
        int numéro = trouverEntréeÉlément(valeurCaractère, longueur);
        if (numéro == -2) {
            for (int nombre = 0; nombre < 8 && numéro < 0; nombre++) if (listeNoms[nombre * 64] == 0 && ouvrirNombreÉléments[nombre] == 0) numéro = nombre;
            if (numéro >= 0) autorisationsPermission[numéro] = 438;
        }
        if (numéro < 0) return -28;
        int adresse = Périphérique.mémoireFichier() + numéro * tailleMaximal;
        for (int nombre = 0; nombre < taille; nombre++) Périphérique.écrireMémoire(adresse + nombre, Données[nombre]);
        for (int nombre = 0; nombre < 64; nombre++) listeNoms[numéro * 64 + nombre] = nombre < longueur ? valeurCaractère[nombre] : 0;
        listeTaille[numéro] = taille;
        return taille;
    }

    static void listeEntréeÉlément() {
        for (int nombre = 0; nombre < 8; nombre++) if (listeNoms[nombre * 64] != 0) {
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64 && listeNoms[nombre * 64 + entréeÉlémentEmplacement] != 0; entréeÉlémentEmplacement++) TerminalTexte.Caractères(listeNoms[nombre * 64 + entréeÉlémentEmplacement]);
            TerminalTexte.écrire("  "); TerminalTexte.écrireNuméro(listeTaille[nombre]); TerminalTexte.écrire("valeurOctet\n");
        }
        TerminalTexte.écrire(ConnexionStockage.estDisponible ? "Fichier 8칸, 파일당 16384바이트; sync로 valeurStocker 장치에 보존\n"
            : "valeurTemporaire Fichier 8칸, 파일당 16384바이트; valeurRéessayer 시작하면 사라짐\n");
    }

    static void commande(int[] valeurEntrée, int lancer, int longueur, int action) {
        while (lancer < longueur && valeurEntrée[lancer] == ' ') lancer++;
        int terminaison = longueur;
        while (terminaison > lancer && valeurEntrée[terminaison - 1] == ' ') terminaison--;
        int nombre = terminaison - lancer;
        if (nombre < 1 || nombre > 63) { TerminalTexte.écrire("올바르지 않은 Fichier nom\n"); return; }
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64; entréeÉlémentEmplacement++) nom[entréeÉlémentEmplacement] = entréeÉlémentEmplacement < nombre ? valeurEntrée[lancer + entréeÉlémentEmplacement] : 0;
        int numéro = trouverEntréeÉlément(nom, nombre);
        if (numéro == -22) { TerminalTexte.écrire("올바르지 않은 Fichier nom\n"); return; }
        if (action == 0) {
            estÉditionEnCours = true; tailleÉditer = 0; valeurDébordement = false;
            TerminalTexte.écrire("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (numéro < 0) TerminalTexte.écrire("파일을 찾을 nombre 없습니다\n");
        else if (action == 1) {
            int adresse = Périphérique.mémoireFichier() + numéro * tailleMaximal;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < listeTaille[numéro]; entréeÉlémentEmplacement++) TerminalTexte.Caractères(Périphérique.lireMémoire(adresse + entréeÉlémentEmplacement));
            TerminalTexte.Caractères(10);
        } else { listeNoms[numéro * 64] = 0; listeTaille[numéro] = 0; TerminalTexte.écrire("파일을 지웠습니다\n"); }
    }

    static boolean estExact(int[] valeurEntrée, int longueur, String valeurExpressionPhrase) {
        if (longueur != valeurExpressionPhrase.length()) return false;
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) if (valeurEntrée[entréeÉlémentEmplacement] != valeurExpressionPhrase.charAt(entréeÉlémentEmplacement)) return false;
        return true;
    }

    static void ligneÉdité(int[] valeurEntrée, int longueur, boolean débordementLigne) {
        if (estExact(valeurEntrée, longueur, ".cancel")) {
            estÉditionEnCours = false; TerminalTexte.écrire("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (estExact(valeurEntrée, longueur, ".save")) {
            estÉditionEnCours = false;
            if (valeurDébordement) { TerminalTexte.écrire("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int nombre = 0;
            while (nombre < 64 && nom[nombre] != 0) nombre++;
            int résultat = valeurStocker(nom, nombre, valeurÉditer, tailleÉditer);
            TerminalTexte.écrire(résultat >= 0 ? "보존한 valeurOctet nombre: " : "보존 valeurÉchec: ");
            TerminalTexte.écrireNuméro(résultat); TerminalTexte.Caractères(10);
        } else if (débordementLigne || longueur + 1 > tailleMaximal - tailleÉditer) valeurDébordement = true;
        else {
            for (int nombre = 0; nombre < longueur; nombre++) valeurÉditer[tailleÉditer++] = valeurEntrée[nombre];
            valeurÉditer[tailleÉditer++] = 10;
        }
    }

    static void Exemples(String Fichier, String valeurContenuValeur) {
        for (int nombre = 0; nombre < 64; nombre++) nom[nombre] = nombre < Fichier.length() ? Fichier.charAt(nombre) : 0;
        for (int nombre = 0; nombre < valeurContenuValeur.length(); nombre++) valeurÉditer[nombre] = valeurContenuValeur.charAt(nombre);
        valeurStocker(nom, Fichier.length(), valeurÉditer, valeurContenuValeur.length());
    }

    static void préparer() {
        Exemples("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int valeurGroupe = Périphérique.lotFichierJava(), taille = Périphérique.tailleLotFichierJava();
        if (taille < 8 || GestionExécution.nombre(valeurGroupe) != 0x464a4b4a) { TerminalTexte.écrire("올바르지 않은 Java Fichier valeurGroupe\n"); return; }
        int nombreÉlémentsÉlémentListe = GestionExécution.nombre(valeurGroupe + 4);
        if (nombreÉlémentsÉlémentListe < 0 || nombreÉlémentsÉlémentListe > 8 || nombreÉlémentsÉlémentListe > (taille - 8) / 72) { TerminalTexte.écrire("올바르지 않은 Java Fichier listeEntréeÉlément\n"); return; }
        for (int nombre = 0; nombre < nombreÉlémentsÉlémentListe; nombre++) {
            int valeurEntréeÉlément = valeurGroupe + 8 + nombre * 72, longueur = 0;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64; entréeÉlémentEmplacement++) nom[entréeÉlémentEmplacement] = Périphérique.lireMémoire(valeurEntréeÉlément + entréeÉlémentEmplacement);
            while (longueur < 64 && nom[longueur] != 0) longueur++;
            int position = GestionExécution.nombre(valeurEntréeÉlément + 64), tailleFichier = GestionExécution.nombre(valeurEntréeÉlément + 68);
            if (!contrôlerNom(nom, longueur) || tailleFichier < 0 || tailleFichier > tailleMaximal || position < 8 + nombreÉlémentsÉlémentListe * 72 || position > taille - tailleFichier) {
                TerminalTexte.écrire("올바르지 않은 Java Fichier valeurEntréeÉlément\n"); return;
            }
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < tailleFichier; entréeÉlémentEmplacement++) valeurÉditer[entréeÉlémentEmplacement] = Périphérique.lireMémoire(valeurGroupe + position + entréeÉlémentEmplacement);
            if (valeurStocker(nom, longueur, valeurÉditer, tailleFichier) < 0) { TerminalTexte.écrire("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
