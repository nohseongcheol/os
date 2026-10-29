// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاڪستان.JPakOS.فائل_سسٽم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 طئي_ٿيل_ملهه 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ورڇ_قدر {
        private final int 종류;
        private final long شروع_سيڪشن;
        private final long 구역수;

        ورڇ_قدر(int 종류, long شروع_سيڪشن, long 구역수) {
            this.종류 = 종류;
            this.شروع_سيڪشن = شروع_سيڪشن;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long شروع_سيڪشن() { return شروع_سيڪشن; }
        public long 구역수() { return 구역수; }
    }

    public List<ورڇ_قدر> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ورڇ_قدر> 결과 = new ArrayList<ورڇ_قدر>();
        for (int ابتدائي = 0; ابتدائي < 4; ابتدائي++) {
            int 위치 = 446 + ابتدائي * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long هلائڻ = 작은순서정수(첫구역, 위치 + 8);
            long سائيز = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && سائيز != 0) {
                결과.add(new ورڇ_قدر(종류, هلائڻ, سائيز));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] ڪوائف, int 위치) {
        return (ڪوائف[위치] & 0xffL)
                | ((ڪوائف[위치 + 1] & 0xffL) << 8)
                | ((ڪوائف[위치 + 2] & 0xffL) << 16)
                | ((ڪوائف[위치 + 3] & 0xffL) << 24);
    }
}

