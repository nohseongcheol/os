// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.salvesti;

import java.util.Arrays;

/** ATA 28비트 Käsk 계층과 같은 512바이트 논리 jaotis_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int jaotis_suurust_muutma = 512;
    private final byte[] andmed;
    private final boolean kirjutuskaitstud_VALUE;

    public 고급기술결합장치(int jaotis_COUNT, boolean kirjutuskaitstud_VALUE) {
        if (jaotis_COUNT <= 0) {
            throw new IllegalArgumentException("jaotis_VALUE 수가 올바르지 않습니다.");
        }
        andmed = new byte[Math.multiplyExact(jaotis_COUNT, jaotis_suurust_muutma)];
        this.kirjutuskaitstud_VALUE = kirjutuskaitstud_VALUE;
    }

    public int jaotis_COUNT() {
        return andmed.length / jaotis_suurust_muutma;
    }

    public void Lugemine(int jaotis_INDEX, byte[] saama_sihtkoht) {
        tšekk_vahemik(jaotis_INDEX, saama_sihtkoht);
        System.arraycopy(andmed, jaotis_INDEX * jaotis_suurust_muutma, saama_sihtkoht, 0, jaotis_suurust_muutma);
    }

    public void Kirjutamine(int jaotis_INDEX, byte[] 쓸자료) {
        if (kirjutuskaitstud_VALUE) {
            throw new IllegalStateException("Lugemine 전용 장치입니다.");
        }
        tšekk_vahemik(jaotis_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, andmed, jaotis_INDEX * jaotis_suurust_muutma, jaotis_suurust_muutma);
    }

    public void kustutama_kirje() {
        if (kirjutuskaitstud_VALUE) {
            throw new IllegalStateException("Lugemine 전용 장치입니다.");
        }
        Arrays.fill(andmed, (byte) 0);
    }

    private void tšekk_vahemik(int jaotis_INDEX, byte[] 임시공간) {
        if (jaotis_INDEX < 0 || jaotis_INDEX >= jaotis_COUNT() || 임시공간.length < jaotis_suurust_muutma) {
            throw new IllegalArgumentException("ATA jaotis_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

