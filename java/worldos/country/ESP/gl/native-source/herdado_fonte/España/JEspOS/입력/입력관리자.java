// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CÓDIGO_VALOR 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> Eventos_Lista = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Evento 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int Chave_datos) {
        넣기(new 입력사건(입력사건.종류.키누름, Chave_datos & 0xff, 0));
    }

    public synchronized void 키놓음(int Chave_datos) {
        넣기(new 입력사건(입력사건.종류.키놓음, Chave_datos & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Vertical_cargo) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, Vertical_cargo));
    }

    public synchronized 입력사건 Seguinte_evento() {
        return Eventos_Lista.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 Evento) {
        if (Eventos_Lista.size() == 최대사건수) {
            Eventos_Lista.poll();
            버린사건수++;
        }
        Eventos_Lista.offer(Evento);
    }
}

