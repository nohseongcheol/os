// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फाइल_प्रणाली;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 पूर्वनिर्धारित_मान 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class विभाजन_मान {
        private final int 종류;
        private final long सुरु_सेक्सन;
        private final long 구역수;

        विभाजन_मान(int 종류, long सुरु_सेक्सन, long 구역수) {
            this.종류 = 종류;
            this.सुरु_सेक्सन = सुरु_सेक्सन;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long सुरु_सेक्सन() { return सुरु_सेक्सन; }
        public long 구역수() { return 구역수; }
    }

    public List<विभाजन_मान> पढनुहोस्(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<विभाजन_मान> मापन = new ArrayList<विभाजन_मान>();
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < 4; अनुक्रमणिका++) {
            int स्थिति = 446 + अनुक्रमणिका * 16;
            int 종류 = 첫구역[स्थिति + 4] & 0xff;
            long चलाउनुहोस् = 작은순서정수(첫구역, स्थिति + 8);
            long आकार = 작은순서정수(첫구역, स्थिति + 12);
            if (종류 != 0 && आकार != 0) {
                मापन.add(new विभाजन_मान(종류, चलाउनुहोस्, आकार));
            }
        }
        return Collections.unmodifiableList(मापन);
    }

    private long 작은순서정수(byte[] लगत, int स्थिति) {
        return (लगत[स्थिति] & 0xffL)
                | ((लगत[स्थिति + 1] & 0xffL) << 8)
                | ((लगत[स्थिति + 2] & 0xffL) << 16)
                | ((लगत[स्थिति + 3] & 0xffL) << 24);
    }
}

