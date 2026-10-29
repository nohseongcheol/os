// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.inndata_VERDI;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KODE_VERDI 사이에서 inndata_VERDI 사건을 안전하게 넘긴다. */
public final class inndata_overordnet {
    private final Queue<inndatahendelse> Events_Liste = new ArrayDeque<inndatahendelse>();
    private final int 최대사건수;
    private int 버린사건수;

    public inndata_overordnet(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Hendelse 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int tast_data) {
        넣기(new inndatahendelse(inndatahendelse.종류.키누름, tast_data & 0xff, 0));
    }

    public synchronized void 키놓음(int tast_data) {
        넣기(new inndatahendelse(inndatahendelse.종류.키놓음, tast_data & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int vertikal_plassere) {
        넣기(new inndatahendelse(inndatahendelse.종류.쥐이동, 가로, vertikal_plassere));
    }

    public synchronized inndatahendelse Neste_hendelse() {
        return Events_Liste.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(inndatahendelse Hendelse) {
        if (Events_Liste.size() == 최대사건수) {
            Events_Liste.poll();
            버린사건수++;
        }
        Events_Liste.offer(Hendelse);
    }
}

