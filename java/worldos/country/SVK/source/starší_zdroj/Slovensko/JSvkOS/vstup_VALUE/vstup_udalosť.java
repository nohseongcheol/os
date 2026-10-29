// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.vstup_VALUE;

public final class vstup_udalosť {
    public enum 종류 {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 druh_udalosti;
    private final int 첫째값;
    private final int SECOND_VALUE;

    public vstup_udalosť(종류 druh_udalosti, int 첫째값, int SECOND_VALUE) {
        this.druh_udalosti = druh_udalosti;
        this.첫째값 = 첫째값;
        this.SECOND_VALUE = SECOND_VALUE;
    }

    public 종류 druh_udalosti() {
        return druh_udalosti;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECOND_VALUE() {
        return SECOND_VALUE;
    }
}

