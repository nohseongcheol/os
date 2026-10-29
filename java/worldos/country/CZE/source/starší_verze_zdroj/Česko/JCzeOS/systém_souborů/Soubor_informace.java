// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systém_souborů;

public final class Soubor_informace {
    private final int Velikost;
    private final int tvar_Druh;

    public Soubor_informace(int Velikost, int tvar_Druh) {
        this.Velikost = Velikost;
        this.tvar_Druh = tvar_Druh;
    }

    public int Velikost() {
        return Velikost;
    }

    public int tvar_Druh() {
        return tvar_Druh;
    }
}

