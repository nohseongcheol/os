// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 luach_bunaiteach 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class pàirteachadh_VALUE {
        private final int 종류;
        private final long Start_earrann;
        private final long earrann_COUNT;

        pàirteachadh_VALUE(int 종류, long Start_earrann, long earrann_COUNT) {
            this.종류 = 종류;
            this.Start_earrann = Start_earrann;
            this.earrann_COUNT = earrann_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_earrann() { return Start_earrann; }
        public long earrann_COUNT() { return earrann_COUNT; }
    }

    public List<pàirteachadh_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<pàirteachadh_VALUE> tomhas = new ArrayList<pàirteachadh_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int suidhich = 446 + INDEX * 16;
            int 종류 = 첫구역[suidhich + 4] & 0xff;
            long ruith = 작은순서정수(첫구역, suidhich + 8);
            long atharraich_am_meud = 작은순서정수(첫구역, suidhich + 12);
            if (종류 != 0 && atharraich_am_meud != 0) {
                tomhas.add(new pàirteachadh_VALUE(종류, ruith, atharraich_am_meud));
            }
        }
        return Collections.unmodifiableList(tomhas);
    }

    private long 작은순서정수(byte[] dàta, int suidhich) {
        return (dàta[suidhich] & 0xffL)
                | ((dàta[suidhich + 1] & 0xffL) << 8)
                | ((dàta[suidhich + 2] & 0xffL) << 16)
                | ((dàta[suidhich + 3] & 0xffL) << 24);
    }
}

