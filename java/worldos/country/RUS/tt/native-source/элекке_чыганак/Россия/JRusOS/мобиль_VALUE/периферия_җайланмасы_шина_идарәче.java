// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.мобиль_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI мобиль_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class периферия_җайланмасы_шина_идарәче {
    public static final class мобиль_VALUE {
        private final int 판매자식별자;
        private final int мобиль_күрсәткеч;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public мобиль_VALUE(int 판매자식별자, int мобиль_күрсәткеч, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.мобиль_күрсәткеч = мобиль_күрсәткеч;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int мобиль_күрсәткеч() { return мобиль_күрсәткеч; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<мобиль_VALUE> Җайланма_Исемлек = new ArrayList<мобиль_VALUE>();

    public void 발견(мобиль_VALUE мобиль_VALUE) {
        Җайланма_Исемлек.add(мобиль_VALUE);
    }

    public List<мобиль_VALUE> Җайланма_Исемлек() {
        return Collections.unmodifiableList(Җайланма_Исемлек);
    }

    public мобиль_VALUE FIND_кертү(int 판매자식별자, int мобиль_күрсәткеч) {
        for (мобиль_VALUE 후보 : Җайланма_Исемлек) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.мобиль_күрсәткеч == мобиль_күрсәткеч) {
                return 후보;
            }
        }
        return null;
    }
}

