// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_iş_dolandyryjy {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean işjeň;

    public void 등록(int indeks, 개입중단처리기 처리기) {
        번호확인(indeks);
        처리기들[indeks] = 처리기;
    }

    public void goýbermek_Ammar(int indeks) {
        번호확인(indeks);
        처리기들[indeks] = null;
    }

    public int paýla_baha(int indeks, int 저장된쌓임주소) {
        번호확인(indeks);
        if (!işjeň) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[indeks];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proses_baha_girizmeklik(저장된쌓임주소);
    }

    public void mümkinçilik_ber() {
        işjeň = true;
    }

    public void işjeňlikden_aýyr() {
        işjeň = false;
    }

    public boolean 활성인가() {
        return işjeň;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int indeks) {
        if (indeks < 0 || indeks >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

