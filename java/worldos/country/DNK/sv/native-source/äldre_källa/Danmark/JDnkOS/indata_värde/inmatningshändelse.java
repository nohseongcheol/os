// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.indata_värde;

public final class inmatningshändelse {
    public enum variant_värde {
        Nyckel_ur_funktion,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final variant_värde händelsesort;
    private final int 첫째값;
    private final int SEKUND_värde;

    public inmatningshändelse(variant_värde händelsesort, int 첫째값, int SEKUND_värde) {
        this.händelsesort = händelsesort;
        this.첫째값 = 첫째값;
        this.SEKUND_värde = SEKUND_värde;
    }

    public variant_värde händelsesort() {
        return händelsesort;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUND_värde() {
        return SEKUND_värde;
    }
}

