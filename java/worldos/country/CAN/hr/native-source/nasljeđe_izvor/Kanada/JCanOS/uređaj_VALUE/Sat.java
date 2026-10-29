// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.uređaj_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Sat {
    private final int 초당틱;
    private long brojač_promjena;

    public Sat(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 otkucavanje_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long otkucavanje_VALUE() {
        return ++brojač_promjena;
    }

    public long brojač_promjena() {
        return brojač_promjena;
    }

    public long 지난밀리초() {
        return brojač_promjena * 1000L / 초당틱;
    }
}

