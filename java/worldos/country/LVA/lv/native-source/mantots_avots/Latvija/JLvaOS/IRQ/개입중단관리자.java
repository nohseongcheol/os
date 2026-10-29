// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktīvs;

    public void reģistrs_ievade(int INDEX, 개입중단처리기 처리기) {
        verificēt_numurs(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void izlaist_Krātuve(int INDEX) {
        verificēt_numurs(INDEX);
        처리기들[INDEX] = null;
    }

    public int izplatīt_VALUE(int INDEX, int 저장된쌓임주소) {
        verificēt_numurs(INDEX);
        if (!Aktīvs) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Process_VALUE_ievade(저장된쌓임주소);
    }

    public void ieslēgt() {
        Aktīvs = true;
    }

    public void deaktivizēt() {
        Aktīvs = false;
    }

    public boolean informācijas_tehnoloģija_Aktīvs() {
        return Aktīvs;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void verificēt_numurs(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

