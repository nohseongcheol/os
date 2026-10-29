// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aruba.JAbwOS.mobiel_WAARDE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Klok {
    private final int 초당틱;
    private long kloktikgetal;

    public Klok(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tik_WAARDE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tik_WAARDE() {
        return ++kloktikgetal;
    }

    public long kloktikgetal() {
        return kloktikgetal;
    }

    public long 지난밀리초() {
        return kloktikgetal * 1000L / 초당틱;
    }
}

