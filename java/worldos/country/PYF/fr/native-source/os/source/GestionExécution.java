// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Vérifie ELF32 dans les paquets exécutables en lecture seule, transmet les arguments et exécute un processus utilisateur à la fois. */
public final class GestionExécution {
    static final int démarrerProgrammeUtilisateur = 0x04000000;
    static final int finUtilisateur = 0x04400000;
    static final int adresseFinImage = 0x04200000;
    static final int démarrerArgument = 0x04300000;
    static int nombreÉlémentsArgument = 0;
    static int[] adresseArgument = new int[16];

    static boolean rogner(int adresse, int longueur) {
        return adresse >= démarrerProgrammeUtilisateur && adresse < finUtilisateur && longueur >= 0 && longueur <= finUtilisateur - adresse;
    }

    static int nombre(int adresse) { return EspaceMémoire.analyserEntier(adresse); }
    static int valeurCourt(int adresse) { return Périphérique.lireMémoire(adresse) | Périphérique.lireMémoire(adresse + 1) << 8; }
    static void écrireNuméro(int adresse, int valeur) {
        for (int numéro = 0; numéro < 4; numéro++) Périphérique.écrireMémoire(adresse + numéro, valeur >>> (numéro * 8));
    }

    static int nombreÉlémentsGroupe() {
        int adresse = Périphérique.LotCodeExécutable();
        int taille = Périphérique.tailleLotCodeExécutable();
        if (taille < 8 || nombre(adresse) != 0x50414b4a) return 0;
        int nombreÉlémentsÉlémentListe = nombre(adresse + 4);
        return nombreÉlémentsÉlémentListe >= 0 && nombreÉlémentsÉlémentListe <= 32 && nombreÉlémentsÉlémentListe <= (taille - 8) / 24 ? nombreÉlémentsÉlémentListe : 0;
    }

    static void listeEntréeÉlément() {
        for (int numéro = 0; numéro < nombreÉlémentsGroupe(); numéro++) {
            int valeurEntréeÉlément = Périphérique.LotCodeExécutable() + 8 + numéro * 24;
            for (int valeurCaractère = 0; valeurCaractère < 16 && Périphérique.lireMémoire(valeurEntréeÉlément + valeurCaractère) != 0; valeurCaractère++)
                TerminalTexte.Caractères(Périphérique.lireMémoire(valeurEntréeÉlément + valeurCaractère));
            TerminalTexte.écrire("\n");
        }
    }

    static int trouverEntréeÉlément(int[] valeurEntrée, int lancer, int longueur) {
        if (longueur <= 0 || longueur >= 16) return 0;
        for (int numéro = 0; numéro < nombreÉlémentsGroupe(); numéro++) {
            int valeurEntréeÉlément = Périphérique.LotCodeExécutable() + 8 + numéro * 24;
            boolean texteÉgal = Périphérique.lireMémoire(valeurEntréeÉlément + longueur) == 0;
            for (int valeurCaractère = 0; valeurCaractère < longueur; valeurCaractère++)
                if (valeurEntrée[lancer + valeurCaractère] != Périphérique.lireMémoire(valeurEntréeÉlément + valeurCaractère)) texteÉgal = false;
            if (texteÉgal) return valeurEntréeÉlément;
        }
        return 0;
    }

