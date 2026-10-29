// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ausztria.JAutOS.bevitel_ÉRTÉK;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KÓD_ÉRTÉK 사이에서 bevitel_ÉRTÉK 사건을 안전하게 넘긴다. */
public final class bevitel_kezelő {
    private final Queue<bevitel_esemény> Események_Lista = new ArrayDeque<bevitel_esemény>();
    private final int 최대사건수;
    private int 버린사건수;

    public bevitel_kezelő(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Esemény 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int Kulcs_adat) {
        넣기(new bevitel_esemény(bevitel_esemény.Altípus_ÉRTÉK.키누름, Kulcs_adat & 0xff, 0));
    }

    public synchronized void 키놓음(int Kulcs_adat) {
        넣기(new bevitel_esemény(bevitel_esemény.Altípus_ÉRTÉK.키놓음, Kulcs_adat & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int szektor_pozíció) {
        넣기(new bevitel_esemény(bevitel_esemény.Altípus_ÉRTÉK.쥐이동, 가로, szektor_pozíció));
    }

    public synchronized bevitel_esemény Tovább_esemény() {
        return Események_Lista.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(bevitel_esemény Esemény) {
        if (Események_Lista.size() == 최대사건수) {
            Események_Lista.poll();
            버린사건수++;
        }
        Események_Lista.offer(Esemény);
    }
}

