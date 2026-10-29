// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फायल_प्रणाली;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 डिफॉल्ट_मोल 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class विभागणी_मोल {
        private final int 종류;
        private final long Start_विभाग;
        private final long विभाग_COUNT;

        विभागणी_मोल(int 종류, long Start_विभाग, long विभाग_COUNT) {
            this.종류 = 종류;
            this.Start_विभाग = Start_विभाग;
            this.विभाग_COUNT = विभाग_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_विभाग() { return Start_विभाग; }
        public long विभाग_COUNT() { return विभाग_COUNT; }
    }

    public List<विभागणी_मोल> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<विभागणी_मोल> मेजप = new ArrayList<विभागणी_मोल>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int स्थिती = 446 + INDEX * 16;
            int 종류 = 첫구역[स्थिती + 4] & 0xff;
            long चलोवप = 작은순서정수(첫구역, स्थिती + 8);
            long आवाठ = 작은순서정수(첫구역, स्थिती + 12);
            if (종류 != 0 && आवाठ != 0) {
                मेजप.add(new विभागणी_मोल(종류, चलोवप, आवाठ));
            }
        }
        return Collections.unmodifiableList(मेजप);
    }

    private long 작은순서정수(byte[] डेटा, int स्थिती) {
        return (डेटा[स्थिती] & 0xffL)
                | ((डेटा[स्थिती + 1] & 0xffL) << 8)
                | ((डेटा[स्थिती + 2] & 0xffL) << 16)
                | ((डेटा[स्थिती + 3] & 0xffL) << 24);
    }
}

