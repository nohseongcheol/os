// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.datotečni_sistem;

public final class Datoteka_informacije {
    private final int Velikost;
    private final int 형태;

    public Datoteka_informacije(int Velikost, int 형태) {
        this.Velikost = Velikost;
        this.형태 = 형태;
    }

    public int Velikost() {
        return Velikost;
    }

    public int 형태() {
        return 형태;
    }
}

