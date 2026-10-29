// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.ھۆججەت_سىستېمىسى;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 سۈكۈتتىكى_قىممەت 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class رايون_قىممىتى {
        private final int 종류;
        private final long باشلاش_بۆلۈم;
        private final long 구역수;

        رايون_قىممىتى(int 종류, long باشلاش_بۆلۈم, long 구역수) {
            this.종류 = 종류;
            this.باشلاش_بۆلۈم = باشلاش_بۆلۈم;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long باشلاش_بۆلۈم() { return باشلاش_بۆلۈم; }
        public long 구역수() { return 구역수; }
    }

    public List<رايون_قىممىتى> ئوقۇ(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<رايون_قىممىتى> ئۆلچەم = new ArrayList<رايون_قىممىتى>();
        for (int ئىندېكس = 0; ئىندېكس < 4; ئىندېكس++) {
            int ئورۇن = 446 + ئىندېكس * 16;
            int 종류 = 첫구역[ئورۇن + 4] & 0xff;
            long ئىجرا_قىل_2 = 작은순서정수(첫구역, ئورۇن + 8);
            long چوڭلۇقى = 작은순서정수(첫구역, ئورۇن + 12);
            if (종류 != 0 && چوڭلۇقى != 0) {
                ئۆلچەم.add(new رايون_قىممىتى(종류, ئىجرا_قىل_2, چوڭلۇقى));
            }
        }
        return Collections.unmodifiableList(ئۆلچەم);
    }

    private long 작은순서정수(byte[] مەلۇمات, int ئورۇن) {
        return (مەلۇمات[ئورۇن] & 0xffL)
                | ((مەلۇمات[ئورۇن + 1] & 0xffL) << 8)
                | ((مەلۇمات[ئورۇن + 2] & 0xffL) << 16)
                | ((مەلۇمات[ئورۇن + 3] & 0xffL) << 24);
    }
}

