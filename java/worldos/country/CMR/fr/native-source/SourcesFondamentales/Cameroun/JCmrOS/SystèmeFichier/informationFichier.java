// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cameroun.JCmrOS.SystèmeFichier;

public final class informationFichier {
    private final int taille;
    private final int genreForme;

    public informationFichier(int taille, int genreForme) {
        this.taille = taille;
        this.genreForme = genreForme;
    }

    public int taille() {
        return taille;
    }

    public int genreForme() {
        return genreForme;
    }
}

