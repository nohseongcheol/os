// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_stjórnandi {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Laus;

    public void skrá_færsla(int INDEX, 개입중단처리기 처리기) {
        sannprófa_númer(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void losa_geymsla(int INDEX) {
        sannprófa_númer(INDEX);
        처리기들[INDEX] = null;
    }

    public int dreifa_VALUE(int INDEX, int 저장된쌓임주소) {
        sannprófa_númer(INDEX);
        if (!Laus) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Ferli_VALUE_færsla(저장된쌓임주소);
    }

    public void kveikja() {
        Laus = true;
    }

    public void gera_óvirkan() {
        Laus = false;
    }

    public boolean upplýsingatækni_Laus() {
        return Laus;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void sannprófa_númer(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

