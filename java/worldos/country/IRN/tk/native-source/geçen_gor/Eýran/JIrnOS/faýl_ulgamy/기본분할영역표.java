// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.faýl_ulgamy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 öňünden_kabul_edilen_baha 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class bölüm_baha {
        private final int 종류;
        private final long başlat_bölüm;
        private final long 구역수;

        bölüm_baha(int 종류, long başlat_bölüm, long 구역수) {
            this.종류 = 종류;
            this.başlat_bölüm = başlat_bölüm;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long başlat_bölüm() { return başlat_bölüm; }
        public long 구역수() { return 구역수; }
    }

    public List<bölüm_baha> Oka(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<bölüm_baha> 결과 = new ArrayList<bölüm_baha>();
        for (int indeks = 0; indeks < 4; indeks++) {
            int 위치 = 446 + indeks * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Bitir = 작은순서정수(첫구역, 위치 + 8);
            long Ululyk = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ululyk != 0) {
                결과.add(new bölüm_baha(종류, Bitir, Ululyk));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] maglumat, int 위치) {
        return (maglumat[위치] & 0xffL)
                | ((maglumat[위치 + 1] & 0xffL) << 8)
                | ((maglumat[위치 + 2] & 0xffL) << 16)
                | ((maglumat[위치 + 3] & 0xffL) << 24);
    }
}

