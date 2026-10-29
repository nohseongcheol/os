// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package امارات_متحدهٔ_عربی.JAreOS.دستگاه_مقدار;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI دستگاه_مقدار 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class جانبی_انتقال_دهنده_مدیر {
    public static final class دستگاه_مقدار {
        private final int تولیدکننده_شناسه;
        private final int دستگاه_شناسه;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public دستگاه_مقدار(int تولیدکننده_شناسه, int دستگاه_شناسه, int 입출력바탕, int 개입중단번호) {
            this.تولیدکننده_شناسه = تولیدکننده_شناسه;
            this.دستگاه_شناسه = دستگاه_شناسه;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int تولیدکننده_شناسه() { return تولیدکننده_شناسه; }
        public int دستگاه_شناسه() { return دستگاه_شناسه; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<دستگاه_مقدار> دستگاه_ها_لیست = new ArrayList<دستگاه_مقدار>();

    public void 발견(دستگاه_مقدار دستگاه_مقدار) {
        دستگاه_ها_لیست.add(دستگاه_مقدار);
    }

    public List<دستگاه_مقدار> دستگاه_ها_لیست() {
        return Collections.unmodifiableList(دستگاه_ها_لیست);
    }

    public دستگاه_مقدار کشف_ورودی(int تولیدکننده_شناسه, int دستگاه_شناسه) {
        for (دستگاه_مقدار 후보 : دستگاه_ها_لیست) {
            if (후보.تولیدکننده_شناسه == تولیدکننده_شناسه && 후보.دستگاه_شناسه == دستگاه_شناسه) {
                return 후보;
            }
        }
        return null;
    }
}

