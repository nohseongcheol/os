// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lenkija.JPolOS.įrenginys_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class laikrodis {
    private final int 초당틱;
    private long atnaujinimų_ciklų_skaičius;

    public laikrodis(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tiksėjimas_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tiksėjimas_VALUE() {
        return ++atnaujinimų_ciklų_skaičius;
    }

    public long atnaujinimų_ciklų_skaičius() {
        return atnaujinimų_ciklų_skaičius;
    }

    public long 지난밀리초() {
        return atnaujinimų_ciklų_skaičius * 1000L / 초당틱;
    }
}

