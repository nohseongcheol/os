// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Maďarsko.JHunOS.vstup_VALUE;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 kód_VALUE 사이에서 vstup_VALUE 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<vstup_udalosť> Udalosti_Zoznam = new ArrayDeque<vstup_udalosť>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Udalosť 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int Kľúč_údaje) {
        넣기(new vstup_udalosť(vstup_udalosť.종류.키누름, Kľúč_údaje & 0xff, 0));
    }

    public synchronized void 키놓음(int Kľúč_údaje) {
        넣기(new vstup_udalosť(vstup_udalosť.종류.키놓음, Kľúč_údaje & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int vertikála_pozícia) {
        넣기(new vstup_udalosť(vstup_udalosť.종류.쥐이동, 가로, vertikála_pozícia));
    }

    public synchronized vstup_udalosť Ďalej_udalosť() {
        return Udalosti_Zoznam.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(vstup_udalosť Udalosť) {
        if (Udalosti_Zoznam.size() == 최대사건수) {
            Udalosti_Zoznam.poll();
            버린사건수++;
        }
        Udalosti_Zoznam.offer(Udalosť);
    }
}

