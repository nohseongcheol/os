// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ತಡೆಗಟ್ಟು;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ತಡೆಗಟ್ಟು_ವ್ಯವಸ್ಥಾಪಕ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ಲಭ್ಯ;

    public void ನೋಂದಾಯಿಸು_ನಮೂದು(int ಪದಸೂಚಿ, 개입중단처리기 처리기) {
        번호확인(ಪದಸೂಚಿ);
        처리기들[ಪದಸೂಚಿ] = 처리기;
    }

    public void ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ(int ಪದಸೂಚಿ) {
        번호확인(ಪದಸೂಚಿ);
        처리기들[ಪದಸೂಚಿ] = null;
    }

    public int ವಿತರಿಸು_ಮೌಲ್ಯ(int ಪದಸೂಚಿ, int 저장된쌓임주소) {
        번호확인(ಪದಸೂಚಿ);
        if (!ಲಭ್ಯ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ಪದಸೂಚಿ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು(저장된쌓임주소);
    }

    public void ಆನ್_ಮಾಡು() {
        ಲಭ್ಯ = true;
    }

    public void ನಿಷ್ಕ್ರಿಯಗೊಳಿಸಿ() {
        ಲಭ್ಯ = false;
    }

    public boolean ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಲಭ್ಯ() {
        return ಲಭ್ಯ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ಪದಸೂಚಿ) {
        if (ಪದಸೂಚಿ < 0 || ಪದಸೂಚಿ >= 처리기들.length) {
            throw new IllegalArgumentException("ತಡೆಗಟ್ಟು 번호가 올바르지 않습니다.");
        }
    }
}

