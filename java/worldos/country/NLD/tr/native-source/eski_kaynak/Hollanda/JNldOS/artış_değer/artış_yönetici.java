// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.artış_değer;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KOD_değer 사이에서 artış_değer 사건을 안전하게 넘긴다. */
public final class artış_yönetici {
    private final Queue<artış_olay> Etkinlikler_Liste = new ArrayDeque<artış_olay>();
    private final int 최대사건수;
    private int 버린사건수;

    public artış_yönetici(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Olay 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void tuş_kapalı(int tuş_veri) {
        넣기(new artış_olay(artış_olay.Tip_değer.tuş_kapalı, tuş_veri & 0xff, 0));
    }

    public synchronized void 키놓음(int tuş_veri) {
        넣기(new artış_olay(artış_olay.Tip_değer.키놓음, tuş_veri & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Dikey_konum) {
        넣기(new artış_olay(artış_olay.Tip_değer.쥐이동, 가로, Dikey_konum));
    }

    public synchronized artış_olay Sonraki_olay() {
        return Etkinlikler_Liste.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(artış_olay Olay) {
        if (Etkinlikler_Liste.size() == 최대사건수) {
            Etkinlikler_Liste.poll();
            버린사건수++;
        }
        Etkinlikler_Liste.offer(Olay);
    }
}

