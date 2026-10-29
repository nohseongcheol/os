// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.enhed_VÆRDI;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Ur {
    private final int 초당틱;
    private long tik_TÆL;

    public Ur(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tik_VÆRDI 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tik_VÆRDI() {
        return ++tik_TÆL;
    }

    public long tik_TÆL() {
        return tik_TÆL;
    }

    public long 지난밀리초() {
        return tik_TÆL * 1000L / 초당틱;
    }
}

