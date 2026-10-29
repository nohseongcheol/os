// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.tallennuslaite;

import java.util.Arrays;

/** ATA 28비트 komento 계층과 같은 512바이트 논리 osa_ARVO 장치다. */
public final class 고급기술결합장치 {
    public static final int osa_muuttaa_kokoa = 512;
    private final byte[] data;
    private final boolean vain_luku_ARVO;

    public 고급기술결합장치(int osa_LASKE, boolean vain_luku_ARVO) {
        if (osa_LASKE <= 0) {
            throw new IllegalArgumentException("osa_ARVO 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(osa_LASKE, osa_muuttaa_kokoa)];
        this.vain_luku_ARVO = vain_luku_ARVO;
    }

    public int osa_LASKE() {
        return data.length / osa_muuttaa_kokoa;
    }

    public void Luku(int osa_INDEKSI, byte[] saada_kohde) {
        sekki_alue(osa_INDEKSI, saada_kohde);
        System.arraycopy(data, osa_INDEKSI * osa_muuttaa_kokoa, saada_kohde, 0, osa_muuttaa_kokoa);
    }

    public void Kirjoitus(int osa_INDEKSI, byte[] 쓸자료) {
        if (vain_luku_ARVO) {
            throw new IllegalStateException("Luku 전용 장치입니다.");
        }
        sekki_alue(osa_INDEKSI, 쓸자료);
        System.arraycopy(쓸자료, 0, data, osa_INDEKSI * osa_muuttaa_kokoa, osa_muuttaa_kokoa);
    }

    public void poistaa_merkintä_c8dbc399() {
        if (vain_luku_ARVO) {
            throw new IllegalStateException("Luku 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void sekki_alue(int osa_INDEKSI, byte[] 임시공간) {
        if (osa_INDEKSI < 0 || osa_INDEKSI >= osa_LASKE() || 임시공간.length < osa_muuttaa_kokoa) {
            throw new IllegalArgumentException("ATA osa_ARVO 범위가 올바르지 않습니다.");
        }
    }
}

