// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ungaria.JHunOS.mobil_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Ceas {
    private final int 초당틱;
    private long contor_de_cicluri;

    public Ceas(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 gradație_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long gradație_VALUE() {
        return ++contor_de_cicluri;
    }

    public long contor_de_cicluri() {
        return contor_de_cicluri;
    }

    public long 지난밀리초() {
        return contor_de_cicluri * 1000L / 초당틱;
    }
}

