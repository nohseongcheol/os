// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrajna.JUkrOS.fájlrendszer;

public final class Fájl_infó {
    private final int Méret;
    private final int alakzat_Altípus;

    public Fájl_infó(int Méret, int alakzat_Altípus) {
        this.Méret = Méret;
        this.alakzat_Altípus = alakzat_Altípus;
    }

    public int Méret() {
        return Méret;
    }

    public int alakzat_Altípus() {
        return alakzat_Altípus;
    }
}

