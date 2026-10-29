// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ExempleFichier {
    public static void lancer() throws français.interne.ExceptionSortieEntrée {
        français.interne.Fichier.écrire("java.txt", "JAVA Fichier: français 😀\n");
        français.interne.Sortie.écrire(français.interne.Fichier.lire("java.txt"));
    }
}
