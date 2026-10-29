// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.input_VÆRDI;

public final class inputhændelse {
    public enum 종류 {
        tast_nede,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 hændelsestype;
    private final int 첫째값;
    private final int SEKUND_VÆRDI;

    public inputhændelse(종류 hændelsestype, int 첫째값, int SEKUND_VÆRDI) {
        this.hændelsestype = hændelsestype;
        this.첫째값 = 첫째값;
        this.SEKUND_VÆRDI = SEKUND_VÆRDI;
    }

    public 종류 hændelsestype() {
        return hændelsestype;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUND_VÆRDI() {
        return SEKUND_VÆRDI;
    }
}

