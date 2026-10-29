// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** IPv4/ARP/UDP statiques. Au plus quatre ports de communication, avec un datagramme par port. */
public final class PileRéseau {
    static final int adressePropre = 0xc0a80064; /* ip.conf:IP */
    static final int masqueRéseau = 0xffffff00; /* ip.conf:NETMASK */
    static final int valeurPasserelle = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] cadreEntrée = new int[1536], cadreSortie = new int[1536];
    static int[] ports = new int[4], longueurReçu = new int[4], adresseReçu = new int[4], numéroPortReçu = new int[4];
    static int[] donnéesReçu = new int[4096], périphériqueTrouvé = new int[6];
    static int trouverVersAdresse = 0, adresseTrouvé = 0, valeurIdentificateur = 0, nombreÉlémentsAbandonné = 0;

    static int entier16(int[] indiceCadre, int position) { return (indiceCadre[position] << 8) | indiceCadre[position + 1]; }
    static int entier32(int[] indiceCadre, int position) { return (entier16(indiceCadre, position) << 16) | entier16(indiceCadre, position + 2); }
    static void placer16Bits(int[] indiceCadre, int position, int valeur) { indiceCadre[position] = (valeur >>> 8) & 255; indiceCadre[position + 1] = valeur & 255; }
    static void placer32Bits(int[] indiceCadre, int position, int valeur) { placer16Bits(indiceCadre, position, valeur >>> 16); placer16Bits(indiceCadre, position + 2, valeur); }
    static int valeurSomme(int[] indiceCadre, int lancer, int longueur, int valeur) {
        for (int numéro = 0; numéro < longueur; numéro += 2)
            valeur += (indiceCadre[lancer + numéro] << 8) | (numéro + 1 < longueur ? indiceCadre[lancer + numéro + 1] : 0);
        while ((valeur >>> 16) != 0) valeur = (valeur & 65535) + (valeur >>> 16);
        return valeur;
    }
    static int sommeContrôleEntêtePseudo(int valeurDépart, int valeurArrivée, int longueur) {
        return (valeurDépart >>> 16) + (valeurDépart & 65535) + (valeurArrivée >>> 16) + (valeurArrivée & 65535) + 17 + longueur;
    }

    static void processusNettoyer() {
        for (int numéro = 0; numéro < 4; numéro++) {
            ports[numéro] = 0; longueurReçu[numéro] = -1; adresseReçu[numéro] = 0; numéroPortReçu[numéro] = 0;
        }
        for (int numéro = 0; numéro < 64; numéro++) if (PiloteRéseau.recevoir(cadreEntrée) == 0) break;
    }
    static int numéro(int valeurPoignée) { return valeurPoignée >= 3 && valeurPoignée < 7 && ports[valeurPoignée - 3] != 0 ? valeurPoignée - 3 : -1; }
    static int ouvrir(int numéroPort) {
        if (PiloteRéseau.adresseBaseEntréeSortie == 0) return -19;
        if (numéroPort < 0 || numéroPort > 65535) return -22;
        if (numéroPort != 0) for (int numéro = 0; numéro < 4; numéro++) if (ports[numéro] == numéroPort) return -98;
        for (int numéro = 0; numéro < 4; numéro++) if (ports[numéro] == 0) {
            if (numéroPort == 0) {
                numéroPort = 49152;
                boolean chevauchements = true;
                while (chevauchements) {
                    chevauchements = false;
                    for (int valeurAvantCôté = 0; valeurAvantCôté < 4; valeurAvantCôté++) if (ports[valeurAvantCôté] == numéroPort) chevauchements = true;
                    if (chevauchements) numéroPort++;
                }
            }
            ports[numéro] = numéroPort; longueurReçu[numéro] = -1;
            return numéro + 3;
        }
        return -24;
    }
    static int fermer(int valeurPoignée) {
        int entréeÉlémentEmplacement = numéro(valeurPoignée);
        if (entréeÉlémentEmplacement < 0) return -9;
        ports[entréeÉlémentEmplacement] = 0; longueurReçu[entréeÉlémentEmplacement] = -1;
        return 0;
    }
    static int adressePairRéseau(int valeurPoignée) { int entréeÉlémentEmplacement = numéro(valeurPoignée); return entréeÉlémentEmplacement < 0 ? -9 : adresseReçu[entréeÉlémentEmplacement]; }
    static int numéroPortPairRéseau(int valeurPoignée) { int entréeÉlémentEmplacement = numéro(valeurPoignée); return entréeÉlémentEmplacement < 0 ? -9 : numéroPortReçu[entréeÉlémentEmplacement]; }

    static void entêteExterne(int valeurGenre, boolean valeurDiffusionGénérale) {
        for (int numéro = 0; numéro < 6; numéro++) {
            cadreSortie[numéro] = valeurDiffusionGénérale ? 255 : périphériqueTrouvé[numéro];
            cadreSortie[6 + numéro] = PiloteRéseau.adressePériphérique[numéro];
        }
        placer16Bits(cadreSortie, 12, valeurGenre);
    }
    static void adresseRequête(int valeurDestination) {
        entêteExterne(0x0806, true);
        placer16Bits(cadreSortie, 14, 1); placer16Bits(cadreSortie, 16, 0x0800);
        cadreSortie[18] = 6; cadreSortie[19] = 4; placer16Bits(cadreSortie, 20, 1);
        for (int numéro = 0; numéro < 6; numéro++) {
            cadreSortie[22 + numéro] = PiloteRéseau.adressePériphérique[numéro]; cadreSortie[32 + numéro] = 0;
        }
        placer32Bits(cadreSortie, 28, adressePropre); placer32Bits(cadreSortie, 38, valeurDestination);
        PiloteRéseau.envoyer(cadreSortie, 42);
    }
    static void adresseProcessus(int longueur) {
        if (longueur < 42 || entier16(cadreEntrée, 14) != 1 || entier16(cadreEntrée, 16) != 0x0800
            || cadreEntrée[18] != 6 || cadreEntrée[19] != 4 || entier32(cadreEntrée, 38) != adressePropre) { nombreÉlémentsAbandonné++; return; }
        int valeurGenre = entier16(cadreEntrée, 20), valeurPairRéseau = entier32(cadreEntrée, 28);
        if (valeurGenre == 2 && valeurPairRéseau == trouverVersAdresse) {
            for (int numéro = 0; numéro < 6; numéro++) {
                if (cadreEntrée[6 + numéro] != cadreEntrée[22 + numéro] || cadreEntrée[32 + numéro] != PiloteRéseau.adressePériphérique[numéro]) return;
            }
            for (int numéro = 0; numéro < 6; numéro++) périphériqueTrouvé[numéro] = cadreEntrée[22 + numéro];
            adresseTrouvé = valeurPairRéseau;
        } else if (valeurGenre == 1) {
            entêteExterne(0x0806, false);
            placer16Bits(cadreSortie, 14, 1); placer16Bits(cadreSortie, 16, 0x0800);
            cadreSortie[18] = 6; cadreSortie[19] = 4; placer16Bits(cadreSortie, 20, 2);
            for (int numéro = 0; numéro < 6; numéro++) {
                cadreSortie[numéro] = cadreEntrée[22 + numéro]; cadreSortie[32 + numéro] = cadreEntrée[22 + numéro];
                cadreSortie[22 + numéro] = PiloteRéseau.adressePériphérique[numéro];
            }
            placer32Bits(cadreSortie, 28, adressePropre); placer32Bits(cadreSortie, 38, valeurPairRéseau);
            PiloteRéseau.envoyer(cadreSortie, 42);
        }
    }

    static void cadreProcessus(int longueur) {
        if (longueur < 14 || longueur > cadreEntrée.length) { nombreÉlémentsAbandonné++; return; }
        boolean référenceSoi = true, valeurDiffusionGénérale = true;
        for (int numéro = 0; numéro < 6; numéro++) {
            if (cadreEntrée[numéro] != PiloteRéseau.adressePériphérique[numéro]) référenceSoi = false;
            if (cadreEntrée[numéro] != 255) valeurDiffusionGénérale = false;
        }
        if (!référenceSoi && !valeurDiffusionGénérale) return;
        if (entier16(cadreEntrée, 12) == 0x0806) { adresseProcessus(longueur); return; }
        if (entier16(cadreEntrée, 12) != 0x0800) return;
        if (longueur < 34 || (cadreEntrée[14] >>> 4) != 4) { nombreÉlémentsAbandonné++; return; }
        int longueurEntête = (cadreEntrée[14] & 15) * 4, longueurTotal = entier16(cadreEntrée, 16);
        if (longueurEntête < 20 || longueurEntête > 60 || longueurTotal < longueurEntête + 8 || longueurTotal > longueur - 14
            || (entier16(cadreEntrée, 20) & 0x3fff) != 0 || cadreEntrée[23] != 17
            || entier32(cadreEntrée, 30) != adressePropre || valeurSomme(cadreEntrée, 14, longueurEntête, 0) != 65535) { nombreÉlémentsAbandonné++; return; }
        int lancer = 14 + longueurEntête, longueurDonnées = entier16(cadreEntrée, lancer + 4);
        if (longueurDonnées < 8 || longueurDonnées != longueurTotal - longueurEntête || longueurDonnées > 1032) { nombreÉlémentsAbandonné++; return; }
        int valeurDépart = entier32(cadreEntrée, 26);
        if (entier16(cadreEntrée, lancer + 6) != 0 && valeurSomme(cadreEntrée, lancer, longueurDonnées, sommeContrôleEntêtePseudo(valeurDépart, adressePropre, longueurDonnées)) != 65535) {
            nombreÉlémentsAbandonné++; return;
        }
        int valeurDestination = entier16(cadreEntrée, lancer + 2);
        for (int entréeÉlémentEmplacement = 0; entréeÉlémentEmplacement < 4; entréeÉlémentEmplacement++) if (ports[entréeÉlémentEmplacement] != 0 && ports[entréeÉlémentEmplacement] == valeurDestination) {
            if (longueurReçu[entréeÉlémentEmplacement] >= 0) { nombreÉlémentsAbandonné++; return; }
            longueurReçu[entréeÉlémentEmplacement] = longueurDonnées - 8; adresseReçu[entréeÉlémentEmplacement] = valeurDépart; numéroPortReçu[entréeÉlémentEmplacement] = entier16(cadreEntrée, lancer);
            for (int numéro = 0; numéro < longueurDonnées - 8; numéro++) donnéesReçu[entréeÉlémentEmplacement * 1024 + numéro] = cadreEntrée[lancer + 8 + numéro];
            return;
        }
    }

    static void vérifier() {
        for (int numéro = 0; numéro < 16; numéro++) {
            int longueur = PiloteRéseau.recevoir(cadreEntrée);
            if (longueur == 0) return;
            cadreProcessus(longueur);
        }
    }
    static int trouverAdresse(int adresse) {
        if (adresse == 0 || adresse == -1 || (adresse >>> 28) >= 14 || (adresse >>> 24) == 127 || adresse == adressePropre) return -101;
        int élémentListeSuivant = (adresse & masqueRéseau) == (adressePropre & masqueRéseau) ? adresse : valeurPasserelle;
        if (élémentListeSuivant == adresseTrouvé) return 0;
        trouverVersAdresse = élémentListeSuivant;
        int lancer = Périphérique.millisecondes(), requêteSuivant = lancer;
        while (Périphérique.millisecondes() - lancer < 1000) {
            if (Périphérique.millisecondes() - requêteSuivant >= 0) { adresseRequête(élémentListeSuivant); requêteSuivant += 300; }
            vérifier();
            if (adresseTrouvé == élémentListeSuivant) return 0;
            Périphérique.céderBrièvement();
        }
        return -110;
    }
    static int envoyer(int valeurPoignée, int adresse, int numéroPort, int[] Données, int longueur) {
        int entréeÉlémentEmplacement = numéro(valeurPoignée);
        if (entréeÉlémentEmplacement < 0) return -9;
        if (PiloteRéseau.adresseBaseEntréeSortie == 0) return -19;
        if (numéroPort < 1 || numéroPort > 65535 || longueur < 0 || longueur > 1024) return -22;
        int résultat = trouverAdresse(adresse);
        if (résultat < 0) return résultat;
        entêteExterne(0x0800, false);
        cadreSortie[14] = 0x45; cadreSortie[15] = 0; placer16Bits(cadreSortie, 16, 28 + longueur);
        placer16Bits(cadreSortie, 18, valeurIdentificateur++); placer16Bits(cadreSortie, 20, 0x4000);
        cadreSortie[22] = 64; cadreSortie[23] = 17; placer16Bits(cadreSortie, 24, 0);
        placer32Bits(cadreSortie, 26, adressePropre); placer32Bits(cadreSortie, 30, adresse);
        placer16Bits(cadreSortie, 24, ~valeurSomme(cadreSortie, 14, 20, 0));
        placer16Bits(cadreSortie, 34, ports[entréeÉlémentEmplacement]); placer16Bits(cadreSortie, 36, numéroPort);
        placer16Bits(cadreSortie, 38, longueur + 8); placer16Bits(cadreSortie, 40, 0);
        for (int numéro = 0; numéro < longueur; numéro++) cadreSortie[42 + numéro] = Données[numéro] & 255;
        int sommeContrôle = (~valeurSomme(cadreSortie, 34, longueur + 8, sommeContrôleEntêtePseudo(adressePropre, adresse, longueur + 8))) & 65535;
        placer16Bits(cadreSortie, 40, sommeContrôle == 0 ? 65535 : sommeContrôle);
        résultat = PiloteRéseau.envoyer(cadreSortie, longueur + 42);
        return résultat < 0 ? résultat : longueur;
    }
    static int recevoir(int valeurPoignée, int[] Données, int valeurCapacité, int valeurLimite) {
        int entréeÉlémentEmplacement = numéro(valeurPoignée);
        if (entréeÉlémentEmplacement < 0) return -9;
        int lancer = Périphérique.millisecondes();
        while (true) {
            vérifier();
            int longueur = longueurReçu[entréeÉlémentEmplacement];
            if (longueur >= 0) {
                longueurReçu[entréeÉlémentEmplacement] = -1;
                if (longueur > valeurCapacité) return -90;
                for (int numéro = 0; numéro < longueur; numéro++) Données[numéro] = donnéesReçu[entréeÉlémentEmplacement * 1024 + numéro];
                return longueur;
            }
            if (valeurLimite == 0) return -11;
            if (Périphérique.millisecondes() - lancer >= valeurLimite) return -110;
            Périphérique.céderBrièvement();
        }
    }
    static void valeurÉtatValeur() {
        TerminalTexte.écrire(PiloteRéseau.adresseBaseEntréeSortie == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        TerminalTexte.écrire("TX: "); TerminalTexte.écrireNuméro(PiloteRéseau.nombreÉlémentsTransmettre);
        TerminalTexte.écrire(" RX: "); TerminalTexte.écrireNuméro(PiloteRéseau.recevoirNombreÉléments);
        TerminalTexte.écrire(" DROP: "); TerminalTexte.écrireNuméro(nombreÉlémentsAbandonné);
        TerminalTexte.écrire("\n");
    }
}
