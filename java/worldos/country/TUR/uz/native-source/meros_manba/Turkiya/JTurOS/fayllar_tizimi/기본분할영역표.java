// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkiya.JTurOS.fayllar_tizimi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 sukut_bo_yicha_qiymat 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class bo_lim_VALUE {
        private final int 종류;
        private final long Start_bo_lim;
        private final long bo_lim_COUNT;

        bo_lim_VALUE(int 종류, long Start_bo_lim, long bo_lim_COUNT) {
            this.종류 = 종류;
            this.Start_bo_lim = Start_bo_lim;
            this.bo_lim_COUNT = bo_lim_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_bo_lim() { return Start_bo_lim; }
        public long bo_lim_COUNT() { return bo_lim_COUNT; }
    }

    public List<bo_lim_VALUE> Oʻqish(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<bo_lim_VALUE> o_lchov = new ArrayList<bo_lim_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Holati = 446 + INDEX * 16;
            int 종류 = 첫구역[Holati + 4] & 0xff;
            long Bajarish = 작은순서정수(첫구역, Holati + 8);
            long Hajmi = 작은순서정수(첫구역, Holati + 12);
            if (종류 != 0 && Hajmi != 0) {
                o_lchov.add(new bo_lim_VALUE(종류, Bajarish, Hajmi));
            }
        }
        return Collections.unmodifiableList(o_lchov);
    }

    private long 작은순서정수(byte[] ma_lumotlar, int Holati) {
        return (ma_lumotlar[Holati] & 0xffL)
                | ((ma_lumotlar[Holati + 1] & 0xffL) << 8)
                | ((ma_lumotlar[Holati + 2] & 0xffL) << 16)
                | ((ma_lumotlar[Holati + 3] & 0xffL) << 24);
    }
}

