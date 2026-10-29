// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systém_súborov;

public final class Súbor_informácia {
    private final int Veľkosť;
    private final int 형태;

    public Súbor_informácia(int Veľkosť, int 형태) {
        this.Veľkosť = Veľkosť;
        this.형태 = 형태;
    }

    public int Veľkosť() {
        return Veľkosť;
    }

    public int 형태() {
        return 형태;
    }
}

