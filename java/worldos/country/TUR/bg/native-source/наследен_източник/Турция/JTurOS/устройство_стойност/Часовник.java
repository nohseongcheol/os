// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.устройство_стойност;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Часовник {
    private final int 초당틱;
    private long нарастващ_брой;

    public Часовник(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 такт_стойност 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long такт_стойност() {
        return ++нарастващ_брой;
    }

    public long нарастващ_брой() {
        return нарастващ_брой;
    }

    public long 지난밀리초() {
        return нарастващ_брой * 1000L / 초당틱;
    }
}

