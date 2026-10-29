// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.saugojimo_įrenginys;

import java.util.Arrays;

/** ATA 28비트 Komanda 계층과 같은 512바이트 논리 sekcija_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int sekcija_dydis = 512;
    private final byte[] duomenys;
    private final boolean tik_skaitomas_VALUE;

    public 고급기술결합장치(int sekcija_COUNT, boolean tik_skaitomas_VALUE) {
        if (sekcija_COUNT <= 0) {
            throw new IllegalArgumentException("sekcija_VALUE 수가 올바르지 않습니다.");
        }
        duomenys = new byte[Math.multiplyExact(sekcija_COUNT, sekcija_dydis)];
        this.tik_skaitomas_VALUE = tik_skaitomas_VALUE;
    }

    public int sekcija_COUNT() {
        return duomenys.length / sekcija_dydis;
    }

    public void Skaitymas(int sekcija_INDEX, byte[] gauti_vieta) {
        čekis_diapazonas(sekcija_INDEX, gauti_vieta);
        System.arraycopy(duomenys, sekcija_INDEX * sekcija_dydis, gauti_vieta, 0, sekcija_dydis);
    }

    public void Rašymas(int sekcija_INDEX, byte[] 쓸자료) {
        if (tik_skaitomas_VALUE) {
            throw new IllegalStateException("Skaitymas 전용 장치입니다.");
        }
        čekis_diapazonas(sekcija_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, duomenys, sekcija_INDEX * sekcija_dydis, sekcija_dydis);
    }

    public void ištrinti_įrašas() {
        if (tik_skaitomas_VALUE) {
            throw new IllegalStateException("Skaitymas 전용 장치입니다.");
        }
        Arrays.fill(duomenys, (byte) 0);
    }

    private void čekis_diapazonas(int sekcija_INDEX, byte[] 임시공간) {
        if (sekcija_INDEX < 0 || sekcija_INDEX >= sekcija_COUNT() || 임시공간.length < sekcija_dydis) {
            throw new IllegalArgumentException("ATA sekcija_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

