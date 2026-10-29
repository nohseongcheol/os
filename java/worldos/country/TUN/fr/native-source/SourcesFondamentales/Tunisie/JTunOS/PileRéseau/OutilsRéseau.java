// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tunisie.JTunOS.PileRéseau;

/** Outils d’ordre des octets et de somme de contrôle communs aux couches Ethernet/ARP/IPv4/ICMP/UDP. */
public final class OutilsRéseau {
    private OutilsRéseau() {
    }

    public static int courtOrdreOctetsGrand(byte[] Données, int position) {
        contrôlerPlage(Données, position, 2);
        return ((Données[position] & 0xff) << 8) | (Données[position + 1] & 0xff);
    }

    public static long entierOrdreOctetsGrand(byte[] Données, int position) {
        contrôlerPlage(Données, position, 4);
        return ((long) (Données[position] & 0xff) << 24)
                | ((long) (Données[position + 1] & 0xff) << 16)
                | ((long) (Données[position + 2] & 0xff) << 8)
                | (Données[position + 3] & 0xffL);
    }

    public static int sommeContrôleInternet(byte[] Données, int lancer, int longueur) {
        contrôlerPlage(Données, lancer, longueur);
        long valeurSomme = 0;
        int terminaison = lancer + longueur;
        int position = lancer;
        while (position + 1 < terminaison) {
            valeurSomme += courtOrdreOctetsGrand(Données, position);
            position += 2;
        }
        if (position < terminaison) {
            valeurSomme += (Données[position] & 0xff) << 8;
        }
        while ((valeurSomme >>> 16) != 0) {
            valeurSomme = (valeurSomme & 0xffff) + (valeurSomme >>> 16);
        }
        return (int) (~valeurSomme) & 0xffff;
    }

    public static boolean estCadreEthernet(byte[] Données) {
        return Données != null && Données.length >= 14;
    }

    public static int protocoleSupérieurEthernet(byte[] Données) {
        if (!estCadreEthernet(Données)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return courtOrdreOctetsGrand(Données, 12);
    }

    public static boolean estProtocole4VersionIP(byte[] Données, int position) {
        if (Données == null || position < 0 || Données.length - position < 20) {
            return false;
        }
        int valeurVersion = (Données[position] >>> 4) & 0xf;
        int longueurEntête = (Données[position] & 0xf) * 4;
        return valeurVersion == 4 && longueurEntête >= 20 && Données.length - position >= longueurEntête;
    }

    private static void contrôlerPlage(byte[] Données, int lancer, int longueur) {
        if (Données == null || lancer < 0 || longueur < 0 || lancer > Données.length - longueur) {
            throw new IllegalArgumentException("PileRéseau Données 범위를 벗어났습니다.");
        }
    }
}

