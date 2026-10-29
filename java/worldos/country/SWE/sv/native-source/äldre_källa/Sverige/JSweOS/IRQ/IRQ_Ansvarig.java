// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Ansvarig {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktiv;

    public void register_post(int INDEX, 개입중단처리기 처리기) {
        verifiera_nummer(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void släppa_minne(int INDEX) {
        verifiera_nummer(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribuera_värde(int INDEX, int 저장된쌓임주소) {
        verifiera_nummer(INDEX);
        if (!Aktiv) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Process_värde_post(저장된쌓임주소);
    }

    public void aktivera() {
        Aktiv = true;
    }

    public void inaktivera() {
        Aktiv = false;
    }

    public boolean informationsteknik_Aktiv() {
        return Aktiv;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void verifiera_nummer(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

