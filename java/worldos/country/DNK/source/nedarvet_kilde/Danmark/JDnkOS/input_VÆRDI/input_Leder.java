// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.input_VÆRDI;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KODE_VÆRDI 사이에서 input_VÆRDI 사건을 안전하게 넘긴다. */
public final class input_Leder {
    private final Queue<inputhændelse> Events_Liste = new ArrayDeque<inputhændelse>();
    private final int 최대사건수;
    private int 버린사건수;

    public input_Leder(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("hændelse 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void tast_nede(int tast_data) {
        넣기(new inputhændelse(inputhændelse.종류.tast_nede, tast_data & 0xff, 0));
    }

    public synchronized void 키놓음(int tast_data) {
        넣기(new inputhændelse(inputhændelse.종류.키놓음, tast_data & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Lodret_placere) {
        넣기(new inputhændelse(inputhændelse.종류.쥐이동, 가로, Lodret_placere));
    }

    public synchronized inputhændelse Næste_hændelse() {
        return Events_Liste.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(inputhændelse hændelse) {
        if (Events_Liste.size() == 최대사건수) {
            Events_Liste.poll();
            버린사건수++;
        }
        Events_Liste.offer(hændelse);
    }
}

