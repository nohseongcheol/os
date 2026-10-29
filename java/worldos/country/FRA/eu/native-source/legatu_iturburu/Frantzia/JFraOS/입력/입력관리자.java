// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KODE_balio 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Gertaerak_Zerrenda = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Gertaera 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int gako_datuak) {
        넣기(new 입력사건(입력사건.종류.키누름, gako_datuak & 0xff, 0));
    }

    public synchronized void 키놓음(int gako_datuak) {
        넣기(new 입력사건(입력사건.종류.키놓음, gako_datuak & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Bertikala_kargu) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Bertikala_kargu));
    }

    public synchronized 입력사건 Hurrengoa_gertaera() {
        return Gertaerak_Zerrenda.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Gertaera) {
        if (Gertaerak_Zerrenda.size() == 최대사건수) {
            Gertaerak_Zerrenda.poll();
            버린사건수++;
        }
        Gertaerak_Zerrenda.offer(Gertaera);
    }
}

