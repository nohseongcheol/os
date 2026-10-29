// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.naprava_za_shranjevanje;

import java.util.Arrays;

/** ATA 28비트 Ukaz 계층과 같은 512바이트 논리 odsek_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int odsek_spremeniti_velikost = 512;
    private final byte[] podatki;
    private final boolean samo_za_branje_VALUE;

    public 고급기술결합장치(int odsek_COUNT, boolean samo_za_branje_VALUE) {
        if (odsek_COUNT <= 0) {
            throw new IllegalArgumentException("odsek_VALUE 수가 올바르지 않습니다.");
        }
        podatki = new byte[Math.multiplyExact(odsek_COUNT, odsek_spremeniti_velikost)];
        this.samo_za_branje_VALUE = samo_za_branje_VALUE;
    }

    public int odsek_COUNT() {
        return podatki.length / odsek_spremeniti_velikost;
    }

    public void Branje(int odsek_INDEX, byte[] sprejeti_sprejemati_prejeti_prejemati_cilj) {
        preveriti_obseg(odsek_INDEX, sprejeti_sprejemati_prejeti_prejemati_cilj);
        System.arraycopy(podatki, odsek_INDEX * odsek_spremeniti_velikost, sprejeti_sprejemati_prejeti_prejemati_cilj, 0, odsek_spremeniti_velikost);
    }

    public void Pisanje(int odsek_INDEX, byte[] 쓸자료) {
        if (samo_za_branje_VALUE) {
            throw new IllegalStateException("Branje 전용 장치입니다.");
        }
        preveriti_obseg(odsek_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, podatki, odsek_INDEX * odsek_spremeniti_velikost, odsek_spremeniti_velikost);
    }

    public void izbrisati_vnos() {
        if (samo_za_branje_VALUE) {
            throw new IllegalStateException("Branje 전용 장치입니다.");
        }
        Arrays.fill(podatki, (byte) 0);
    }

    private void preveriti_obseg(int odsek_INDEX, byte[] 임시공간) {
        if (odsek_INDEX < 0 || odsek_INDEX >= odsek_COUNT() || 임시공간.length < odsek_spremeniti_velikost) {
            throw new IllegalArgumentException("ATA odsek_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

