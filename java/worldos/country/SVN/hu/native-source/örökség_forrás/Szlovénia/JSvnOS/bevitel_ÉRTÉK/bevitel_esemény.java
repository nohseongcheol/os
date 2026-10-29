// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovénia.JSvnOS.bevitel_ÉRTÉK;

public final class bevitel_esemény {
    public enum Altípus_ÉRTÉK {
        키누름,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final Altípus_ÉRTÉK eseményfajta;
    private final int 첫째값;
    private final int MPERC_ÉRTÉK;

    public bevitel_esemény(Altípus_ÉRTÉK eseményfajta, int 첫째값, int MPERC_ÉRTÉK) {
        this.eseményfajta = eseményfajta;
        this.첫째값 = 첫째값;
        this.MPERC_ÉRTÉK = MPERC_ÉRTÉK;
    }

    public Altípus_ÉRTÉK eseményfajta() {
        return eseményfajta;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int MPERC_ÉRTÉK() {
        return MPERC_ÉRTÉK;
    }
}

