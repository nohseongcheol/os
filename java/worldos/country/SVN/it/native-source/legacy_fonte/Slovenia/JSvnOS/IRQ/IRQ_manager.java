// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenia.JSvnOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 gestore 등록과 분배를 담당한다. */
public final class IRQ_manager {
    private final IRQ_gestore[] gestore_elenco = new IRQ_gestore[256];
    private boolean attivo;

    public void registro_voce(int INDICE, IRQ_gestore gestore) {
        verificare_numero(INDICE);
        gestore_elenco[INDICE] = gestore;
    }

    public void release_Memoria(int INDICE) {
        verificare_numero(INDICE);
        gestore_elenco[INDICE] = null;
    }

    public int distribuire_VALORE(int INDICE, int 저장된쌓임주소) {
        verificare_numero(INDICE);
        if (!attivo) {
            return 저장된쌓임주소;
        }
        IRQ_gestore gestore = gestore_elenco[INDICE];
        return gestore == null ? 저장된쌓임주소 : gestore.Processi_VALORE_voce(저장된쌓임주소);
    }

    public void abilitare() {
        attivo = true;
    }

    public void disattivare() {
        attivo = false;
    }

    public boolean reparto_IT_attivo() {
        return attivo;
    }

    public void 모두해제() {
        Arrays.fill(gestore_elenco, null);
    }

    private void verificare_numero(int INDICE) {
        if (INDICE < 0 || INDICE >= gestore_elenco.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

