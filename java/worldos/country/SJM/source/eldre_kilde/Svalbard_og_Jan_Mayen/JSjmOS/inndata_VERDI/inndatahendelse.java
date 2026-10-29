// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.inndata_VERDI;

public final class inndatahendelse {
    public enum 종류 {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 사건종류;
    private final int 첫째값;
    private final int SEKUND_VERDI;

    public inndatahendelse(종류 사건종류, int 첫째값, int SEKUND_VERDI) {
        this.사건종류 = 사건종류;
        this.첫째값 = 첫째값;
        this.SEKUND_VERDI = SEKUND_VERDI;
    }

    public 종류 사건종류() {
        return 사건종류;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUND_VERDI() {
        return SEKUND_VERDI;
    }
}

