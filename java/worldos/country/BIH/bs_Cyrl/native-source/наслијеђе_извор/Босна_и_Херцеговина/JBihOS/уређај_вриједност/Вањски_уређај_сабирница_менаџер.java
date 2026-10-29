// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.уређај_вриједност;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI уређај_вриједност 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class Вањски_уређај_сабирница_менаџер {
    public static final class уређај_вриједност {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public уређај_вриједност(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.장치식별자 = 장치식별자;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int 장치식별자() { return 장치식별자; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<уређај_вриједност> Уређаји_списак = new ArrayList<уређај_вриједност>();

    public void 발견(уређај_вриједност уређај_вриједност) {
        Уређаји_списак.add(уређај_вриједност);
    }

    public List<уређај_вриједност> Уређаји_списак() {
        return Collections.unmodifiableList(Уређаји_списак);
    }

    public уређај_вриједност наћи_унос(int 판매자식별자, int 장치식별자) {
        for (уређај_вриједност 후보 : Уређаји_списак) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

