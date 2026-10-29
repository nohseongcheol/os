// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Канада.JCanOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 код_значення 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Події_список = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Подія 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Ключ_неробочий(int Ключ_дані) {
        넣기(new 입력사건(입력사건.종류.Ключ_неробочий, Ключ_дані & 0xff, 0));
    }

    public synchronized void 키놓음(int Ключ_дані) {
        넣기(new 입력사건(입력사건.종류.키놓음, Ключ_дані & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Вертикаль_посада) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Вертикаль_посада));
    }

    public synchronized 입력사건 Далі_подія() {
        return Події_список.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Подія) {
        if (Події_список.size() == 최대사건수) {
            Події_список.poll();
            버린사건수++;
        }
        Події_список.offer(Подія);
    }
}

