// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class testMiseEnRéseau {
    public static int lancer() {
        int ordinalPremier = Utilisateur.ouvrirRéseau(45000);
        if (ordinalPremier < 0) { Utilisateur.écrire("NETWORK UNAVAILABLE\n"); return 3; }
        int[] Données = new int[8];
        boolean valeurPassage = Utilisateur.ouvrirRéseau(45000) == -98
            && Utilisateur.recevoirDonnées(ordinalPremier, Données, 0) == -11
            && Utilisateur.recevoirDonnées(ordinalPremier, Données, 50) == -110
            && Utilisateur.recevoirDonnées(ordinalPremier, Données, 3000) == -22
            && Utilisateur.envoyerDonnées(ordinalPremier, 0x0a000202, 9, Données, 9) == -90
            && Utilisateur.recevoirDonnées(ordinalPremier, null, 0) == -14
            && Utilisateur.fermerRéseau(ordinalPremier) == 0 && Utilisateur.fermerRéseau(ordinalPremier) == -9;
        Utilisateur.écrire(valeurPassage ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return valeurPassage ? 0 : 1;
    }
}
