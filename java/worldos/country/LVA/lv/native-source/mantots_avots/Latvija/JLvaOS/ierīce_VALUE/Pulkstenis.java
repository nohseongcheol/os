// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.ierīce_VALUE;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Pulkstenis {
    private final int 초당틱;
    private long mirkļu_skaits;

    public Pulkstenis(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 tikšķis_VALUE 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long tikšķis_VALUE() {
        return ++mirkļu_skaits;
    }

    public long mirkļu_skaits() {
        return mirkļu_skaits;
    }

    public long 지난밀리초() {
        return mirkļu_skaits * 1000L / 초당틱;
    }
}

