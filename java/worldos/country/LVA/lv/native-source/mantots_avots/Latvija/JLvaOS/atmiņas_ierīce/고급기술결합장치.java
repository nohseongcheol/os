// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.atmiņas_ierīce;

import java.util.Arrays;

/** ATA 28비트 Komanda 계층과 같은 512바이트 논리 sadaļa_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int sadaļa_mainīt_izmērus = 512;
    private final byte[] dati;
    private final boolean tikai_lasāms_VALUE;

    public 고급기술결합장치(int sadaļa_COUNT, boolean tikai_lasāms_VALUE) {
        if (sadaļa_COUNT <= 0) {
            throw new IllegalArgumentException("sadaļa_VALUE 수가 올바르지 않습니다.");
        }
        dati = new byte[Math.multiplyExact(sadaļa_COUNT, sadaļa_mainīt_izmērus)];
        this.tikai_lasāms_VALUE = tikai_lasāms_VALUE;
    }

    public int sadaļa_COUNT() {
        return dati.length / sadaļa_mainīt_izmērus;
    }

    public void Lasīt(int sadaļa_INDEX, byte[] saņemt_mērķis) {
        čeks_diapazons(sadaļa_INDEX, saņemt_mērķis);
        System.arraycopy(dati, sadaļa_INDEX * sadaļa_mainīt_izmērus, saņemt_mērķis, 0, sadaļa_mainīt_izmērus);
    }

    public void Rakstīt(int sadaļa_INDEX, byte[] 쓸자료) {
        if (tikai_lasāms_VALUE) {
            throw new IllegalStateException("Lasīt 전용 장치입니다.");
        }
        čeks_diapazons(sadaļa_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, dati, sadaļa_INDEX * sadaļa_mainīt_izmērus, sadaļa_mainīt_izmērus);
    }

    public void dzēst_ievade() {
        if (tikai_lasāms_VALUE) {
            throw new IllegalStateException("Lasīt 전용 장치입니다.");
        }
        Arrays.fill(dati, (byte) 0);
    }

    private void čeks_diapazons(int sadaļa_INDEX, byte[] 임시공간) {
        if (sadaļa_INDEX < 0 || sadaļa_INDEX >= sadaļa_COUNT() || 임시공간.length < sadaļa_mainīt_izmērus) {
            throw new IllegalArgumentException("ATA sadaļa_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

