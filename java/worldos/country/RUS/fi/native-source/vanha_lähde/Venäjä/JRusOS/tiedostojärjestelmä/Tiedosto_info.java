// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.tiedostojärjestelmä;

public final class Tiedosto_info {
    private final int Koko;
    private final int 형태;

    public Tiedosto_info(int Koko, int 형태) {
        this.Koko = Koko;
        this.형태 = 형태;
    }

    public int Koko() {
        return Koko;
    }

    public int 형태() {
        return 형태;
    }
}

