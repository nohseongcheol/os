// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package कनाडा.JCanOS.उपकरण_मान;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI उपकरण_मान 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class एक्सेसरी_बस_प्रबंधक {
    public static final class उपकरण_मान {
        private final int वेंडर_पहचानकर्ता;
        private final int उपकरण_पहचानकर्ता;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public उपकरण_मान(int वेंडर_पहचानकर्ता, int उपकरण_पहचानकर्ता, int 입출력바탕, int 개입중단번호) {
            this.वेंडर_पहचानकर्ता = वेंडर_पहचानकर्ता;
            this.उपकरण_पहचानकर्ता = उपकरण_पहचानकर्ता;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int वेंडर_पहचानकर्ता() { return वेंडर_पहचानकर्ता; }
        public int उपकरण_पहचानकर्ता() { return उपकरण_पहचानकर्ता; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<उपकरण_मान> उपकरण_सूची = new ArrayList<उपकरण_मान>();

    public void 발견(उपकरण_मान उपकरण_मान) {
        उपकरण_सूची.add(उपकरण_मान);
    }

    public List<उपकरण_मान> उपकरण_सूची() {
        return Collections.unmodifiableList(उपकरण_सूची);
    }

    public उपकरण_मान खोजें_एन्ट्री(int वेंडर_पहचानकर्ता, int उपकरण_पहचानकर्ता) {
        for (उपकरण_मान 후보 : उपकरण_सूची) {
            if (후보.वेंडर_पहचानकर्ता == वेंडर_पहचानकर्ता && 후보.उपकरण_पहचानकर्ता == उपकरण_पहचानकर्ता) {
                return 후보;
            }
        }
        return null;
    }
}

