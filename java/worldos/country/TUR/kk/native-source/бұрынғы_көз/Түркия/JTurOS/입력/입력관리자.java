// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Түркия.JTurOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 код_мән 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Оқиғалар_Тізім = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Оқиға 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Кілт_ажыратылған(int Кілт_деректер) {
        넣기(new 입력사건(입력사건.종류.Кілт_ажыратылған, Кілт_деректер & 0xff, 0));
    }

    public synchronized void 키놓음(int Кілт_деректер) {
        넣기(new 입력사건(입력사건.종류.키놓음, Кілт_деректер & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Тік_лауазым) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Тік_лауазым));
    }

    public synchronized 입력사건 Келесі_оқиға() {
        return Оқиғалар_Тізім.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Оқиға) {
        if (Оқиғалар_Тізім.size() == 최대사건수) {
            Оқиғалар_Тізім.poll();
            버린사건수++;
        }
        Оқиғалар_Тізім.offer(Оқиға);
    }
}

