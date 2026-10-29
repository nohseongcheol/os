// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aruba.JAbwOS.invoer_WAARDE;

public final class invoergebeurtenis {
    public enum soort_WAARDE {
        toets_offline,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final soort_WAARDE soort_gebeurtenis;
    private final int 첫째값;
    private final int SECONDE_WAARDE;

    public invoergebeurtenis(soort_WAARDE soort_gebeurtenis, int 첫째값, int SECONDE_WAARDE) {
        this.soort_gebeurtenis = soort_gebeurtenis;
        this.첫째값 = 첫째값;
        this.SECONDE_WAARDE = SECONDE_WAARDE;
    }

    public soort_WAARDE soort_gebeurtenis() {
        return soort_gebeurtenis;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECONDE_WAARDE() {
        return SECONDE_WAARDE;
    }
}

