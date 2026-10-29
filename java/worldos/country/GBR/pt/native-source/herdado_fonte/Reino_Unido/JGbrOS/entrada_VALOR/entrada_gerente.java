// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reino_Unido.JGbrOS.entrada_VALOR;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 valor_do_código 사이에서 entrada_VALOR 사건을 안전하게 넘긴다. */
public final class entrada_gerente {
    private final Queue<entrada_Evento> Eventos_Lista = new ArrayDeque<entrada_Evento>();
    private final int 최대사건수;
    private int 버린사건수;

    public entrada_gerente(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Evento 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Chave_inoperante(int Chave_dados) {
        넣기(new entrada_Evento(entrada_Evento.Tipo_VALOR.Chave_inoperante, Chave_dados & 0xff, 0));
    }

    public synchronized void 키놓음(int Chave_dados) {
        넣기(new entrada_Evento(entrada_Evento.Tipo_VALOR.키놓음, Chave_dados & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Vertical_cargo) {
        넣기(new entrada_Evento(entrada_Evento.Tipo_VALOR.쥐이동, 가로, Vertical_cargo));
    }

    public synchronized entrada_Evento Avançar_Evento() {
        return Eventos_Lista.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(entrada_Evento Evento) {
        if (Eventos_Lista.size() == 최대사건수) {
            Eventos_Lista.poll();
            버린사건수++;
        }
        Eventos_Lista.offer(Evento);
    }
}

