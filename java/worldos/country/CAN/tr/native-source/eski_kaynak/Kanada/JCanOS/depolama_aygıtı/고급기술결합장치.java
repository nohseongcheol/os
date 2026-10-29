// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.depolama_aygıtı;

import java.util.Arrays;

/** ATA 28비트 komut 계층과 같은 512바이트 논리 bölüm_değer_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int bölüm_boyutlandırmak = 512;
    private final byte[] veri;
    private final boolean salt_okunur_değer;

    public 고급기술결합장치(int bölüm_BAĞ_DEĞ_SAY, boolean salt_okunur_değer) {
        if (bölüm_BAĞ_DEĞ_SAY <= 0) {
            throw new IllegalArgumentException("bölüm_değer_366e0bfa 수가 올바르지 않습니다.");
        }
        veri = new byte[Math.multiplyExact(bölüm_BAĞ_DEĞ_SAY, bölüm_boyutlandırmak)];
        this.salt_okunur_değer = salt_okunur_değer;
    }

    public int bölüm_BAĞ_DEĞ_SAY() {
        return veri.length / bölüm_boyutlandırmak;
    }

    public void Okuma(int bölüm_Dizin, byte[] almak_hedef) {
        çek_aralık(bölüm_Dizin, almak_hedef);
        System.arraycopy(veri, bölüm_Dizin * bölüm_boyutlandırmak, almak_hedef, 0, bölüm_boyutlandırmak);
    }

    public void Yazma(int bölüm_Dizin, byte[] 쓸자료) {
        if (salt_okunur_değer) {
            throw new IllegalStateException("Okuma 전용 장치입니다.");
        }
        çek_aralık(bölüm_Dizin, 쓸자료);
        System.arraycopy(쓸자료, 0, veri, bölüm_Dizin * bölüm_boyutlandırmak, bölüm_boyutlandırmak);
    }

    public void silmek_girdi() {
        if (salt_okunur_değer) {
            throw new IllegalStateException("Okuma 전용 장치입니다.");
        }
        Arrays.fill(veri, (byte) 0);
    }

    private void çek_aralık(int bölüm_Dizin, byte[] 임시공간) {
        if (bölüm_Dizin < 0 || bölüm_Dizin >= bölüm_BAĞ_DEĞ_SAY() || 임시공간.length < bölüm_boyutlandırmak) {
            throw new IllegalArgumentException("ATA bölüm_değer_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

