// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Angola.JAgoOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 manipulador 등록과 분배를 담당한다. */
public final class IRQ_gerente {
    private final IRQ_manipulador[] manipulador_Lista = new IRQ_manipulador[256];
    private boolean Ativo;

    public void registro_entrada(int ÍNDICE, IRQ_manipulador manipulador) {
        verificar_número(ÍNDICE);
        manipulador_Lista[ÍNDICE] = manipulador;
    }

    public void lançar_Armazenamento(int ÍNDICE) {
        verificar_número(ÍNDICE);
        manipulador_Lista[ÍNDICE] = null;
    }

    public int distribuir_VALOR(int ÍNDICE, int 저장된쌓임주소) {
        verificar_número(ÍNDICE);
        if (!Ativo) {
            return 저장된쌓임주소;
        }
        IRQ_manipulador manipulador = manipulador_Lista[ÍNDICE];
        return manipulador == null ? 저장된쌓임주소 : manipulador.Processo_VALOR_entrada(저장된쌓임주소);
    }

    public void ligar() {
        Ativo = true;
    }

    public void desativar() {
        Ativo = false;
    }

    public boolean TI_Ativo() {
        return Ativo;
    }

    public void 모두해제() {
        Arrays.fill(manipulador_Lista, null);
    }

    private void verificar_número(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= manipulador_Lista.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

