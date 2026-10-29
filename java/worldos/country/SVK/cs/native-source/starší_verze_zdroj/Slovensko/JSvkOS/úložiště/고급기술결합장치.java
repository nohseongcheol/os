// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.úložiště;

import java.util.Arrays;

/** ATA 28비트 příkaz 계층과 같은 512바이트 논리 oddíl_HODNOTA_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int oddíl_změnit_velikost = 512;
    private final byte[] data;
    private final boolean jen_pro_čtení_HODNOTA;

    public 고급기술결합장치(int oddíl_POČET, boolean jen_pro_čtení_HODNOTA) {
        if (oddíl_POČET <= 0) {
            throw new IllegalArgumentException("oddíl_HODNOTA_366e0bfa 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(oddíl_POČET, oddíl_změnit_velikost)];
        this.jen_pro_čtení_HODNOTA = jen_pro_čtení_HODNOTA;
    }

    public int oddíl_POČET() {
        return data.length / oddíl_změnit_velikost;
    }

    public void Čtení(int oddíl_INDEX, byte[] dostat_cíl) {
        šek_oblast(oddíl_INDEX, dostat_cíl);
        System.arraycopy(data, oddíl_INDEX * oddíl_změnit_velikost, dostat_cíl, 0, oddíl_změnit_velikost);
    }

    public void Zápis(int oddíl_INDEX, byte[] 쓸자료) {
        if (jen_pro_čtení_HODNOTA) {
            throw new IllegalStateException("Čtení 전용 장치입니다.");
        }
        šek_oblast(oddíl_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, oddíl_INDEX * oddíl_změnit_velikost, oddíl_změnit_velikost);
    }

    public void vymazat_položka() {
        if (jen_pro_čtení_HODNOTA) {
            throw new IllegalStateException("Čtení 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void šek_oblast(int oddíl_INDEX, byte[] 임시공간) {
        if (oddíl_INDEX < 0 || oddíl_INDEX >= oddíl_POČET() || 임시공간.length < oddíl_změnit_velikost) {
            throw new IllegalArgumentException("ATA oddíl_HODNOTA_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

