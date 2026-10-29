// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package दक्षिण_अफ़्रीका.JZafOS.फ़ाइल_सिस्टम;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 डिफ़ॉल्ट_मान 분할 영역을 읽는다. */
public final class प्राथमिक_पार्टिशन_तालिका {
    public static final class विभाजन_मान {
        private final int 종류;
        private final long प्रारंभ_खंड;
        private final long 구역수;

        विभाजन_मान(int 종류, long प्रारंभ_खंड, long 구역수) {
            this.종류 = 종류;
            this.प्रारंभ_खंड = प्रारंभ_खंड;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long प्रारंभ_खंड() { return प्रारंभ_खंड; }
        public long 구역수() { return 구역수; }
    }

    public List<विभाजन_मान> पढ़ें(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<विभाजन_मान> परिणाम = new ArrayList<विभाजन_मान>();
        for (int इंडेक्स = 0; इंडेक्स < 4; इंडेक्स++) {
            int स्थान = 446 + इंडेक्स * 16;
            int 종류 = 첫구역[स्थान + 4] & 0xff;
            long चलाएँ = लिटिल_एंडियन_पूर्णांक(첫구역, स्थान + 8);
            long आकार = लिटिल_एंडियन_पूर्णांक(첫구역, स्थान + 12);
            if (종류 != 0 && आकार != 0) {
                परिणाम.add(new विभाजन_मान(종류, चलाएँ, आकार));
            }
        }
        return Collections.unmodifiableList(परिणाम);
    }

    private long लिटिल_एंडियन_पूर्णांक(byte[] आँकड़े, int स्थान) {
        return (आँकड़े[स्थान] & 0xffL)
                | ((आँकड़े[स्थान + 1] & 0xffL) << 8)
                | ((आँकड़े[स्थान + 2] & 0xffL) << 16)
                | ((आँकड़े[स्थान + 3] & 0xffL) << 24);
    }
}

