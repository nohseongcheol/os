// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.입력;

public final class 입력사건 {
    public enum 종류 {
        Kunci_bawah,
        키놓음,
        쥐이동,
        쥐단추누름,
        쥐단추놓음
    }

    private final 종류 jenis_peristiwa;
    private final int 첫째값;
    private final int SECOND_VALUE;

    public 입력사건(종류 jenis_peristiwa, int 첫째값, int SECOND_VALUE) {
        this.jenis_peristiwa = jenis_peristiwa;
        this.첫째값 = 첫째값;
        this.SECOND_VALUE = SECOND_VALUE;
    }

    public 종류 jenis_peristiwa() {
        return jenis_peristiwa;
    }

    public int 첫째값() {
        return 첫째값;
    }

    public int SECOND_VALUE() {
        return SECOND_VALUE;
    }
}

