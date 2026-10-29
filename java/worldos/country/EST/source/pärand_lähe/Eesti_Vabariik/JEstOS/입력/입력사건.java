// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.입력;

public final class 입력사건 {
    public enum 종류 {
        Võti_rikkis,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 sündmuse_liik;
    private final int 첫째값;
    private final int SECOND_VALUE;

    public 입력사건(종류 sündmuse_liik, int 첫째값, int SECOND_VALUE) {
        this.sündmuse_liik = sündmuse_liik;
        this.첫째값 = 첫째값;
        this.SECOND_VALUE = SECOND_VALUE;
    }

    public 종류 sündmuse_liik() {
        return sündmuse_liik;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECOND_VALUE() {
        return SECOND_VALUE;
    }
}

