// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Manaja {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aiki_d9ba6551;

    public void 등록(int Indes, 개입중단처리기 처리기) {
        번호확인(Indes);
        처리기들[Indes] = 처리기;
    }

    public void saka_Wurin_adana(int Indes) {
        번호확인(Indes);
        처리기들[Indes] = null;
    }

    public int rarraba_Daraja(int Indes, int 저장된쌓임주소) {
        번호확인(Indes);
        if (!Aiki_d9ba6551) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[Indes];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.haryar_aikin_na_ura_Daraja_Mashigar_bayanai(저장된쌓임주소);
    }

    public void kunna() {
        Aiki_d9ba6551 = true;
    }

    public void nakasa() {
        Aiki_d9ba6551 = false;
    }

    public boolean kimiyar_bayanai_Aiki() {
        return Aiki_d9ba6551;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int Indes) {
        if (Indes < 0 || Indes >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

