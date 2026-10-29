// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ermənistan.JArmOS.fayl_sistemi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standart_qiymət 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class bölmə_VALUE {
        private final int 종류;
        private final long Başla_bölmə;
        private final long bölmə_COUNT;

        bölmə_VALUE(int 종류, long Başla_bölmə, long bölmə_COUNT) {
            this.종류 = 종류;
            this.Başla_bölmə = Başla_bölmə;
            this.bölmə_COUNT = bölmə_COUNT;
        }

        public int 종류() { return 종류; }
        public long Başla_bölmə() { return Başla_bölmə; }
        public long bölmə_COUNT() { return bölmə_COUNT; }
    }

    public List<bölmə_VALUE> Oxuma(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<bölmə_VALUE> ölçü = new ArrayList<bölmə_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int yerinə_qoymaq = 446 + INDEX * 16;
            int 종류 = 첫구역[yerinə_qoymaq + 4] & 0xff;
            long İcra_Et = 작은순서정수(첫구역, yerinə_qoymaq + 8);
            long Böyüklük = 작은순서정수(첫구역, yerinə_qoymaq + 12);
            if (종류 != 0 && Böyüklük != 0) {
                ölçü.add(new bölmə_VALUE(종류, İcra_Et, Böyüklük));
            }
        }
        return Collections.unmodifiableList(ölçü);
    }

    private long 작은순서정수(byte[] verilənlər, int yerinə_qoymaq) {
        return (verilənlər[yerinə_qoymaq] & 0xffL)
                | ((verilənlər[yerinə_qoymaq + 1] & 0xffL) << 8)
                | ((verilənlər[yerinə_qoymaq + 2] & 0xffL) << 16)
                | ((verilənlər[yerinə_qoymaq + 3] & 0xffL) << 24);
    }
}

