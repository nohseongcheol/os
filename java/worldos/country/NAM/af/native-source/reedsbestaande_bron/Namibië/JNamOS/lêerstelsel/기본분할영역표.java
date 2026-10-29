// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.lêerstelsel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 verstekwaarde 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partisie_VALUE {
        private final int 종류;
        private final long BEGIN_seksie;
        private final long seksie_COUNT;

        partisie_VALUE(int 종류, long BEGIN_seksie, long seksie_COUNT) {
            this.종류 = 종류;
            this.BEGIN_seksie = BEGIN_seksie;
            this.seksie_COUNT = seksie_COUNT;
        }

        public int 종류() { return 종류; }
        public long BEGIN_seksie() { return BEGIN_seksie; }
        public long seksie_COUNT() { return seksie_COUNT; }
    }

    public List<partisie_VALUE> Lees(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partisie_VALUE> maatreël = new ArrayList<partisie_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Posisie = 446 + INDEX * 16;
            int 종류 = 첫구역[Posisie + 4] & 0xff;
            long Loop = 작은순서정수(첫구역, Posisie + 8);
            long Grootte = 작은순서정수(첫구역, Posisie + 12);
            if (종류 != 0 && Grootte != 0) {
                maatreël.add(new partisie_VALUE(종류, Loop, Grootte));
            }
        }
        return Collections.unmodifiableList(maatreël);
    }

    private long 작은순서정수(byte[] data, int Posisie) {
        return (data[Posisie] & 0xffL)
                | ((data[Posisie + 1] & 0xffL) << 8)
                | ((data[Posisie + 2] & 0xffL) << 16)
                | ((data[Posisie + 3] & 0xffL) << 24);
    }
}

