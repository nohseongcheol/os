// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.syöte_ARVO;

public final class syöte_tapahtuma {
    public enum 종류 {
        Avain_ei_toiminnassa,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 tapahtumatyyppi;
    private final int 첫째값;
    private final int SEKUNNIT_ARVO;

    public syöte_tapahtuma(종류 tapahtumatyyppi, int 첫째값, int SEKUNNIT_ARVO) {
        this.tapahtumatyyppi = tapahtumatyyppi;
        this.첫째값 = 첫째값;
        this.SEKUNNIT_ARVO = SEKUNNIT_ARVO;
    }

    public 종류 tapahtumatyyppi() {
        return tapahtumatyyppi;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SEKUNNIT_ARVO() {
        return SEKUNNIT_ARVO;
    }
}

