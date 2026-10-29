// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_менаџер {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean активно;

    public void 등록(int индекс, 개입중단처리기 처리기) {
        번호확인(индекс);
        처리기들[индекс] = 처리기;
    }

    public void 해제(int индекс) {
        번호확인(индекс);
        처리기들[индекс] = null;
    }

    public int 분배(int индекс, int 저장된쌓임주소) {
        번호확인(индекс);
        if (!активно) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[индекс];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.процес_вриједност_унос(저장된쌓임주소);
    }

    public void укључити() {
        активно = true;
    }

    public void 비활성화() {
        активно = false;
    }

    public boolean 활성인가() {
        return активно;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int индекс) {
        if (индекс < 0 || индекс >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

