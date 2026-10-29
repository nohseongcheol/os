// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package کینیڈا.JCanOS.فائل_نظام;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 طے_شدہ_قدر 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class بٹوارا_قدر {
        private final int 종류;
        private final long ابتدا_صیغہ;
        private final long 구역수;

        بٹوارا_قدر(int 종류, long ابتدا_صیغہ, long 구역수) {
            this.종류 = 종류;
            this.ابتدا_صیغہ = ابتدا_صیغہ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ابتدا_صیغہ() { return ابتدا_صیغہ; }
        public long 구역수() { return 구역수; }
    }

    public List<بٹوارا_قدر> پڑھیں(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<بٹوارا_قدر> پیمائش = new ArrayList<بٹوارا_قدر>();
        for (int اشاریہ = 0; اشاریہ < 4; اشاریہ++) {
            int مقام = 446 + اشاریہ * 16;
            int 종류 = 첫구역[مقام + 4] & 0xff;
            long چلائیں = 작은순서정수(첫구역, مقام + 8);
            long حجم = 작은순서정수(첫구역, مقام + 12);
            if (종류 != 0 && حجم != 0) {
                پیمائش.add(new بٹوارا_قدر(종류, چلائیں, حجم));
            }
        }
        return Collections.unmodifiableList(پیمائش);
    }

    private long 작은순서정수(byte[] کوائف, int مقام) {
        return (کوائف[مقام] & 0xffL)
                | ((کوائف[مقام + 1] & 0xffL) << 8)
                | ((کوائف[مقام + 2] & 0xffL) << 16)
                | ((کوائف[مقام + 3] & 0xffL) << 24);
    }
}

