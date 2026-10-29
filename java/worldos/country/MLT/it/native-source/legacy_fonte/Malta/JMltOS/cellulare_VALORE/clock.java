// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.cellulare_VALORE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class clock {
    private final int 초당틱;
    private long conteggio;

    public clock(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tick_VALORE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tick_VALORE() {
        return ++conteggio;
    }

    public long conteggio() {
        return conteggio;
    }

    public long 지난밀리초() {
        return conteggio * 1000L / 초당틱;
    }
}

