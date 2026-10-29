// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class IRQ_njikwa {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean kèdịìrè;

    public void 등록(int indèks, 개입중단처리기 처리기) {
        번호확인(indèks);
        처리기들[indèks] = 처리기;
    }

    public void bupute_Nchekwa(int indèks) {
        번호확인(indèks);
        처리기들[indèks] = null;
    }

    public int kesaa_valuu(int indèks, int 저장된쌓임주소) {
        번호확인(indèks);
        if (!kèdịìrè) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[indèks];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ùsòrò_valuu_ndebà(저장된쌓임주소);
    }

    public void gbanye() {
        kèdịìrè = true;
    }

    public void mwepụ̀_ike() {
        kèdịìrè = false;
    }

    public boolean 활성인가() {
        return kèdịìrè;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int indèks) {
        if (indèks < 0 || indèks >= 처리기들.length) {
            throw new IllegalArgumentException("IRQ 번호가 올바르지 않습니다.");
        }
    }
}

