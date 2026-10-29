// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.vstup_HODNOTA;

public final class vstup_událost {
    public enum Druh_HODNOTA {
        Klíč_mimo_provoz,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Druh_HODNOTA událost_Druh;
    private final int 첫째값;
    private final int SEKUNDA_HODNOTA;

    public vstup_událost(Druh_HODNOTA událost_Druh, int 첫째값, int SEKUNDA_HODNOTA) {
        this.událost_Druh = událost_Druh;
        this.첫째값 = 첫째값;
        this.SEKUNDA_HODNOTA = SEKUNDA_HODNOTA;
    }

    public Druh_HODNOTA událost_Druh() {
        return událost_Druh;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUNDA_HODNOTA() {
        return SEKUNDA_HODNOTA;
    }
}

