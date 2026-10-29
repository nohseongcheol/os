// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.input_VALORE;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 CODICE_VALORE 사이에서 input_VALORE 사건을 안전하게 넘긴다. */
public final class input_manager {
    private final Queue<evento_di_input> Eventi_elenco = new ArrayDeque<evento_di_input>();
    private final int 최대사건수;
    private int 버린사건수;

    public input_manager(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Evento 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int tasto_dati) {
        넣기(new evento_di_input(evento_di_input.Kind_VALORE.키누름, tasto_dati & 0xff, 0));
    }

    public synchronized void 키놓음(int tasto_dati) {
        넣기(new evento_di_input(evento_di_input.Kind_VALORE.키놓음, tasto_dati & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Verticale_funzione) {
        넣기(new evento_di_input(evento_di_input.Kind_VALORE.쥐이동, 가로, Verticale_funzione));
    }

    public synchronized evento_di_input Avanti_evento() {
        return Eventi_elenco.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(evento_di_input Evento) {
        if (Eventi_elenco.size() == 최대사건수) {
            Eventi_elenco.poll();
            버린사건수++;
        }
        Eventi_elenco.offer(Evento);
    }
}

