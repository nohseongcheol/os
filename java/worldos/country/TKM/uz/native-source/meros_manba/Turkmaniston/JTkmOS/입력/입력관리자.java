// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 kod_VALUE 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Hodisalar_Ro_yxat = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("hodisa 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int Kalit_ma_lumotlar) {
        넣기(new 입력사건(입력사건.종류.키누름, Kalit_ma_lumotlar & 0xff, 0));
    }

    public synchronized void 키놓음(int Kalit_ma_lumotlar) {
        넣기(new 입력사건(입력사건.종류.키놓음, Kalit_ma_lumotlar & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Vertikal_holat) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Vertikal_holat));
    }

    public synchronized 입력사건 Keyingi_hodisa() {
        return Hodisalar_Ro_yxat.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 hodisa) {
        if (Hodisalar_Ro_yxat.size() == 최대사건수) {
            Hodisalar_Ro_yxat.poll();
            버린사건수++;
        }
        Hodisalar_Ro_yxat.offer(hodisa);
    }
}

