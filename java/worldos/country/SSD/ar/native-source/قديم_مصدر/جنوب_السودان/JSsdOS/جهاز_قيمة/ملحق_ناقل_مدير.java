// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جنوب_السودان.JSsdOS.جهاز_قيمة;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI جهاز_قيمة 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ملحق_ناقل_مدير {
    public static final class جهاز_قيمة {
        private final int مورّد_معرف;
        private final int جهاز_معرف;
        private final int 입출력바탕;
        private final int مقاطعة_رقم;

        public جهاز_قيمة(int مورّد_معرف, int جهاز_معرف, int 입출력바탕, int مقاطعة_رقم) {
            this.مورّد_معرف = مورّد_معرف;
            this.جهاز_معرف = جهاز_معرف;
            this.입출력바탕 = 입출력바탕;
            this.مقاطعة_رقم = مقاطعة_رقم;
        }

        public int مورّد_معرف() { return مورّد_معرف; }
        public int جهاز_معرف() { return جهاز_معرف; }
        public int 입출력바탕() { return 입출력바탕; }
        public int مقاطعة_رقم() { return مقاطعة_رقم; }
    }

    private final List<جهاز_قيمة> الأجهزة_قائمة = new ArrayList<جهاز_قيمة>();

    public void 발견(جهاز_قيمة جهاز_قيمة) {
        الأجهزة_قائمة.add(جهاز_قيمة);
    }

    public List<جهاز_قيمة> الأجهزة_قائمة() {
        return Collections.unmodifiableList(الأجهزة_قائمة);
    }

    public جهاز_قيمة بحث_إدخال(int مورّد_معرف, int جهاز_معرف) {
        for (جهاز_قيمة 후보 : الأجهزة_قائمة) {
            if (후보.مورّد_معرف == مورّد_معرف && 후보.جهاز_معرف == جهاز_معرف) {
                return 후보;
            }
        }
        return null;
    }
}

