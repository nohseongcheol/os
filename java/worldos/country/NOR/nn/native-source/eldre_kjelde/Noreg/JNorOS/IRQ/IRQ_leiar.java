// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_leiar {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean aktiv;

    public void registrere_oppføring(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void frigi_Lagring(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribuere_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!aktiv) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Prosess_VALUE_oppføring(저장된쌓임주소);
    }

    public void slå_på() {
        aktiv = true;
    }

    public void deaktivere() {
        aktiv = false;
    }

    public boolean informasjonsteknologi_aktiv() {
        return aktiv;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

