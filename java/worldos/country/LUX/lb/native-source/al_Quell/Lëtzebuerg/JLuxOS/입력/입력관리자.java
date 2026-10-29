// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CODE_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Evenementer_Lëscht = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Evenement 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int Tast_Daten) {
        넣기(new 입력사건(입력사건.종류.키누름, Tast_Daten & 0xff, 0));
    }

    public synchronized void 키놓음(int Tast_Daten) {
        넣기(new 입력사건(입력사건.종류.키놓음, Tast_Daten & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Vertikal_positionéieren) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Vertikal_positionéieren));
    }

    public synchronized 입력사건 Weider_Evenement() {
        return Evenementer_Lëscht.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Evenement) {
        if (Evenementer_Lëscht.size() == 최대사건수) {
            Evenementer_Lëscht.poll();
            버린사건수++;
        }
        Evenementer_Lëscht.offer(Evenement);
    }
}

