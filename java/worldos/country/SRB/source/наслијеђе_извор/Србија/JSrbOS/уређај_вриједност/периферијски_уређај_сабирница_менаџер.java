// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.уређај_вриједност;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI уређај_вриједност 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class периферијски_уређај_сабирница_менаџер {
    public static final class уређај_вриједност {
        private final int снабдевач_идентификатор;
        private final int уређај_идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public уређај_вриједност(int снабдевач_идентификатор, int уређај_идентификатор, int 입출력바탕, int 개입중단번호) {
            this.снабдевач_идентификатор = снабдевач_идентификатор;
            this.уређај_идентификатор = уређај_идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int снабдевач_идентификатор() { return снабдевач_идентификатор; }
        public int уређај_идентификатор() { return уређај_идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<уређај_вриједност> Уређаји_Листа = new ArrayList<уређај_вриједност>();

    public void 발견(уређај_вриједност уређај_вриједност) {
        Уређаји_Листа.add(уређај_вриједност);
    }

    public List<уређај_вриједност> Уређаји_Листа() {
        return Collections.unmodifiableList(Уређаји_Листа);
    }

    public уређај_вриједност наћи_унос(int снабдевач_идентификатор, int уређај_идентификатор) {
        for (уређај_вриједност 후보 : Уређаји_Листа) {
            if (후보.снабдевач_идентификатор == снабдевач_идентификатор && 후보.уређај_идентификатор == уређај_идентификатор) {
                return 후보;
            }
        }
        return null;
    }
}

