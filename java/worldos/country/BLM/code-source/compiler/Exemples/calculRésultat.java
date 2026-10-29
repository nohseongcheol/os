// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class calculRésultat {
    static int valeurTotal(int terminaison) {
        int résultat = 0;
        for (int numéro = 1; numéro <= terminaison; numéro++) résultat += numéro;
        return résultat;
    }

    public static int lancer() {
        int[] valeurs = new int[3];
        valeurs[0] = valeurTotal(10);
        valeurs[1] = -7 / 3;
        valeurs[2] = "한글".length();
        return valeurs[0] == 55 && valeurs[1] == -2 && valeurs[2] == 2 ? 0 : 1;
    }
}
