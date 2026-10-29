// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class CommunicationDonnées {
    static int valeurChiffre(String texte) {
        if (texte == null || texte.length() == 0) return -1;
        int résultat = 0;
        for (int numéro = 0; numéro < texte.length(); numéro++) {
            int valeur = texte.charAt(numéro) - '0';
            if (valeur < 0 || valeur > 9 || résultat > 6553) return -1;
            résultat = résultat * 10 + valeur;
            if (résultat > 65535) return -1;
        }
        return résultat;
    }
    static int adresse(String texte) {
        if (texte == null) return 0;
        int valeur = 0, résultat = 0, valeurSousPartie = 0, chiffres = 0;
        for (int numéro = 0; numéro <= texte.length(); numéro++) {
            int Caractères = numéro == texte.length() ? '.' : texte.charAt(numéro);
            if (Caractères == '.') {
                if (chiffres == 0 || valeurSousPartie == 4) return 0;
                résultat = (résultat << 8) | valeur; valeurSousPartie++; valeur = 0; chiffres = 0;
            } else {
                if (Caractères < '0' || Caractères > '9') return 0;
                valeur = valeur * 10 + Caractères - '0';
                if (++chiffres > 3 || valeur > 255) return 0;
            }
        }
        return valeurSousPartie == 4 ? résultat : 0;
    }
    public static int lancer() {
        if (Utilisateur.nombreÉlémentsArguments() != 3) { Utilisateur.écrire("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresse = adresse(Utilisateur.arguments(0)), valeurPort = valeurChiffre(Utilisateur.arguments(1));
        String valeurContenuValeur = Utilisateur.arguments(2);
        if (adresse == 0 || valeurPort < 1 || valeurContenuValeur.length() > 1024) { Utilisateur.écrire("Bad destination\n"); return 2; }
        int valeurPoignée = Utilisateur.ouvrirRéseau(0);
        if (valeurPoignée < 0) { Utilisateur.écrire("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] Données = new int[1024];
        for (int numéro = 0; numéro < valeurContenuValeur.length(); numéro++) Données[numéro] = valeurContenuValeur.charAt(numéro);
        if (Utilisateur.envoyerDonnées(valeurPoignée, adresse, valeurPort, Données, valeurContenuValeur.length()) < 0) {
            Utilisateur.écrire("UDP SEND FAILED\n"); Utilisateur.fermerRéseau(valeurPoignée); return 4;
        }
        Utilisateur.écrire("UDP SENT\n");
        int longueurReçu = Utilisateur.recevoirDonnées(valeurPoignée, Données, 1500);
        boolean texteÉgal = longueurReçu == valeurContenuValeur.length() && Utilisateur.adresseEnvoyé(valeurPoignée) == adresse && Utilisateur.portEnvoyé(valeurPoignée) == valeurPort;
        if (texteÉgal) for (int numéro = 0; numéro < longueurReçu; numéro++) if (Données[numéro] != valeurContenuValeur.charAt(numéro)) texteÉgal = false;
        Utilisateur.fermerRéseau(valeurPoignée);
        if (longueurReçu < 0) { Utilisateur.écrire("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        Utilisateur.écrire(texteÉgal ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return texteÉgal ? 0 : 6;
    }
}
