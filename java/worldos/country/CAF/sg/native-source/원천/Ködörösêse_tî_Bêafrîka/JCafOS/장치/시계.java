// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ködörösêse_tî_Bêafrîka.JCafOS.장치;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class 시계 {
    private final int 초당틱;
    private long 틱수;

    public 시계(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 틱 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long 틱() {
        return ++틱수;
    }

    public long 틱수() {
        return 틱수;
    }

    public long 지난밀리초() {
        return 틱수 * 1000L / 초당틱;
    }
}

