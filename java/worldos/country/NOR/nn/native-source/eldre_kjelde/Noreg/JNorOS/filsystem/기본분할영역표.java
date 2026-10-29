// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standardverdi 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partisjon_VALUE {
        private final int 종류;
        private final long START_del;
        private final long del_COUNT;

        partisjon_VALUE(int 종류, long START_del, long del_COUNT) {
            this.종류 = 종류;
            this.START_del = START_del;
            this.del_COUNT = del_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_del() { return START_del; }
        public long del_COUNT() { return del_COUNT; }
    }

    public List<partisjon_VALUE> Les(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partisjon_VALUE> forretningsmål = new ArrayList<partisjon_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Posisjon = 446 + INDEX * 16;
            int 종류 = 첫구역[Posisjon + 4] & 0xff;
            long Køyr_2 = 작은순서정수(첫구역, Posisjon + 8);
            long Storleik = 작은순서정수(첫구역, Posisjon + 12);
            if (종류 != 0 && Storleik != 0) {
                forretningsmål.add(new partisjon_VALUE(종류, Køyr_2, Storleik));
            }
        }
        return Collections.unmodifiableList(forretningsmål);
    }

    private long 작은순서정수(byte[] data, int Posisjon) {
        return (data[Posisjon] & 0xffL)
                | ((data[Posisjon + 1] & 0xffL) << 8)
                | ((data[Posisjon + 2] & 0xffL) << 16)
                | ((data[Posisjon + 3] & 0xffL) << 24);
    }
}

