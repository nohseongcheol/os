// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.Ħażna_mowbajl;

import java.util.Arrays;

/** ATA 28비트 kmand 계층과 같은 512바이트 논리 taqsima_VALUE_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int taqsima_daqqas = 512;
    private final byte[] data;
    private final boolean qari_biss_VALUE;

    public 고급기술결합장치(int taqsima_COUNT, boolean qari_biss_VALUE) {
        if (taqsima_COUNT <= 0) {
            throw new IllegalArgumentException("taqsima_VALUE_366e0bfa 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(taqsima_COUNT, taqsima_daqqas)];
        this.qari_biss_VALUE = qari_biss_VALUE;
    }

    public int taqsima_COUNT() {
        return data.length / taqsima_daqqas;
    }

    public void 읽기(int taqsima_INDEX, byte[] 받을곳) {
        범위확인(taqsima_INDEX, 받을곳);
        System.arraycopy(data, taqsima_INDEX * taqsima_daqqas, 받을곳, 0, taqsima_daqqas);
    }

    public void kiteb(int taqsima_INDEX, byte[] 쓸자료) {
        if (qari_biss_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(taqsima_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, taqsima_INDEX * taqsima_daqqas, taqsima_daqqas);
    }

    public void 지우기() {
        if (qari_biss_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int taqsima_INDEX, byte[] 임시공간) {
        if (taqsima_INDEX < 0 || taqsima_INDEX >= taqsima_COUNT() || 임시공간.length < taqsima_daqqas) {
            throw new IllegalArgumentException("ATA taqsima_VALUE_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

