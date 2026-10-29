// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.систем_на_датотеки;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 стандардна_вредност 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class партиција_VALUE {
        private final int 종류;
        private final long Start_секција;
        private final long секција_COUNT;

        партиција_VALUE(int 종류, long Start_секција, long секција_COUNT) {
            this.종류 = 종류;
            this.Start_секција = Start_секција;
            this.секција_COUNT = секција_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_секција() { return Start_секција; }
        public long секција_COUNT() { return секција_COUNT; }
    }

    public List<партиција_VALUE> Читај(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<партиција_VALUE> мерка = new ArrayList<партиција_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Позиција = 446 + INDEX * 16;
            int 종류 = 첫구역[Позиција + 4] & 0xff;
            long Изврши_2 = 작은순서정수(첫구역, Позиција + 8);
            long Големина = 작은순서정수(첫구역, Позиција + 12);
            if (종류 != 0 && Големина != 0) {
                мерка.add(new партиција_VALUE(종류, Изврши_2, Големина));
            }
        }
        return Collections.unmodifiableList(мерка);
    }

    private long 작은순서정수(byte[] податоци, int Позиција) {
        return (податоци[Позиција] & 0xffL)
                | ((податоци[Позиција + 1] & 0xffL) << 8)
                | ((податоци[Позиција + 2] & 0xffL) << 16)
                | ((податоци[Позиција + 3] & 0xffL) << 24);
    }
}

