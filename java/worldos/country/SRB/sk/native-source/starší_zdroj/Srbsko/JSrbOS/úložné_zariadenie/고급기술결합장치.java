// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbsko.JSrbOS.úložné_zariadenie;

import java.util.Arrays;

/** ATA 28비트 Príkaz 계층과 같은 512바이트 논리 sekcia_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int sekcia_zmeniť_veľkosť = 512;
    private final byte[] údaje;
    private final boolean iba_na_čítanie_VALUE;

    public 고급기술결합장치(int sekcia_COUNT, boolean iba_na_čítanie_VALUE) {
        if (sekcia_COUNT <= 0) {
            throw new IllegalArgumentException("sekcia_VALUE 수가 올바르지 않습니다.");
        }
        údaje = new byte[Math.multiplyExact(sekcia_COUNT, sekcia_zmeniť_veľkosť)];
        this.iba_na_čítanie_VALUE = iba_na_čítanie_VALUE;
    }

    public int sekcia_COUNT() {
        return údaje.length / sekcia_zmeniť_veľkosť;
    }

    public void Čítanie(int sekcia_INDEX, byte[] dostať_cieľ) {
        skontrolovať_rozsah(sekcia_INDEX, dostať_cieľ);
        System.arraycopy(údaje, sekcia_INDEX * sekcia_zmeniť_veľkosť, dostať_cieľ, 0, sekcia_zmeniť_veľkosť);
    }

    public void Zápis(int sekcia_INDEX, byte[] 쓸자료) {
        if (iba_na_čítanie_VALUE) {
            throw new IllegalStateException("Čítanie 전용 장치입니다.");
        }
        skontrolovať_rozsah(sekcia_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, údaje, sekcia_INDEX * sekcia_zmeniť_veľkosť, sekcia_zmeniť_veľkosť);
    }

    public void vymazať_položka() {
        if (iba_na_čítanie_VALUE) {
            throw new IllegalStateException("Čítanie 전용 장치입니다.");
        }
        Arrays.fill(údaje, (byte) 0);
    }

    private void skontrolovať_rozsah(int sekcia_INDEX, byte[] 임시공간) {
        if (sekcia_INDEX < 0 || sekcia_INDEX >= sekcia_COUNT() || 임시공간.length < sekcia_zmeniť_veľkosť) {
            throw new IllegalArgumentException("ATA sekcia_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

