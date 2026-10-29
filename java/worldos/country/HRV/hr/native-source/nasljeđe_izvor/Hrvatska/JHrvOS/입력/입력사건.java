// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hrvatska.JHrvOS.입력;

public final class 입력사건 {
    public enum 종류 {
        Ključ_izvan_funkcije,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 vrsta_događaja;
    private final int 첫째값;
    private final int SECOND_VALUE;

    public 입력사건(종류 vrsta_događaja, int 첫째값, int SECOND_VALUE) {
        this.vrsta_događaja = vrsta_događaja;
        this.첫째값 = 첫째값;
        this.SECOND_VALUE = SECOND_VALUE;
    }

    public 종류 vrsta_događaja() {
        return vrsta_događaja;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECOND_VALUE() {
        return SECOND_VALUE;
    }
}

