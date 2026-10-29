// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Беларусь.JBlrOS.устройство_ЗНАЧЕН;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Часы {
    private final int 초당틱;
    private long счетчик_тактов;

    public Часы(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 такт_ЗНАЧЕН 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long такт_ЗНАЧЕН() {
        return ++счетчик_тактов;
    }

    public long счетчик_тактов() {
        return счетчик_тактов;
    }

    public long 지난밀리초() {
        return счетчик_тактов * 1000L / 초당틱;
    }
}

