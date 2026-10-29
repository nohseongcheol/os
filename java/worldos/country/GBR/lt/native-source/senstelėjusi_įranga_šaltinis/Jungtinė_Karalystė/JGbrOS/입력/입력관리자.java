// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CODE_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Įvykiai_Sąrašas = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Įvykis 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Raktas_neveikiantis(int Raktas_duomenys) {
        넣기(new 입력사건(입력사건.종류.Raktas_neveikiantis, Raktas_duomenys & 0xff, 0));
    }

    public synchronized void 키놓음(int Raktas_duomenys) {
        넣기(new 입력사건(입력사건.종류.키놓음, Raktas_duomenys & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int segmentas_padėtis) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, segmentas_padėtis));
    }

    public synchronized 입력사건 toliau_įvykis() {
        return Įvykiai_Sąrašas.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Įvykis) {
        if (Įvykiai_Sąrašas.size() == 최대사건수) {
            Įvykiai_Sąrašas.poll();
            버린사건수++;
        }
        Įvykiai_Sąrašas.offer(Įvykis);
    }
}

