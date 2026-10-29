// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brunei.JBrnOS.Storan_peranti;

import java.util.Arrays;

/** ATA 28비트 Perintah 계층과 같은 512바이트 논리 seksyen_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int seksyen_saiz = 512;
    private final byte[] data;
    private final boolean baca_sahaja_VALUE;

    public 고급기술결합장치(int seksyen_COUNT, boolean baca_sahaja_VALUE) {
        if (seksyen_COUNT <= 0) {
            throw new IllegalArgumentException("seksyen_VALUE 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(seksyen_COUNT, seksyen_saiz)];
        this.baca_sahaja_VALUE = baca_sahaja_VALUE;
    }

    public int seksyen_COUNT() {
        return data.length / seksyen_saiz;
    }

    public void Baca(int seksyen_INDEX, byte[] 받을곳) {
        cek_julat(seksyen_INDEX, 받을곳);
        System.arraycopy(data, seksyen_INDEX * seksyen_saiz, 받을곳, 0, seksyen_saiz);
    }

    public void Tulis(int seksyen_INDEX, byte[] 쓸자료) {
        if (baca_sahaja_VALUE) {
            throw new IllegalStateException("Baca 전용 장치입니다.");
        }
        cek_julat(seksyen_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, data, seksyen_INDEX * seksyen_saiz, seksyen_saiz);
    }

    public void padam_pemasukan() {
        if (baca_sahaja_VALUE) {
            throw new IllegalStateException("Baca 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void cek_julat(int seksyen_INDEX, byte[] 임시공간) {
        if (seksyen_INDEX < 0 || seksyen_INDEX >= seksyen_COUNT() || 임시공간.length < seksyen_saiz) {
            throw new IllegalArgumentException("ATA seksyen_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

