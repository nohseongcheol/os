// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CODE_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Sündmused_Loend = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Sündmus 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Võti_rikkis(int Võti_andmed) {
        넣기(new 입력사건(입력사건.종류.Võti_rikkis, Võti_andmed & 0xff, 0));
    }

    public synchronized void 키놓음(int Võti_andmed) {
        넣기(new 입력사건(입력사건.종류.키놓음, Võti_andmed & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int vertikaal_ametikoht) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, vertikaal_ametikoht));
    }

    public synchronized 입력사건 Edasi_sündmus() {
        return Sündmused_Loend.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Sündmus) {
        if (Sündmused_Loend.size() == 최대사건수) {
            Sündmused_Loend.poll();
            버린사건수++;
        }
        Sündmused_Loend.offer(Sündmus);
    }
}