    static int valider(int Fichier, int longueur) {
        if (longueur < 52 || nombre(Fichier) != 0x464c457f || Périphérique.lireMémoire(Fichier + 4) != 1
            || Périphérique.lireMémoire(Fichier + 5) != 1 || Périphérique.lireMémoire(Fichier + 6) != 1
            || valeurCourt(Fichier + 16) != 2 || valeurCourt(Fichier + 18) != 3 || nombre(Fichier + 20) != 1
            || valeurCourt(Fichier + 40) != 52 || valeurCourt(Fichier + 42) != 32) return -8;
        int valeurPointEntréeÉlément = nombre(Fichier + 24);
        int positionTable = nombre(Fichier + 28);
        int nombreÉlémentsÉlémentListe = valeurCourt(Fichier + 44);
        if (nombreÉlémentsÉlémentListe == 0 || nombreÉlémentsÉlémentListe > 16 || positionTable < 52 || positionTable > longueur - nombreÉlémentsÉlémentListe * 32) return -8;
        boolean estCodeExécutable = false;
        for (int numéro = 0; numéro < nombreÉlémentsÉlémentListe; numéro++) {
            int Table = Fichier + positionTable + numéro * 32;
            int valeurGenre = nombre(Table);
            if (valeurGenre == 2 || valeurGenre == 3) return -8; // Pas de liaison dynamique ni d’interpréteur.
            if (valeurGenre != 1) continue;
            int position = nombre(Table + 4), adresse = nombre(Table + 8), tailleFichier = nombre(Table + 16), tailleMémoire = nombre(Table + 20);
            int valeurAligner = nombre(Table + 28);
            if (adresse < démarrerProgrammeUtilisateur || adresse >= adresseFinImage || tailleMémoire < 0 || tailleMémoire > adresseFinImage - adresse
                || tailleFichier < 0 || tailleFichier > tailleMémoire || position < 0 || (tailleFichier > 0 && position > longueur - tailleFichier)
                || (valeurAligner != 0 && (valeurAligner < 0 || (valeurAligner & (valeurAligner - 1)) != 0
                    || ((adresse - position) & (valeurAligner - 1)) != 0))) return -8;
            for (int valeurAvantCôté = 0; valeurAvantCôté < numéro; valeurAvantCôté++) {
                int élémentListePrécédentÉlément = Fichier + positionTable + valeurAvantCôté * 32;
                if (nombre(élémentListePrécédentÉlément) == 1 && tailleMémoire > 0 && nombre(élémentListePrécédentÉlément + 20) > 0
                    && adresse < nombre(élémentListePrécédentÉlément + 8) + nombre(élémentListePrécédentÉlément + 20) && nombre(élémentListePrécédentÉlément + 8) < adresse + tailleMémoire) return -8;
            }
            if ((nombre(Table + 24) & 1) != 0 && valeurPointEntréeÉlément >= adresse && valeurPointEntréeÉlément - adresse < tailleFichier) estCodeExécutable = true;
        }
        return estCodeExécutable ? valeurPointEntréeÉlément : -8;
    }

    static int exécuterCommande(int[] valeurEntrée, int lancer, int longueur) {
        while (lancer < longueur && valeurEntrée[lancer] == ' ') lancer++;
        int terminaison = lancer;
        while (terminaison < longueur && valeurEntrée[terminaison] != ' ') terminaison++;
        int valeurEntréeÉlément = trouverEntréeÉlément(valeurEntrée, lancer, terminaison - lancer);
        if (valeurEntréeÉlément == 0) return -2;
        int position = nombre(valeurEntréeÉlément + 16), taille = nombre(valeurEntréeÉlément + 20);
        if (position < 8 + nombreÉlémentsGroupe() * 24 || taille < 52 || position > Périphérique.tailleLotCodeExécutable() - taille) return -8;
        int Fichier = Périphérique.LotCodeExécutable() + position;
        int valeurPointEntréeÉlément = valider(Fichier, taille);
        if (valeurPointEntréeÉlément < 0) return valeurPointEntréeÉlément;
        Périphérique.contenuEffacerContenuUtilisateur();
        int positionTable = nombre(Fichier + 28), nombreÉlémentsÉlémentListe = valeurCourt(Fichier + 44);
        for (int numéro = 0; numéro < nombreÉlémentsÉlémentListe; numéro++) {
            int Table = Fichier + positionTable + numéro * 32;
            if (nombre(Table) != 1) continue;
            int original = Fichier + nombre(Table + 4), valeurDestination = nombre(Table + 8), tailleFichier = nombre(Table + 16);
            for (int valeurOctet = 0; valeurOctet < tailleFichier; valeurOctet++) Périphérique.écrireMémoire(valeurDestination + valeurOctet, Périphérique.lireMémoire(original + valeurOctet));
        }
        nombreÉlémentsArgument = 0;
        int valeurStocker = démarrerArgument;
        while (terminaison < longueur) {
            while (terminaison < longueur && valeurEntrée[terminaison] == ' ') terminaison++;
            if (terminaison == longueur) break;
            if (nombreÉlémentsArgument == adresseArgument.length) return -22;
            lancer = terminaison;
            while (terminaison < longueur && valeurEntrée[terminaison] != ' ') terminaison++;
            adresseArgument[nombreÉlémentsArgument++] = valeurStocker;
            écrireNuméro(valeurStocker, terminaison - lancer);
            for (int valeurCaractère = lancer; valeurCaractère < terminaison; valeurCaractère++) écrireNuméro(valeurStocker + 4 + (valeurCaractère - lancer) * 4, valeurEntrée[valeurCaractère]);
            valeurStocker += 4 + (terminaison - lancer) * 4;
        }
        PileRéseau.processusNettoyer();
        GestionDescripteursFichier.démarrerProcessus();
        int résultat = Périphérique.lancerProgrammeUtilisateur(valeurPointEntréeÉlément, finUtilisateur - 16);
        GestionDescripteursFichier.processusNettoyer();
        PileRéseau.processusNettoyer();
        return résultat;
    }
}
