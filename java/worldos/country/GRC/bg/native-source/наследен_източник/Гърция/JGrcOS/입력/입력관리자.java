// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Гърция.JGrcOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 код_стойност 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Събития_Списък = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Събитие 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Ключ_нефункциониращ(int Ключ_данни) {
        넣기(new 입력사건(입력사건.종류.Ключ_нефункциониращ, Ключ_данни & 0xff, 0));
    }

    public synchronized void 키놓음(int Ключ_данни) {
        넣기(new 입력사건(입력사건.종류.키놓음, Ключ_данни & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int вертикал_позиция) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, вертикал_позиция));
    }

    public synchronized 입력사건 Следваща_събитие() {
        return Събития_Списък.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Събитие) {
        if (Събития_Списък.size() == 최대사건수) {
            Събития_Списък.poll();
            버린사건수++;
        }
        Събития_Списък.offer(Събитие);
    }
}

