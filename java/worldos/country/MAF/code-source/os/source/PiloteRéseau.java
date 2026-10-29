// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), un tampon d’émission et un anneau de réception de 8 KiB. Utilise l’interrogation plutôt que les interruptions. */
public final class PiloteRéseau {
    static int adresseBaseEntréeSortie = 0;
    static int recevoirPosition = 0, emplacementTransmettre = 0;
    static int[] adressePériphérique = new int[6];
    static int nombreÉlémentsTransmettre = 0, recevoirNombreÉléments = 0, nombreÉlémentsErreur = 0;

    static int lireRéglages(int numéroPériphérique, int position) {
        Périphérique.écrireEntierEntréeSortie(0xcf8, 0x80000000 | (numéroPériphérique << 11) | position);
        return Périphérique.lireEntierEntréeSortie(0xcfc);
    }

    static boolean préparer() {
        int numéroPériphérique = -1;
        for (int numéro = 0; numéro < 32; numéro++) {
            if (lireRéglages(numéro, 0) == 0x813910ec) { numéroPériphérique = numéro; break; }
        }
        if (numéroPériphérique < 0) return false;
        int valeurDéfaut = lireRéglages(numéroPériphérique, 0x10);
        if ((valeurDéfaut & 1) == 0 || (valeurDéfaut & 0xfffffffc) < 0x100 || (valeurDéfaut & 0xfffffffc) > 65535) return false;
        adresseBaseEntréeSortie = valeurDéfaut & 0xfffc;
        int commande = lireRéglages(numéroPériphérique, 4);
        Périphérique.écrireEntierEntréeSortie(0xcf8, 0x80000004 | (numéroPériphérique << 11));
        Périphérique.écrireCourtEntréeSortie(0xcfc, commande | 5); // Activer les entrées-sorties et la maîtrise du bus ; ne pas modifier les bits d’état PCI.
        Périphérique.écrireOctetEntréeSortie(adresseBaseEntréeSortie + 0x52, 0);
        if (!réinitialiserValeur()) { adresseBaseEntréeSortie = 0; return false; }
        for (int numéro = 0; numéro < 6; numéro++) adressePériphérique[numéro] = Périphérique.lireOctetEntréeSortie(adresseBaseEntréeSortie + numéro);
        return true;
    }

    static boolean réinitialiserValeur() {
        Périphérique.écrireOctetEntréeSortie(adresseBaseEntréeSortie + 0x37, 0x10);
        int lancer = Périphérique.millisecondes();
        while ((Périphérique.lireOctetEntréeSortie(adresseBaseEntréeSortie + 0x37) & 0x10) != 0)
            if (Périphérique.millisecondes() - lancer > 100) return false;
        recevoirPosition = 0; emplacementTransmettre = 0;
        Périphérique.écrireEntierEntréeSortie(adresseBaseEntréeSortie + 0x30, Périphérique.mémoireRéseau());
        for (int numéro = 0; numéro < 4; numéro++) Périphérique.écrireEntierEntréeSortie(adresseBaseEntréeSortie + 0x20 + numéro * 4, Périphérique.mémoireRéseau() + 12288);
        Périphérique.écrireCourtEntréeSortie(adresseBaseEntréeSortie + 0x3c, 0);
        Périphérique.écrireCourtEntréeSortie(adresseBaseEntréeSortie + 0x3e, 0xffff);
        Périphérique.écrireOctetEntréeSortie(adresseBaseEntréeSortie + 0x37, 0x0c);
        Périphérique.écrireEntierEntréeSortie(adresseBaseEntréeSortie + 0x44, 0x0000e78a); // Accepter l’adresse propre et les diffusions ; stockage contigu au bouclage, 8 KiB.
        Périphérique.écrireEntierEntréeSortie(adresseBaseEntréeSortie + 0x40, 0x03000600);
        return true;
    }

    static int envoyer(int[] Données, int longueur) {
        if (adresseBaseEntréeSortie == 0) return -19;
        if (longueur < 14 || longueur > 1514) return -90;
        int portÉtat = adresseBaseEntréeSortie + 0x10 + emplacementTransmettre * 4;
        int lancer = Périphérique.millisecondes();
        while ((Périphérique.lireEntierEntréeSortie(portÉtat) & 0x2000) == 0)
            if (Périphérique.millisecondes() - lancer > 100) return -110;
        int taille = longueur < 60 ? 60 : longueur;
        for (int numéro = 0; numéro < taille; numéro++)
            Périphérique.écrireMémoire(Périphérique.mémoireRéseau() + 12288 + numéro, numéro < longueur ? Données[numéro] : 0);
        Périphérique.écrireEntierEntréeSortie(portÉtat, taille | 0x00080000);
        lancer = Périphérique.millisecondes();
        while ((Périphérique.lireEntierEntréeSortie(portÉtat) & 0xe0008000) == 0)
            if (Périphérique.millisecondes() - lancer > 100) return -110;
        if ((Périphérique.lireEntierEntréeSortie(portÉtat) & 0x8000) == 0) { nombreÉlémentsErreur++; return -5; }
        emplacementTransmettre = (emplacementTransmettre + 1) & 3;
        nombreÉlémentsTransmettre++;
        return longueur;
    }

    static int recevoir(int[] Données) {
        if (adresseBaseEntréeSortie == 0) return 0;
        if ((Périphérique.lireOctetEntréeSortie(adresseBaseEntréeSortie + 0x3e) & 0x50) != 0) {
            nombreÉlémentsErreur++;
            if (!réinitialiserValeur()) adresseBaseEntréeSortie = 0;
            return 0;
        }
        if ((Périphérique.lireOctetEntréeSortie(adresseBaseEntréeSortie + 0x37) & 1) != 0) return 0;
        int valeurTête = Périphérique.mémoireRéseau() + recevoirPosition;
        int valeurÉtatValeur = GestionExécution.valeurCourt(valeurTête), taille = GestionExécution.valeurCourt(valeurTête + 2);
        if (taille == 0xfff0) return 0; // Transfert DMA en cours.
        if (taille < 4 || taille > 1518) {
            nombreÉlémentsErreur++;
            if (!réinitialiserValeur()) adresseBaseEntréeSortie = 0;
            return 0;
        }
        int longueur = taille - 4;
        if ((valeurÉtatValeur & 1) != 0) {
            for (int numéro = 0; numéro < longueur; numéro++) Données[numéro] = Périphérique.lireMémoire(valeurTête + 4 + numéro);
            recevoirNombreÉléments++;
        } else { longueur = 0; nombreÉlémentsErreur++; }
        recevoirPosition = (recevoirPosition + taille + 4 + 3) & ~3;
        recevoirPosition &= 8191;
        Périphérique.écrireCourtEntréeSortie(adresseBaseEntréeSortie + 0x38, (recevoirPosition - 16) & 65535);
        Périphérique.écrireCourtEntréeSortie(adresseBaseEntréeSortie + 0x3e, 0x000f);
        return longueur;
    }
}
