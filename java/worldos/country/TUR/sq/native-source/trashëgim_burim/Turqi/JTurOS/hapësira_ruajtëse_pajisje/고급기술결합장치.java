// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.hapësira_ruajtëse_pajisje;

import java.util.Arrays;

/** ATA 28비트 Komanda 계층과 같은 512바이트 논리 seksion_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int seksion_ndryshoj_përmasat = 512;
    private final byte[] të_dhëna;
    private final boolean vetëm_për_lexim_VALUE;

    public 고급기술결합장치(int seksion_COUNT, boolean vetëm_për_lexim_VALUE) {
        if (seksion_COUNT <= 0) {
            throw new IllegalArgumentException("seksion_VALUE 수가 올바르지 않습니다.");
        }
        të_dhëna = new byte[Math.multiplyExact(seksion_COUNT, seksion_ndryshoj_përmasat)];
        this.vetëm_për_lexim_VALUE = vetëm_për_lexim_VALUE;
    }

    public int seksion_COUNT() {
        return të_dhëna.length / seksion_ndryshoj_përmasat;
    }

    public void Leximi(int seksion_INDEX, byte[] 받을곳) {
        범위확인(seksion_INDEX, 받을곳);
        System.arraycopy(të_dhëna, seksion_INDEX * seksion_ndryshoj_përmasat, 받을곳, 0, seksion_ndryshoj_përmasat);
    }

    public void Shkrimi(int seksion_INDEX, byte[] 쓸자료) {
        if (vetëm_për_lexim_VALUE) {
            throw new IllegalStateException("Leximi 전용 장치입니다.");
        }
        범위확인(seksion_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, të_dhëna, seksion_INDEX * seksion_ndryshoj_përmasat, seksion_ndryshoj_përmasat);
    }

    public void spastroj_futje() {
        if (vetëm_për_lexim_VALUE) {
            throw new IllegalStateException("Leximi 전용 장치입니다.");
        }
        Arrays.fill(të_dhëna, (byte) 0);
    }

    private void 범위확인(int seksion_INDEX, byte[] 임시공간) {
        if (seksion_INDEX < 0 || seksion_INDEX >= seksion_COUNT() || 임시공간.length < seksion_ndryshoj_përmasat) {
            throw new IllegalArgumentException("ATA seksion_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

