// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Leder {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktiv;

    public void register_post(int INDEKS, 개입중단처리기 처리기) {
        bekræfte_tal(INDEKS);
        처리기들[INDEKS] = 처리기;
    }

    public void udgive_Lager(int INDEKS) {
        bekræfte_tal(INDEKS);
        처리기들[INDEKS] = null;
    }

    public int fordele_VÆRDI(int INDEKS, int 저장된쌓임주소) {
        bekræfte_tal(INDEKS);
        if (!Aktiv) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEKS];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proces_VÆRDI_post(저장된쌓임주소);
    }

    public void slå_til() {
        Aktiv = true;
    }

    public void deaktivere() {
        Aktiv = false;
    }

    public boolean it_Aktiv() {
        return Aktiv;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void bekræfte_tal(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

