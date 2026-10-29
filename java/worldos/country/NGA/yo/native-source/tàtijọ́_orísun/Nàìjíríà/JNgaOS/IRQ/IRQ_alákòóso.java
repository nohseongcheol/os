// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_alákòóso {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean tó_ń_ṣiṣẹ́;

    public void forúkọsílẹ̀_ìgbéwọlé(int wá_atọ̀ka_àkóónú, 개입중단처리기 처리기) {
        번호확인(wá_atọ̀ka_àkóónú);
        처리기들[wá_atọ̀ka_àkóónú] = 처리기;
    }

    public void dápadà_Ibi_ìpamọ́(int wá_atọ̀ka_àkóónú) {
        번호확인(wá_atọ̀ka_àkóónú);
        처리기들[wá_atọ̀ka_àkóónú] = null;
    }

    public int pínkiri_iye(int wá_atọ̀ka_àkóónú, int 저장된쌓임주소) {
        번호확인(wá_atọ̀ka_àkóónú);
        if (!tó_ń_ṣiṣẹ́) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[wá_atọ̀ka_àkóónú];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Ìlànà_iye_ìgbéwọlé(저장된쌓임주소);
    }

    public void mu_ṣiṣẹ́() {
        tó_ń_ṣiṣẹ́ = true;
    }

    public void ìsọ_di_àìṣiṣẹ́() {
        tó_ń_ṣiṣẹ́ = false;
    }

    public boolean 활성인가() {
        return tó_ń_ṣiṣẹ́;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú < 0 || wá_atọ̀ka_àkóónú >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

