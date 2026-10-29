// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Teste le bouclage réel de l’anneau de réception RTL8139 avec des datagrammes de taille maximale ou impaire. */
public final class boucleRéseau {
    public static int lancer() {
        if (Utilisateur.nombreÉlémentsArguments() != 1) { Utilisateur.écrire("Usage: run stress PORT\n"); return 2; }
        String texte = Utilisateur.arguments(0);
        int valeurPort = 0;
        for (int numéro = 0; numéro < texte.length(); numéro++) {
            if (texte.charAt(numéro) < '0' || texte.charAt(numéro) > '9' || valeurPort > 6553) return 2;
            valeurPort = valeurPort * 10 + texte.charAt(numéro) - '0';
        }
        if (valeurPort < 1 || valeurPort > 65535) return 2;
        int valeurPoignée = Utilisateur.ouvrirRéseau(0);
        if (valeurPoignée < 0) return 3;
        int[] Données = new int[1024];
        for (int ordinalItération = 0; ordinalItération < 24; ordinalItération++) {
            int longueur = 1024 - (ordinalItération & 1);
            for (int numéro = 0; numéro < longueur; numéro++) Données[numéro] = (numéro + ordinalItération) & 255;
            if (Utilisateur.envoyerDonnées(valeurPoignée, 0x0a000202, valeurPort, Données, longueur) != longueur) return 4;
            if (Utilisateur.recevoirDonnées(valeurPoignée, Données, 300) != longueur) return 5;
            for (int numéro = 0; numéro < longueur; numéro++) if (Données[numéro] != ((numéro + ordinalItération) & 255)) return 6;
        }
        Utilisateur.fermerRéseau(valeurPoignée);
        Utilisateur.écrire("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
