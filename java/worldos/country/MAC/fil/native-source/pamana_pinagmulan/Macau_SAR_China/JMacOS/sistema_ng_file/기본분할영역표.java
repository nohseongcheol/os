// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_SAR_China.JMacOS.sistema_ng_file;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 value_ng_default 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partisyon_VALUE {
        private final int 종류;
        private final long Start_seksiyon;
        private final long seksiyon_COUNT;

        partisyon_VALUE(int 종류, long Start_seksiyon, long seksiyon_COUNT) {
            this.종류 = 종류;
            this.Start_seksiyon = Start_seksiyon;
            this.seksiyon_COUNT = seksiyon_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_seksiyon() { return Start_seksiyon; }
        public long seksiyon_COUNT() { return seksiyon_COUNT; }
    }

    public List<partisyon_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partisyon_VALUE> sukat = new ArrayList<partisyon_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int posisyon = 446 + INDEX * 16;
            int 종류 = 첫구역[posisyon + 4] & 0xff;
            long run = 작은순서정수(첫구역, posisyon + 8);
            long sukat_82232621 = 작은순서정수(첫구역, posisyon + 12);
            if (종류 != 0 && sukat_82232621 != 0) {
                sukat.add(new partisyon_VALUE(종류, run, sukat_82232621));
            }
        }
        return Collections.unmodifiableList(sukat);
    }

    private long 작은순서정수(byte[] data, int posisyon) {
        return (data[posisyon] & 0xffL)
                | ((data[posisyon + 1] & 0xffL) << 8)
                | ((data[posisyon + 2] & 0xffL) << 16)
                | ((data[posisyon + 3] & 0xffL) << 24);
    }
}

