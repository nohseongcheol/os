// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.mobilní_HODNOTA;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Hodiny {
    private final int 초당틱;
    private long čítač_impulzů;

    public Hodiny(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 틱 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long 틱() {
        return ++čítač_impulzů;
    }

    public long čítač_impulzů() {
        return čítač_impulzů;
    }

    public long 지난밀리초() {
        return čítač_impulzů * 1000L / 초당틱;
    }
}

