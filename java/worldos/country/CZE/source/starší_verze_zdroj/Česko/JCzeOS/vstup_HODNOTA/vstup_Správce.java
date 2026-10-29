// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.vstup_HODNOTA;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KÓD_HODNOTA 사이에서 vstup_HODNOTA 사건을 안전하게 넘긴다. */
public final class vstup_Správce {
    private final Queue<vstup_událost> Události_Seznam = new ArrayDeque<vstup_událost>();
    private final int 최대사건수;
    private int 버린사건수;

    public vstup_Správce(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Události 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Klíč_mimo_provoz(int Klíč_data) {
        넣기(new vstup_událost(vstup_událost.Druh_HODNOTA.Klíč_mimo_provoz, Klíč_data & 0xff, 0));
    }

    public synchronized void 키놓음(int Klíč_data) {
        넣기(new vstup_událost(vstup_událost.Druh_HODNOTA.키놓음, Klíč_data & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Svislá_pozice) {
        넣기(new vstup_událost(vstup_událost.Druh_HODNOTA.쥐이동, 가로, Svislá_pozice));
    }

    public synchronized vstup_událost Další_událost() {
        return Události_Seznam.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(vstup_událost Události) {
        if (Události_Seznam.size() == 최대사건수) {
            Události_Seznam.poll();
            버린사건수++;
        }
        Události_Seznam.offer(Události);
    }
}

