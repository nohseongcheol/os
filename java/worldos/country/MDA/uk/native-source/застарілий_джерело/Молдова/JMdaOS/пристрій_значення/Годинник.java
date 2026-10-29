// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.пристрій_значення;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Годинник {
    private final int 초당틱;
    private long лічильник_змін;

    public Годинник(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 такт_значення 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long такт_значення() {
        return ++лічильник_змін;
    }

    public long лічильник_змін() {
        return лічильник_змін;
    }

    public long 지난밀리초() {
        return лічильник_змін * 1000L / 초당틱;
    }
}

