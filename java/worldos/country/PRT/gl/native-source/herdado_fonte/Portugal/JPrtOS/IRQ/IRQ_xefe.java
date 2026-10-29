// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_xefe {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Activo;

    public void rexistrarse_introdución(int ÍNDICE, 개입중단처리기 처리기) {
        번호확인(ÍNDICE);
        처리기들[ÍNDICE] = 처리기;
    }

    public void liberar_Almacenamento(int ÍNDICE) {
        번호확인(ÍNDICE);
        처리기들[ÍNDICE] = null;
    }

    public int distribuír_VALOR(int ÍNDICE, int 저장된쌓임주소) {
        번호확인(ÍNDICE);
        if (!Activo) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ÍNDICE];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proceso_VALOR_introdución(저장된쌓임주소);
    }

    public void activar() {
        Activo = true;
    }

    public void desactivar() {
        Activo = false;
    }

    public boolean Tecnoloxía_da_información_TI_Activo() {
        return Activo;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

