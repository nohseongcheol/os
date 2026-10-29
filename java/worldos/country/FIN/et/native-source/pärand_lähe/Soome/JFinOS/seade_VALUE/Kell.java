// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.seade_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Kell {
    private final int 초당틱;
    private long kriipsuloendus;

    public Kell(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tiks_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tiks_VALUE() {
        return ++kriipsuloendus;
    }

    public long kriipsuloendus() {
        return kriipsuloendus;
    }

    public long 지난밀리초() {
        return kriipsuloendus * 1000L / 초당틱;
    }
}

