// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Couleur {
    public static void main(String[] arguments) throws Exception {
        int valeurSomme = 0;
        int nombre = 1;
        while (nombre <= 10) {
            valeurSomme = valeurSomme + nombre;
            nombre = nombre + 1;
        }
        français.interne.Sortie.écrireNuméro(valeurSomme);
        français.interne.Fichier.écrire("aot.txt", "한글 AOT Fichier 😀");
        français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("aot.txt"));
    }
}
