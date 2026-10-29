// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Petit format de stockage dédié avec sommes de contrôle et deux copies. Persistance uniquement lors de fsync/sync. */
public final class PersistanceFichiers {
    static int copierPréservéActuel = -1, numéroGénération = 0;
    static int[] tableFichier = new int[1024];
    static int octetsHachage(int valeur, int Données) { return (valeur ^ Données) * 16777619; }
    static void effacerContenuDonnées() {
        for (int numéro = 0; numéro < 512; numéro++) ConnexionStockage.donnéesSection[numéro] = 0;
    }
    static int entierTable(int position) {
        return tableFichier[position] | tableFichier[position + 1] << 8 | tableFichier[position + 2] << 16 | tableFichier[position + 3] << 24;
    }
    static void écrireEntierTable(int position, int valeur) {
        for (int numéro = 0; numéro < 4; numéro++) tableFichier[position + numéro] = (valeur >>> (numéro * 8)) & 255;
    }
    static boolean contrôlerTable() {
        for (int Fichier = 0; Fichier < 8; Fichier++) {
            int longueur = 0;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64; entréeÉlémentEmplacement++) SystèmeFichiersMémoire.nom[entréeÉlémentEmplacement] = tableFichier[Fichier * 72 + entréeÉlémentEmplacement];
            while (longueur < 64 && SystèmeFichiersMémoire.nom[longueur] != 0) longueur++;
            if (longueur == 0) continue;
            if (!SystèmeFichiersMémoire.contrôlerNom(SystèmeFichiersMémoire.nom, longueur)
                || entierTable(Fichier * 72 + 64) < 0 || entierTable(Fichier * 72 + 64) > 16384) return false;
            for (int valeurAvantCôté = 0; valeurAvantCôté < Fichier; valeurAvantCôté++) {
                boolean texteÉgal = tableFichier[valeurAvantCôté * 72 + longueur] == 0;
                for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < longueur; entréeÉlémentEmplacement++) if (tableFichier[valeurAvantCôté * 72 + entréeÉlémentEmplacement] != SystèmeFichiersMémoire.nom[entréeÉlémentEmplacement]) texteÉgal = false;
                if (texteÉgal) return false;
            }
        }
        return true;
    }
    static int contrôlerCopierPréservé(int copierPréservé) {
        int démarrerSection = 1 + copierPréservé * 259;
        if (ConnexionStockage.lire(démarrerSection) < 0 || ConnexionStockage.analyserEntier(0) != 0x4a4b534e) return -1;
        int valeurGénération = ConnexionStockage.analyserEntier(4), sommeContrôle = ConnexionStockage.analyserEntier(8);
        if (valeurGénération < 1 || ConnexionStockage.analyserEntier(12) != (valeurGénération ^ sommeContrôle ^ 0x4a4b534e)) return -1;
        int fichierHachage = 0x811c9dc5;
        for (int valeurSection = 0; valeurSection < 258; valeurSection++) {
            if (ConnexionStockage.lire(démarrerSection + 1 + valeurSection) < 0) return -1;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 512; entréeÉlémentEmplacement++) {
                int valeur = ConnexionStockage.donnéesSection[entréeÉlémentEmplacement];
                fichierHachage = octetsHachage(fichierHachage, valeur);
                if (valeurSection < 2) tableFichier[valeurSection * 512 + entréeÉlémentEmplacement] = valeur;
            }
        }
        return fichierHachage == sommeContrôle && contrôlerTable() ? valeurGénération : -1;
    }
    static int charger(int copierPréservé) {
        int démarrerSection = 1 + copierPréservé * 259;
        for (int valeurSection = 0; valeurSection < 2; valeurSection++) {
            if (ConnexionStockage.lire(démarrerSection + 1 + valeurSection) < 0) return -5;
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 512; entréeÉlémentEmplacement++) tableFichier[valeurSection * 512 + entréeÉlémentEmplacement] = ConnexionStockage.donnéesSection[entréeÉlémentEmplacement];
        }
        for (int Fichier = 0; Fichier < 8; Fichier++) {
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64; entréeÉlémentEmplacement++) SystèmeFichiersMémoire.listeNoms[Fichier * 64 + entréeÉlémentEmplacement] = tableFichier[Fichier * 72 + entréeÉlémentEmplacement];
            SystèmeFichiersMémoire.listeTaille[Fichier] = tableFichier[Fichier * 72] == 0 ? 0 : entierTable(Fichier * 72 + 64);
            SystèmeFichiersMémoire.autorisationsPermission[Fichier] = entierTable(Fichier * 72 + 68) & 511;
            for (int valeurSection = 0; valeurSection < 32; valeurSection++) {
                if (ConnexionStockage.lire(démarrerSection + 3 + Fichier * 32 + valeurSection) < 0) return -5;
                int adresse = Périphérique.mémoireFichier() + Fichier * 16384 + valeurSection * 512;
                for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 512; entréeÉlémentEmplacement++) Périphérique.écrireMémoire(adresse + entréeÉlémentEmplacement, ConnexionStockage.donnéesSection[entréeÉlémentEmplacement]);
            }
        }
        return 0;
    }
    static void préparer() {
        if (ConnexionStockage.lire(0) < 0 || ConnexionStockage.analyserEntier(0) != 0x54534b4a
            || ConnexionStockage.analyserEntier(4) != 0x3145524f || ConnexionStockage.analyserEntier(8) != 2048
            || ConnexionStockage.analyserEntier(12) != 0x3153464a) {
            TerminalTexte.écrire("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        ConnexionStockage.estDisponible = true;
        int ordinalPremier = contrôlerCopierPréservé(0), ordinalDeuxième = contrôlerCopierPréservé(1);
        if (ordinalPremier < 0 && ordinalDeuxième < 0) { TerminalTexte.écrire("STORE ready; no valid snapshot\n"); return; }
        copierPréservéActuel = ordinalPremier >= ordinalDeuxième ? 0 : 1; numéroGénération = ordinalPremier >= ordinalDeuxième ? ordinalPremier : ordinalDeuxième;
        if (charger(copierPréservéActuel) < 0) {
            TerminalTexte.écrire("STORE read failed; halted to preserve files\n"); Périphérique.exécutionArrêterMachine();
        }
        TerminalTexte.écrire("STORE restored generation "); TerminalTexte.écrireNuméro(numéroGénération); TerminalTexte.Caractères(10);
    }
    static int synchroniser() {
        if (!ConnexionStockage.estDisponible) return -19;
        if (numéroGénération == 2147483647) return -75;
        int élémentListeSuivant = copierPréservéActuel == 0 ? 1 : 0, démarrerSection = 1 + élémentListeSuivant * 259;
        // Invalider l’ancien commit et vider le cache du périphérique avant d’écrire le nouveau contenu.
        effacerContenuDonnées();
        if (ConnexionStockage.écrire(démarrerSection) < 0 || ConnexionStockage.sortieViderTampon() < 0) return -5;
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 1024; entréeÉlémentEmplacement++) tableFichier[entréeÉlémentEmplacement] = 0;
        for (int Fichier = 0; Fichier < 8; Fichier++) if (SystèmeFichiersMémoire.listeNoms[Fichier * 64] != 0) {
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 64; entréeÉlémentEmplacement++) tableFichier[Fichier * 72 + entréeÉlémentEmplacement] = SystèmeFichiersMémoire.listeNoms[Fichier * 64 + entréeÉlémentEmplacement];
            écrireEntierTable(Fichier * 72 + 64, SystèmeFichiersMémoire.listeTaille[Fichier]);
            écrireEntierTable(Fichier * 72 + 68, SystèmeFichiersMémoire.autorisationsPermission[Fichier]);
        }
        int fichierHachage = 0x811c9dc5;
        for (int valeurSection = 0; valeurSection < 258; valeurSection++) {
            for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 512; entréeÉlémentEmplacement++) {
                int valeur = 0;
                if (valeurSection < 2) valeur = tableFichier[valeurSection * 512 + entréeÉlémentEmplacement];
                else {
                    int Fichier = (valeurSection - 2) / 32, position = (valeurSection - 2) % 32 * 512 + entréeÉlémentEmplacement;
                    if (tableFichier[Fichier * 72] != 0 && position < SystèmeFichiersMémoire.listeTaille[Fichier])
                        valeur = Périphérique.lireMémoire(Périphérique.mémoireFichier() + Fichier * 16384 + position);
                }
                ConnexionStockage.donnéesSection[entréeÉlémentEmplacement] = valeur; fichierHachage = octetsHachage(fichierHachage, valeur);
            }
            if (ConnexionStockage.écrire(démarrerSection + 1 + valeurSection) < 0) return -5;
        }
        if (ConnexionStockage.sortieViderTampon() < 0) return -5;
        effacerContenuDonnées(); ConnexionStockage.écrireValeurEntier(0, 0x4a4b534e);
        ConnexionStockage.écrireValeurEntier(4, numéroGénération + 1); ConnexionStockage.écrireValeurEntier(8, fichierHachage);
        ConnexionStockage.écrireValeurEntier(12, (numéroGénération + 1) ^ fichierHachage ^ 0x4a4b534e);
        if (ConnexionStockage.écrire(démarrerSection) < 0 || ConnexionStockage.sortieViderTampon() < 0) return -5;
        copierPréservéActuel = élémentListeSuivant; numéroGénération++;
        return 0;
    }
}
