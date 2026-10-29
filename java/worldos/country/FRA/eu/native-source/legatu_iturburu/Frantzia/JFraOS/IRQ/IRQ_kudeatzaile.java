// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_kudeatzaile {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean aktibo;

    public void izena_eman_sarrera(int INDIZE, 개입중단처리기 처리기) {
        번호확인(INDIZE);
        처리기들[INDIZE] = 처리기;
    }

    public void askatu_biltegi(int INDIZE) {
        번호확인(INDIZE);
        처리기들[INDIZE] = null;
    }

    public int banatu_balio(int INDIZE, int 저장된쌓임주소) {
        번호확인(INDIZE);
        if (!aktibo) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDIZE];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.prozesu_balio_sarrera(저장된쌓임주소);
    }

    public void gaitu() {
        aktibo = true;
    }

    public void desaktibatu() {
        aktibo = false;
    }

    public boolean informatika_aktibo() {
        return aktibo;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int INDIZE) {
        if (INDIZE < 0 || INDIZE >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

