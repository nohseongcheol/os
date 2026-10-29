// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.aapiriaaipa;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean a_yataasü;

    public void 등록(int ee_iyatialujuna, 개입중단처리기 처리기) {
        번호확인(ee_iyatialujuna);
        처리기들[ee_iyatialujuna] = 처리기;
    }

    public void 해제(int ee_iyatialujuna) {
        번호확인(ee_iyatialujuna);
        처리기들[ee_iyatialujuna] = null;
    }

    public int 분배(int ee_iyatialujuna, int 저장된쌓임주소) {
        번호확인(ee_iyatialujuna);
        if (!a_yataasü) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ee_iyatialujuna];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.처리(저장된쌓임주소);
    }

    public void 활성화() {
        a_yataasü = true;
    }

    public void 비활성화() {
        a_yataasü = false;
    }

    public boolean 활성인가() {
        return a_yataasü;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ee_iyatialujuna) {
        if (ee_iyatialujuna < 0 || ee_iyatialujuna >= 처리기들.length) {
            throw new IllegalArgumentException("aapiriaaipa 번호가 올바르지 않습니다.");
        }
    }
}

