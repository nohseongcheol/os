// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.Yaddaş_cihaz;

import java.util.Arrays;

/** ATA 28비트 Əmr 계층과 같은 512바이트 논리 bölmə_VALUE_366e0bfa 장치다. */
public final class 고급기술결합장치 {
    public static final int bölmə_ölçünü_dəyişmək = 512;
    private final byte[] verilənlər;
    private final boolean yalnız_oxunan_VALUE;

    public 고급기술결합장치(int bölmə_COUNT, boolean yalnız_oxunan_VALUE) {
        if (bölmə_COUNT <= 0) {
            throw new IllegalArgumentException("bölmə_VALUE_366e0bfa 수가 올바르지 않습니다.");
        }
        verilənlər = new byte[Math.multiplyExact(bölmə_COUNT, bölmə_ölçünü_dəyişmək)];
        this.yalnız_oxunan_VALUE = yalnız_oxunan_VALUE;
    }

    public int bölmə_COUNT() {
        return verilənlər.length / bölmə_ölçünü_dəyişmək;
    }

    public void Oxuma(int bölmə_INDEX, byte[] 받을곳) {
        범위확인(bölmə_INDEX, 받을곳);
        System.arraycopy(verilənlər, bölmə_INDEX * bölmə_ölçünü_dəyişmək, 받을곳, 0, bölmə_ölçünü_dəyişmək);
    }

    public void Yazma(int bölmə_INDEX, byte[] 쓸자료) {
        if (yalnız_oxunan_VALUE) {
            throw new IllegalStateException("Oxuma 전용 장치입니다.");
        }
        범위확인(bölmə_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, verilənlər, bölmə_INDEX * bölmə_ölçünü_dəyişmək, bölmə_ölçünü_dəyişmək);
    }

    public void silmək_daxiletmə_c8dbc399() {
        if (yalnız_oxunan_VALUE) {
            throw new IllegalStateException("Oxuma 전용 장치입니다.");
        }
        Arrays.fill(verilənlər, (byte) 0);
    }

    private void 범위확인(int bölmə_INDEX, byte[] 임시공간) {
        if (bölmə_INDEX < 0 || bölmə_INDEX >= bölmə_COUNT() || 임시공간.length < bölmə_ölçünü_dəyişmək) {
            throw new IllegalArgumentException("ATA bölmə_VALUE_366e0bfa 범위가 올바르지 않습니다.");
        }
    }
}

