// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 kod_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Događaji_Popis = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Događaj 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Ključ_izvan_funkcije(int Ključ_podaci) {
        넣기(new 입력사건(입력사건.종류.Ključ_izvan_funkcije, Ključ_podaci & 0xff, 0));
    }

    public synchronized void 키놓음(int Ključ_podaci) {
        넣기(new 입력사건(입력사건.종류.키놓음, Ključ_podaci & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Okomito_položaj) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Okomito_položaj));
    }

    public synchronized 입력사건 Dalje_događaj() {
        return Događaji_Popis.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Događaj) {
        if (Događaji_Popis.size() == 최대사건수) {
            Događaji_Popis.poll();
            버린사건수++;
        }
        Događaji_Popis.offer(Događaj);
    }
}

