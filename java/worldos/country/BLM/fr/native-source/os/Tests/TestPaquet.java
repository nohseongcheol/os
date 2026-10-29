// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Appelle le véritable gestionnaire de protocole Java dans une JVM pour vérifier rapidement les limites et les entrées corrompues. */
public final class TestPaquet {
    static int nombreÉlémentsRépétition = 0;
    static void vérifier(boolean valeur) { if (!valeur) throw new AssertionError("case " + nombreÉlémentsRépétition); nombreÉlémentsRépétition++; }
    static int sommeContrôle(int[] valeur, int lancer, int longueur, int étatValeurInitialValeur) {
        int valeurSomme = étatValeurInitialValeur;
        for (int numéro = 0; numéro < longueur; numéro++) valeurSomme += valeur[lancer + numéro] << ((numéro & 1) == 0 ? 8 : 0);
        valeurSomme = (valeurSomme & 65535) + (valeurSomme >>> 16);
        valeurSomme = (valeurSomme & 65535) + (valeurSomme >>> 16);
        return ~valeurSomme & 65535;
    }
    static void préparer(int longueur) {
        PileRéseau.processusNettoyer();
        vérifier(PileRéseau.ouvrir(5000) == 3);
        int[] indiceCadre = PileRéseau.cadreEntrée;
        Arrays.fill(indiceCadre, 0);
        for (int numéro = 0; numéro < 6; numéro++) indiceCadre[numéro] = PiloteRéseau.adressePériphérique[numéro];
        PileRéseau.placer16Bits(indiceCadre, 12, 0x0800);
        indiceCadre[14] = 0x45; indiceCadre[22] = 64; indiceCadre[23] = 17;
        PileRéseau.placer16Bits(indiceCadre, 16, 28 + longueur);
        PileRéseau.placer32Bits(indiceCadre, 26, 0x0a000202); PileRéseau.placer32Bits(indiceCadre, 30, PileRéseau.adressePropre);
        PileRéseau.placer16Bits(indiceCadre, 34, 4321); PileRéseau.placer16Bits(indiceCadre, 36, 5000); PileRéseau.placer16Bits(indiceCadre, 38, longueur + 8);
        for (int numéro = 0; numéro < longueur; numéro++) indiceCadre[42 + numéro] = numéro & 255;
        définirSommeContrôle(longueur);
    }
    static void définirSommeContrôle(int longueur) {
        int[] indiceCadre = PileRéseau.cadreEntrée;
        PileRéseau.placer16Bits(indiceCadre, 24, 0); PileRéseau.placer16Bits(indiceCadre, 40, 0);
        PileRéseau.placer16Bits(indiceCadre, 24, sommeContrôle(indiceCadre, 14, 20, 0));
        int étatValeurInitialValeur = PileRéseau.sommeContrôleEntêtePseudo(PileRéseau.entier32(indiceCadre, 26), PileRéseau.adressePropre, longueur + 8);
        int valeurSomme = sommeContrôle(indiceCadre, 34, longueur + 8, étatValeurInitialValeur);
        PileRéseau.placer16Bits(indiceCadre, 40, valeurSomme == 0 ? 65535 : valeurSomme);
    }
    static void rejeterValeur(int longueur) { PileRéseau.cadreProcessus(longueur); vérifier(PileRéseau.longueurReçu[0] == -1); }
    public static void main(String[] arguments) {
        for (int longueur : new int[]{0, 1, 2, 7, 1023, 1024}) {
            préparer(longueur); PileRéseau.cadreProcessus(longueur + 42);
            vérifier(PileRéseau.longueurReçu[0] == longueur);
            vérifier(PileRéseau.adresseReçu[0] == 0x0a000202 && PileRéseau.numéroPortReçu[0] == 4321);
            for (int numéro = 0; numéro < longueur; numéro++) vérifier(PileRéseau.donnéesReçu[numéro] == (numéro & 255));
        }
        for (int longueur = 0; longueur < 42; longueur++) { préparer(0); rejeterValeur(longueur); }
        préparer(1025); rejeterValeur(1067);
        préparer(2); PileRéseau.cadreEntrée[24] ^= 1; rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[42] ^= 1; rejeterValeur(44);
        préparer(2); PileRéseau.placer16Bits(PileRéseau.cadreEntrée, 38, 7); rejeterValeur(44);
        préparer(2); PileRéseau.placer16Bits(PileRéseau.cadreEntrée, 38, 65535); rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[14] = 0x4f; rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[14] = 0x44; rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[20] = 0x20; définirSommeContrôle(2); rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[21] = 1; définirSommeContrôle(2); rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[33] = 99; définirSommeContrôle(2); rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[0] ^= 1; rejeterValeur(44);
        préparer(2); PileRéseau.cadreEntrée[23] = 6; définirSommeContrôle(2); rejeterValeur(44);
        préparer(2); PileRéseau.placer16Bits(PileRéseau.cadreEntrée, 40, 0); PileRéseau.cadreProcessus(44); vérifier(PileRéseau.longueurReçu[0] == 2);
        int[] résultat = new int[4];
        vérifier(PileRéseau.recevoir(3, résultat, 1, 0) == -90);
        vérifier(PileRéseau.recevoir(3, résultat, 4, 0) == -11);
        préparer(2); PileRéseau.cadreProcessus(44); int abandonnerValeur = PileRéseau.nombreÉlémentsAbandonné;
        PileRéseau.cadreProcessus(44); vérifier(PileRéseau.nombreÉlémentsAbandonné == abandonnerValeur + 1);
        PileRéseau.processusNettoyer(); vérifier(PileRéseau.ouvrir(5000) == 3);
        vérifier(PileRéseau.ouvrir(5000) == -98); vérifier(PileRéseau.ouvrir(0) == 4);
        vérifier(PileRéseau.ouvrir(0) == 5); vérifier(PileRéseau.ouvrir(0) == 6); vérifier(PileRéseau.ouvrir(0) == -24);
        vérifier(PileRéseau.fermer(4) == 0); vérifier(PileRéseau.fermer(4) == -9);
        PileRéseau.adresseTrouvé = PileRéseau.valeurPasserelle;
        vérifier(PileRéseau.envoyer(3, PileRéseau.valeurPasserelle, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] possèdeEnvoyé = PiloteRéseau.valeurRécent;
        vérifier(sommeContrôle(possèdeEnvoyé, 14, 20, 0) == 0);
        vérifier(sommeContrôle(possèdeEnvoyé, 34, 11, PileRéseau.sommeContrôleEntêtePseudo(PileRéseau.adressePropre, PileRéseau.valeurPasserelle, 11)) == 0);
        vérifier(possèdeEnvoyé[42] == 1 && possèdeEnvoyé[44] == 3);
        System.out.println("PACKET TEST PASS: " + nombreÉlémentsRépétition + " assertions");
    }
}
