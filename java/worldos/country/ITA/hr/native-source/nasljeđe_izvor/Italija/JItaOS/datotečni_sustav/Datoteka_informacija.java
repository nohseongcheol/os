// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.datotečni_sustav;

public final class Datoteka_informacija {
    private final int Veličina;
    private final int 형태;

    public Datoteka_informacija(int Veličina, int 형태) {
        this.Veličina = Veličina;
        this.형태 = 형태;
    }

    public int Veličina() {
        return Veličina;
    }

    public int 형태() {
        return 형태;
    }
}

