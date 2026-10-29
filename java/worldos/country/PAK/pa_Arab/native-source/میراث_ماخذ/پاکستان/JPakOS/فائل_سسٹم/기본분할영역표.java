// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_سسٹم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 طےشدہ_قدر 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class تقسیم_قدر {
        private final int 종류;
        private final long مکھ_سیکشن;
        private final long 구역수;

        تقسیم_قدر(int 종류, long مکھ_سیکشن, long 구역수) {
            this.종류 = 종류;
            this.مکھ_سیکشن = مکھ_سیکشن;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long مکھ_سیکشن() { return مکھ_سیکشن; }
        public long 구역수() { return 구역수; }
    }

    public List<تقسیم_قدر> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<تقسیم_قدر> 결과 = new ArrayList<تقسیم_قدر>();
        for (int اشاریہ = 0; اشاریہ < 4; اشاریہ++) {
            int 위치 = 446 + اشاریہ * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long چلاؤ = 작은순서정수(첫구역, 위치 + 8);
            long سائز = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && سائز != 0) {
                결과.add(new تقسیم_قدر(종류, چلاؤ, سائز));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] کوائف, int 위치) {
        return (کوائف[위치] & 0xffL)
                | ((کوائف[위치 + 1] & 0xffL) << 8)
                | ((کوائف[위치 + 2] & 0xffL) << 16)
                | ((کوائف[위치 + 3] & 0xffL) << 24);
    }
}

