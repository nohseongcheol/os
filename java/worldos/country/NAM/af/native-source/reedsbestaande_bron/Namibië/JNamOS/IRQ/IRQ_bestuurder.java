// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_bestuurder {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Aktief;

    public void registreer_inskrywing(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void stel_vry_Berging(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int versprei_VALUE(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Aktief) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Proses_VALUE_inskrywing(저장된쌓임주소);
    }

    public void aktiveer() {
        Aktief = true;
    }

    public void deaktiveer() {
        Aktief = false;
    }

    public boolean 활성인가() {
        return Aktief;
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

