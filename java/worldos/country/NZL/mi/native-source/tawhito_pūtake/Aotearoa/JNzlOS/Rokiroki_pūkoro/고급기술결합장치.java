// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.Rokiroki_pūkoro;

import java.util.Arrays;

/** ATA 28비트 tono 계층과 같은 512바이트 논리 wāhanga_uara 장치다. */
public final class 고급기술결합장치 {
    public static final int wāhanga_rahi = 512;
    private final byte[] raraunga;
    private final boolean pānui_anake_uara;

    public 고급기술결합장치(int wāhanga_COUNT, boolean pānui_anake_uara) {
        if (wāhanga_COUNT <= 0) {
            throw new IllegalArgumentException("wāhanga_uara 수가 올바르지 않습니다.");
        }
        raraunga = new byte[Math.multiplyExact(wāhanga_COUNT, wāhanga_rahi)];
        this.pānui_anake_uara = pānui_anake_uara;
    }

    public int wāhanga_COUNT() {
        return raraunga.length / wāhanga_rahi;
    }

    public void Pānuitia(int wāhanga_INDEX, byte[] 받을곳) {
        범위확인(wāhanga_INDEX, 받을곳);
        System.arraycopy(raraunga, wāhanga_INDEX * wāhanga_rahi, 받을곳, 0, wāhanga_rahi);
    }

    public void Tuhia(int wāhanga_INDEX, byte[] 쓸자료) {
        if (pānui_anake_uara) {
            throw new IllegalStateException("Pānuitia 전용 장치입니다.");
        }
        범위확인(wāhanga_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, raraunga, wāhanga_INDEX * wāhanga_rahi, wāhanga_rahi);
    }

    public void 지우기() {
        if (pānui_anake_uara) {
            throw new IllegalStateException("Pānuitia 전용 장치입니다.");
        }
        Arrays.fill(raraunga, (byte) 0);
    }

    private void 범위확인(int wāhanga_INDEX, byte[] 임시공간) {
        if (wāhanga_INDEX < 0 || wāhanga_INDEX >= wāhanga_COUNT() || 임시공간.length < wāhanga_rahi) {
            throw new IllegalArgumentException("ATA wāhanga_uara 범위가 올바르지 않습니다.");
        }
    }
}

