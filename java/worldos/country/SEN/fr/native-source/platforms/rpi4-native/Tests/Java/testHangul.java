// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.interne.Caractères;
import français.interne.Fichier;
import français.interne.listeEntréeÉlément;
import français.interne.Dictionnaire;
import français.interne.Sortie;
public class testHangul {
    public static void main(String[] a) throws Exception {
        String Salutation = "안녕하세요 · 日本語 · العربية · 😀";
        Sortie.écrireLigne(Caractères.déchiffrerDonnées(Caractères.encoder(Salutation))); Sortie.écrireNuméro(Caractères.nombreÉlémentsPointCode("한글😀"));
        Fichier.écrire("한글자료.txt", Salutation); Sortie.écrireLigne(Fichier.lire("한글자료.txt"));
        listeEntréeÉlément listeNoms = new listeEntréeÉlément(); listeNoms.ajouterValeurs("가람"); listeNoms.ajouterValeurs("누리"); Sortie.écrireLigne(listeNoms.lire(1));
        Dictionnaire valeurSens = new Dictionnaire(); valeurSens.placerValeur("가람", "강"); System.gc(); Sortie.écrireLigne(valeurSens.trouverEntréeÉlément("가람"));
        try { Caractères.déchiffrerDonnées(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Sortie.écrireLigne("UTF-8 erreur rejeterValeur"); }
        Sortie.écrireLigne("français bibliothèque estTerminé");
    }
}
