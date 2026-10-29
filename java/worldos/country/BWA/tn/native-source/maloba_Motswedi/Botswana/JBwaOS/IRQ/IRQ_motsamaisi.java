// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_motsamaisi {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean e_e_dirisiwang;

    public void kwadisa_tsenyo(int tshupane, 개입중단처리기 처리기) {
        번호확인(tshupane);
        처리기들[tshupane] = 처리기;
    }

    public void ntsha_Polokelo(int tshupane) {
        번호확인(tshupane);
        처리기들[tshupane] = null;
    }

    public int aba_Boleng(int tshupane, int 저장된쌓임주소) {
        번호확인(tshupane);
        if (!e_e_dirisiwang) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[tshupane];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Thulaganyo_Boleng_tsenyo(저장된쌓임주소);
    }

    public void kgontsha() {
        e_e_dirisiwang = true;
    }

    public void kgontsha_go_dira() {
        e_e_dirisiwang = false;
    }

    public boolean 활성인가() {
        return e_e_dirisiwang;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int tshupane) {
        if (tshupane < 0 || tshupane >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

