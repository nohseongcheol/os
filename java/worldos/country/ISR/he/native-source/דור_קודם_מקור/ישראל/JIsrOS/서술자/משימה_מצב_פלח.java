// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.서술자;

/** x86 작업 מתג_מצב 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class משימה_מצב_פלח {
    private int רמז_אפס_בלוק;
    private int רמז_אפס_למען;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int 조각, int למען) {
        רמז_אפס_בלוק = 조각;
        רמז_אפס_למען = למען;
    }

    public int רמז_אפס_בלוק() { return רמז_אפס_בלוק; }
    public int רמז_אפס_למען() { return רמז_אפס_למען; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

