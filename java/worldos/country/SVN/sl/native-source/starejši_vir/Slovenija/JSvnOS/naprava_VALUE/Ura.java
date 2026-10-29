// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.naprava_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Ura {
    private final int 초당틱;
    private long utrip_COUNT;

    public Ura(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 utrip_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long utrip_VALUE() {
        return ++utrip_COUNT;
    }

    public long utrip_COUNT() {
        return utrip_COUNT;
    }

    public long 지난밀리초() {
        return utrip_COUNT * 1000L / 초당틱;
    }
}

