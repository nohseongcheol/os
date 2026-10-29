// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ماریشس.JMusOS.آلہ_قدر;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI آلہ_قدر 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class لازمہ_بس_مینیجر {
    public static final class آلہ_قدر {
        private final int 판매자식별자;
        private final int آلہ_شناخت_کنندہ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public آلہ_قدر(int 판매자식별자, int آلہ_شناخت_کنندہ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.آلہ_شناخت_کنندہ = آلہ_شناخت_کنندہ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int آلہ_شناخت_کنندہ() { return آلہ_شناخت_کنندہ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<آلہ_قدر> آلات_فہرست = new ArrayList<آلہ_قدر>();

    public void 발견(آلہ_قدر آلہ_قدر) {
        آلات_فہرست.add(آلہ_قدر);
    }

    public List<آلہ_قدر> آلات_فہرست() {
        return Collections.unmodifiableList(آلات_فہرست);
    }

    public آلہ_قدر ڈھونڈیں_اندراج(int 판매자식별자, int آلہ_شناخت_کنندہ) {
        for (آلہ_قدر 후보 : آلات_فہرست) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.آلہ_شناخت_کنندہ == آلہ_شناخت_کنندہ) {
                return 후보;
            }
        }
        return null;
    }
}

