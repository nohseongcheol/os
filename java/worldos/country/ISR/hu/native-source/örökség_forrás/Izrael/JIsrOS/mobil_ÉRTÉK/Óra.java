// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Izrael.JIsrOS.mobil_ÉRTÉK;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Óra {
    private final int 초당틱;
    private long sorszám;

    public Óra(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 órajel_ÉRTÉK 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long órajel_ÉRTÉK() {
        return ++sorszám;
    }

    public long sorszám() {
        return sorszám;
    }

    public long 지난밀리초() {
        return sorszám * 1000L / 초당틱;
    }
}

