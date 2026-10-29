// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Croasia.JHrvOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 코드 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> 사건들 = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("사건 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int 키값) {
        넣기(new 입력사건(입력사건.종류.키누름, 키값 & 0xff, 0));
    }

    public synchronized void 키놓음(int 키값) {
        넣기(new 입력사건(입력사건.종류.키놓음, 키값 & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int 세로) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, 세로));
    }

    public synchronized 입력사건 다음사건() {
        return 사건들.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 사건) {
        if (사건들.size() == 최대사건수) {
            사건들.poll();
            버린사건수++;
        }
        사건들.offer(사건);
    }
}

