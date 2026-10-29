// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Upravitelj {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktivan;

    public void registar_unos(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void izdati_Pohrana(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribuirati_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Aktivan) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proces_VALUE_unos(저장된쌓임주소);
    }

    public void omogućiti() {
        Aktivan = true;
    }

    public void deaktivirati() {
        Aktivan = false;
    }

    public boolean odjel_informacijske_tehnologije_Aktivan() {
        return Aktivan;
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

