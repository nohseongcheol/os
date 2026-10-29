// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_Umugenzuzi {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ifunguye;

    public void 등록(int umugerekashakiro, 개입중단처리기 처리기) {
        번호확인(umugerekashakiro);
        처리기들[umugerekashakiro] = 처리기;
    }

    public void kurekura_Ububiko(int umugerekashakiro) {
        번호확인(umugerekashakiro);
        처리기들[umugerekashakiro] = null;
    }

    public int gucuruza_agaciro(int umugerekashakiro, int 저장된쌓임주소) {
        번호확인(umugerekashakiro);
        if (!ifunguye) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[umugerekashakiro];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Inzira_agaciro_icyinjizwa(저장된쌓임주소);
    }

    public void gufungura() {
        ifunguye = true;
    }

    public void gufunga() {
        ifunguye = false;
    }

    public boolean 활성인가() {
        return ifunguye;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int umugerekashakiro) {
        if (umugerekashakiro < 0 || umugerekashakiro >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

