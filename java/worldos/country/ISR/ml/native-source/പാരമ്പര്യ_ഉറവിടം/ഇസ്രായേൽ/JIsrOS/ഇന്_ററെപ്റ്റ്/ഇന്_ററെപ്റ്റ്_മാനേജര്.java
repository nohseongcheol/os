// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ഇസ്രായേൽ.JIsrOS.ഇന്_ററെപ്റ്റ്;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ഇന്_ററെപ്റ്റ്_മാനേജര് {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean സജീവ;

    public void രജിസ്_റ്റർ_ചെയ്യുക_എന്_ട്രി(int സൂചിക, 개입중단처리기 처리기) {
        번호확인(സൂചിക);
        처리기들[സൂചിക] = 처리기;
    }

    public void റിലീസ്_സംഭരണം(int സൂചിക) {
        번호확인(സൂചിക);
        처리기들[സൂചിക] = null;
    }

    public int വിതരണം_ചെയ്യുക_മൂല്യം(int സൂചിക, int 저장된쌓임주소) {
        번호확인(സൂചിക);
        if (!സജീവ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[സൂചിക];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.പ്രോസസ്_മൂല്യം_എന്_ട്രി(저장된쌓임주소);
    }

    public void ഓൺ_ചെയ്യുക() {
        സജീവ = true;
    }

    public void നിർജ്ജീവമാക്കുക() {
        സജീവ = false;
    }

    public boolean വിവര_സാങ്കേതികവിദ്യ_സജീവ() {
        return സജീവ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int സൂചിക) {
        if (സൂചിക < 0 || സൂചിക >= 처리기들.length) {
            throw new IllegalArgumentException("ഇന്_ററെപ്റ്റ് 번호가 올바르지 않습니다.");
        }
    }
}

