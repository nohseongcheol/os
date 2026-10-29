// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.ئامێر_نرخ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ئامێر_نرخ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class لاوەکی_باس_بەڕێوەبەر {
    public static final class ئامێر_نرخ {
        private final int 판매자식별자;
        private final int ئامێر_ناسێنەر;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ئامێر_نرخ(int 판매자식별자, int ئامێر_ناسێنەر, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ئامێر_ناسێنەر = ئامێر_ناسێنەر;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ئامێر_ناسێنەر() { return ئامێر_ناسێنەر; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ئامێر_نرخ> ئامێرەکان_لیست = new ArrayList<ئامێر_نرخ>();

    public void 발견(ئامێر_نرخ ئامێر_نرخ) {
        ئامێرەکان_لیست.add(ئامێر_نرخ);
    }

    public List<ئامێر_نرخ> ئامێرەکان_لیست() {
        return Collections.unmodifiableList(ئامێرەکان_لیست);
    }

    public ئامێر_نرخ دۆزینەوە_تێنووسین(int 판매자식별자, int ئامێر_ناسێنەر) {
        for (ئامێر_نرخ 후보 : ئامێرەکان_لیست) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ئامێر_ناسێنەر == ئامێر_ناسێنەر) {
                return 후보;
            }
        }
        return null;
    }
}

