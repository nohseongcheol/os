// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ucraina.JUkrOS.dispozitiv_de_stocare;

import java.util.Arrays;

/** ATA 28비트 Comandă 계층과 같은 512바이트 논리 secțiune_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int secțiune_dimensiona = 512;
    private final byte[] date;
    private final boolean doar_în_citire_VALUE;

    public 고급기술결합장치(int secțiune_COUNT, boolean doar_în_citire_VALUE) {
        if (secțiune_COUNT <= 0) {
            throw new IllegalArgumentException("secțiune_VALUE 수가 올바르지 않습니다.");
        }
        date = new byte[Math.multiplyExact(secțiune_COUNT, secțiune_dimensiona)];
        this.doar_în_citire_VALUE = doar_în_citire_VALUE;
    }

    public int secțiune_COUNT() {
        return date.length / secțiune_dimensiona;
    }

    public void Citire(int secțiune_INDEX, byte[] primi_destinație) {
        verifica_zonă(secțiune_INDEX, primi_destinație);
        System.arraycopy(date, secțiune_INDEX * secțiune_dimensiona, primi_destinație, 0, secțiune_dimensiona);
    }

    public void Scriere(int secțiune_INDEX, byte[] 쓸자료) {
        if (doar_în_citire_VALUE) {
            throw new IllegalStateException("Citire 전용 장치입니다.");
        }
        verifica_zonă(secțiune_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, date, secțiune_INDEX * secțiune_dimensiona, secțiune_dimensiona);
    }

    public void șterge_intrare() {
        if (doar_în_citire_VALUE) {
            throw new IllegalStateException("Citire 전용 장치입니다.");
        }
        Arrays.fill(date, (byte) 0);
    }

    private void verifica_zonă(int secțiune_INDEX, byte[] 임시공간) {
        if (secțiune_INDEX < 0 || secțiune_INDEX >= secțiune_COUNT() || 임시공간.length < secțiune_dimensiona) {
            throw new IllegalArgumentException("ATA secțiune_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

