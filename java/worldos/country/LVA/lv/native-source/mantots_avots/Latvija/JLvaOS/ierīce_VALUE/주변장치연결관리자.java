// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.ierīce_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ierīce_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class ierīce_VALUE {
        private final int kreditors_identifikators;
        private final int ierīce_identifikators;
        private final int 입출력바탕;
        private final int IRQ_numurs;

        public ierīce_VALUE(int kreditors_identifikators, int ierīce_identifikators, int 입출력바탕, int IRQ_numurs) {
            this.kreditors_identifikators = kreditors_identifikators;
            this.ierīce_identifikators = ierīce_identifikators;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_numurs = IRQ_numurs;
        }

        public int kreditors_identifikators() { return kreditors_identifikators; }
        public int ierīce_identifikators() { return ierīce_identifikators; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_numurs() { return IRQ_numurs; }
    }

    private final List<ierīce_VALUE> Ierīces_Saraksts = new ArrayList<ierīce_VALUE>();

    public void 발견(ierīce_VALUE ierīce_VALUE) {
        Ierīces_Saraksts.add(ierīce_VALUE);
    }

    public List<ierīce_VALUE> Ierīces_Saraksts() {
        return Collections.unmodifiableList(Ierīces_Saraksts);
    }

    public ierīce_VALUE FIND_ievade(int kreditors_identifikators, int ierīce_identifikators) {
        for (ierīce_VALUE 후보 : Ierīces_Saraksts) {
            if (후보.kreditors_identifikators == kreditors_identifikators && 후보.ierīce_identifikators == ierīce_identifikators) {
                return 후보;
            }
        }
        return null;
    }
}

