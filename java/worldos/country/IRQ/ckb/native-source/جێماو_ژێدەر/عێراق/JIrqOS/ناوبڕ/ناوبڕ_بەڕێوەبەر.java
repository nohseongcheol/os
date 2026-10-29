// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.ناوبڕ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ناوبڕ_بەڕێوەبەر {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean چالاک;

    public void 등록(int پێرست, 개입중단처리기 처리기) {
        번호확인(پێرست);
        처리기들[پێرست] = 처리기;
    }

    public void وەشان_هەمارگە(int پێرست) {
        번호확인(پێرست);
        처리기들[پێرست] = null;
    }

    public int دابەشكردن_نرخ(int پێرست, int 저장된쌓임주소) {
        번호확인(پێرست);
        if (!چالاک) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[پێرست];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.پرۆسە_نرخ_تێنووسین(저장된쌓임주소);
    }

    public void چالاک_کردن() {
        چالاک = true;
    }

    public void ناچالاك_كردن() {
        چالاک = false;
    }

    public boolean 활성인가() {
        return چالاک;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int پێرست) {
        if (پێرست < 0 || پێرست >= 처리기들.length) {
            throw new IllegalArgumentException("ناوبڕ 번호가 올바르지 않습니다.");
        }
    }
}

