// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.lagringsenhet;

import java.util.Arrays;

/** ATA 28비트 Kommando 계층과 같은 512바이트 논리 inndeling_VERDI 장치다. */
public final class 고급기술결합장치 {
    public static final int inndeling_skalere = 512;
    private final byte[] data;
    private final boolean skrivebeskyttet_VERDI;

    public 고급기술결합장치(int inndeling_ANTALL, boolean skrivebeskyttet_VERDI) {
        if (inndeling_ANTALL <= 0) {
            throw new IllegalArgumentException("inndeling_VERDI 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(inndeling_ANTALL, inndeling_skalere)];
        this.skrivebeskyttet_VERDI = skrivebeskyttet_VERDI;
    }

    public int inndeling_ANTALL() {
        return data.length / inndeling_skalere;
    }

    public void Les(int inndeling_INDEKS, byte[] motta_mål) {
        sjekk_område(inndeling_INDEKS, motta_mål);
        System.arraycopy(data, inndeling_INDEKS * inndeling_skalere, motta_mål, 0, inndeling_skalere);
    }

    public void Skriv(int inndeling_INDEKS, byte[] 쓸자료) {
        if (skrivebeskyttet_VERDI) {
            throw new IllegalStateException("Les 전용 장치입니다.");
        }
        sjekk_område(inndeling_INDEKS, 쓸자료);
        System.arraycopy(쓸자료, 0, data, inndeling_INDEKS * inndeling_skalere, inndeling_skalere);
    }

    public void slette_oppføring() {
        if (skrivebeskyttet_VERDI) {
            throw new IllegalStateException("Les 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void sjekk_område(int inndeling_INDEKS, byte[] 임시공간) {
        if (inndeling_INDEKS < 0 || inndeling_INDEKS >= inndeling_ANTALL() || 임시공간.length < inndeling_skalere) {
            throw new IllegalArgumentException("ATA inndeling_VERDI 범위가 올바르지 않습니다.");
        }
    }
}

