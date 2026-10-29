// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.құрылғы_мән;

/** PIT 계층이 올리는 틱과 선점 시점을 관리한다. */
public final class Сағат {
    private final int 초당틱;
    private long тактілер_санауыш;

    public Сағат(int 초당틱) {
        if (초당틱 <= 0) {
            throw new IllegalArgumentException("초당 такт_мән 수가 올바르지 않습니다.");
        }
        this.초당틱 = 초당틱;
    }

    public long такт_мән() {
        return ++тактілер_санауыш;
    }

    public long тактілер_санауыш() {
        return тактілер_санауыш;
    }

    public long 지난밀리초() {
        return тактілер_санауыш * 1000L / 초당틱;
    }
}

