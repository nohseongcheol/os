// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.Ammar_enjam;

import java.util.Arrays;

/** ATA 28비트 buýruk 계층과 같은 512바이트 논리 bölüm_baha_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int bölüm_ölçegi_üýtget = 512;
    private final byte[] maglumat;
    private final boolean diňe_okalýan_baha;

    public 고급기술결합장치(int 구역수, boolean diňe_okalýan_baha) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("bölüm_baha_366e0bfa 수가 올바르지 않습니다.");
        }
        maglumat = new byte[Math.multiplyExact(구역수, bölüm_ölçegi_üýtget)];
        this.diňe_okalýan_baha = diňe_okalýan_baha;
    }

    public int 구역수() {
        return maglumat.length / bölüm_ölçegi_üýtget;
    }

    public void Oka(int bölüm_indeks, byte[] 받을곳) {
        범위확인(bölüm_indeks, 받을곳);
        System.arraycopy(maglumat, bölüm_indeks * bölüm_ölçegi_üýtget, 받을곳, 0, bölüm_ölçegi_üýtget);
    }

    public void Ýaz(int bölüm_indeks, byte[] 쓸자료) {
        if (diňe_okalýan_baha) {
            throw new IllegalStateException("Oka 전용 장치입니다.");
        }
        범위확인(bölüm_indeks, 쓸자료);
        System.arraycopy(쓸자료, 0, maglumat, bölüm_indeks * bölüm_ölçegi_üýtget, bölüm_ölçegi_üýtget);
    }

    public void 지우기() {
        if (diňe_okalýan_baha) {
            throw new IllegalStateException("Oka 전용 장치입니다.");
        }
        Arrays.fill(maglumat, (byte) 0);
    }

    private void 범위확인(int bölüm_indeks, byte[] 임시공간) {
        if (bölüm_indeks < 0 || bölüm_indeks >= 구역수() || 임시공간.length < bölüm_ölçegi_üýtget) {
            throw new IllegalArgumentException("ATA bölüm_baha_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

