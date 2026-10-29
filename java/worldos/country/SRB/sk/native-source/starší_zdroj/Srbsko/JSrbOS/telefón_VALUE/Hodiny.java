// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbsko.JSrbOS.telefón_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Hodiny {
    private final int 초당틱;
    private long počítadlo_impulzov;

    public Hodiny(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 틱 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long 틱() {
        return ++počítadlo_impulzov;
    }

    public long počítadlo_impulzov() {
        return počítadlo_impulzov;
    }

    public long 지난밀리초() {
        return počítadlo_impulzov * 1000L / 초당틱;
    }
}

