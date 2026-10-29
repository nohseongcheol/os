// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.cihaz_değer;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Saat {
    private final int 초당틱;
    private long kimlik_numarası;

    public Saat(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tık_değer_a516cff0 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tık_değer_a516cff0() {
        return ++kimlik_numarası;
    }

    public long kimlik_numarası() {
        return kimlik_numarası;
    }

    public long 지난밀리초() {
        return kimlik_numarası * 1000L / 초당틱;
    }
}

