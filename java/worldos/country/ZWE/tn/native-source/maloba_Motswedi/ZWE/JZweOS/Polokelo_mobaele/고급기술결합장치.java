// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ZWE.JZweOS.Polokelo_mobaele;

import java.util.Arrays;

/** ATA 28비트 Taelo 계층과 같은 512바이트 논리 karolo_Boleng 장치다. */
public final class 고급기술결합장치 {
    public static final int karolo_lekanya = 512;
    private final byte[] tshedimosetso;
    private final boolean puiso_fela_Boleng;

    public 고급기술결합장치(int 구역수, boolean puiso_fela_Boleng) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("karolo_Boleng 수가 올바르지 않습니다.");
        }
        tshedimosetso = new byte[Math.multiplyExact(구역수, karolo_lekanya)];
        this.puiso_fela_Boleng = puiso_fela_Boleng;
    }

    public int 구역수() {
        return tshedimosetso.length / karolo_lekanya;
    }

    public void 읽기(int karolo_tshupane, byte[] 받을곳) {
        범위확인(karolo_tshupane, 받을곳);
        System.arraycopy(tshedimosetso, karolo_tshupane * karolo_lekanya, 받을곳, 0, karolo_lekanya);
    }

    public void kwala(int karolo_tshupane, byte[] 쓸자료) {
        if (puiso_fela_Boleng) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(karolo_tshupane, 쓸자료);
        System.arraycopy(쓸자료, 0, tshedimosetso, karolo_tshupane * karolo_lekanya, karolo_lekanya);
    }

    public void 지우기() {
        if (puiso_fela_Boleng) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(tshedimosetso, (byte) 0);
    }

    private void 범위확인(int karolo_tshupane, byte[] 임시공간) {
        if (karolo_tshupane < 0 || karolo_tshupane >= 구역수() || 임시공간.length < karolo_lekanya) {
            throw new IllegalArgumentException("ATA karolo_Boleng 범위가 올바르지 않습니다.");
        }
    }
}

