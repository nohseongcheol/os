// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package România.JRouOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 cod_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Evenimente_Listă = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Eveniment 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Cheie_nefuncțional(int Cheie_date) {
        넣기(new 입력사건(입력사건.종류.Cheie_nefuncțional, Cheie_date & 0xff, 0));
    }

    public synchronized void 키놓음(int Cheie_date) {
        넣기(new 입력사건(입력사건.종류.키놓음, Cheie_date & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Verticală_poziție) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Verticală_poziție));
    }

    public synchronized 입력사건 Următorul_eveniment() {
        return Evenimente_Listă.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Eveniment) {
        if (Evenimente_Listă.size() == 최대사건수) {
            Evenimente_Listă.poll();
            버린사건수++;
        }
        Evenimente_Listă.offer(Eveniment);
    }
}

