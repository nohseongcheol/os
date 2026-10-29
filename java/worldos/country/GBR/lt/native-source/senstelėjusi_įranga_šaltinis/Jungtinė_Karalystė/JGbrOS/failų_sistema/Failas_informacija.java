// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.failų_sistema;

public final class Failas_informacija {
    private final int Dydis;
    private final int 형태;

    public Failas_informacija(int Dydis, int 형태) {
        this.Dydis = Dydis;
        this.형태 = 형태;
    }

    public int Dydis() {
        return Dydis;
    }

    public int 형태() {
        return 형태;
    }
}

