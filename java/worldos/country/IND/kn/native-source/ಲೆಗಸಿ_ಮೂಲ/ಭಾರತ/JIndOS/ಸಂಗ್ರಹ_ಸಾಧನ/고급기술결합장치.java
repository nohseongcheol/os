// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಸಂಗ್ರಹ_ಸಾಧನ;

import java.util.Arrays;

/** ATA 28비트 ಆಜ್ಞೆ 계층과 같은 512바이트 논리 ವಿಭಾಗ_ಮೌಲ್ಯ 장치다. */
public final class 고급기술결합장치 {
    public static final int ವಿಭಾಗ_ಗಾತ್ರಿಸು = 512;
    private final byte[] ಡೇಟಾ;
    private final boolean ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ;

    public 고급기술결합장치(int 구역수, boolean ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ವಿಭಾಗ_ಮೌಲ್ಯ 수가 올바르지 않습니다.");
        }
        ಡೇಟಾ = new byte[Math.multiplyExact(구역수, ವಿಭಾಗ_ಗಾತ್ರಿಸು)];
        this.ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ = ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ;
    }

    public int 구역수() {
        return ಡೇಟಾ.length / ವಿಭಾಗ_ಗಾತ್ರಿಸು;
    }

    public void ಓದು(int ವಿಭಾಗ_ಪದಸೂಚಿ, byte[] 받을곳) {
        범위확인(ವಿಭಾಗ_ಪದಸೂಚಿ, 받을곳);
        System.arraycopy(ಡೇಟಾ, ವಿಭಾಗ_ಪದಸೂಚಿ * ವಿಭಾಗ_ಗಾತ್ರಿಸು, 받을곳, 0, ವಿಭಾಗ_ಗಾತ್ರಿಸು);
    }

    public void ಬರೆ(int ವಿಭಾಗ_ಪದಸೂಚಿ, byte[] 쓸자료) {
        if (ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ) {
            throw new IllegalStateException("ಓದು 전용 장치입니다.");
        }
        범위확인(ವಿಭಾಗ_ಪದಸೂಚಿ, 쓸자료);
        System.arraycopy(쓸자료, 0, ಡೇಟಾ, ವಿಭಾಗ_ಪದಸೂಚಿ * ವಿಭಾಗ_ಗಾತ್ರಿಸು, ವಿಭಾಗ_ಗಾತ್ರಿಸು);
    }

    public void ಅಳಿಸು_ನಮೂದು() {
        if (ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ) {
            throw new IllegalStateException("ಓದು 전용 장치입니다.");
        }
        Arrays.fill(ಡೇಟಾ, (byte) 0);
    }

    private void 범위확인(int ವಿಭಾಗ_ಪದಸೂಚಿ, byte[] 임시공간) {
        if (ವಿಭಾಗ_ಪದಸೂಚಿ < 0 || ವಿಭಾಗ_ಪದಸೂಚಿ >= 구역수() || 임시공간.length < ವಿಭಾಗ_ಗಾತ್ರಿಸು) {
            throw new IllegalArgumentException("ATA ವಿಭಾಗ_ಮೌಲ್ಯ 범위가 올바르지 않습니다.");
        }
    }
}

