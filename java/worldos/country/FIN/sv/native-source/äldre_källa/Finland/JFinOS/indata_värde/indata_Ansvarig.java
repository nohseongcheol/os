// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.indata_värde;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KOD_värde 사이에서 indata_värde 사건을 안전하게 넘긴다. */
public final class indata_Ansvarig {
    private final Queue<inmatningshändelse> Händelser_ange = new ArrayDeque<inmatningshändelse>();
    private final int 최대사건수;
    private int 버린사건수;

    public indata_Ansvarig(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Händelse 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Nyckel_ur_funktion(int Nyckel_data) {
        넣기(new inmatningshändelse(inmatningshändelse.variant_värde.Nyckel_ur_funktion, Nyckel_data & 0xff, 0));
    }

    public synchronized void 키놓음(int Nyckel_data) {
        넣기(new inmatningshändelse(inmatningshändelse.variant_värde.키놓음, Nyckel_data & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int bransch_placera) {
        넣기(new inmatningshändelse(inmatningshändelse.variant_värde.쥐이동, 가로, bransch_placera));
    }

    public synchronized inmatningshändelse Nästa_händelse() {
        return Händelser_ange.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(inmatningshändelse Händelse) {
        if (Händelser_ange.size() == 최대사건수) {
            Händelser_ange.poll();
            버린사건수++;
        }
        Händelser_ange.offer(Händelse);
    }
}

