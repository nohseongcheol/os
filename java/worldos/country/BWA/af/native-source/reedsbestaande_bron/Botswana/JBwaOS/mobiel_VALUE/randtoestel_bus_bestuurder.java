// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.mobiel_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobiel_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class randtoestel_bus_bestuurder {
    public static final class mobiel_VALUE {
        private final int handelaar_waarde;
        private final int mobiel_waarde;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public mobiel_VALUE(int handelaar_waarde, int mobiel_waarde, int 입출력바탕, int 개입중단번호) {
            this.handelaar_waarde = handelaar_waarde;
            this.mobiel_waarde = mobiel_waarde;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int handelaar_waarde() { return handelaar_waarde; }
        public int mobiel_waarde() { return mobiel_waarde; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<mobiel_VALUE> Toestelle_Lys = new ArrayList<mobiel_VALUE>();

    public void 발견(mobiel_VALUE mobiel_VALUE) {
        Toestelle_Lys.add(mobiel_VALUE);
    }

    public List<mobiel_VALUE> Toestelle_Lys() {
        return Collections.unmodifiableList(Toestelle_Lys);
    }

    public mobiel_VALUE FIND_inskrywing(int handelaar_waarde, int mobiel_waarde) {
        for (mobiel_VALUE 후보 : Toestelle_Lys) {
            if (후보.handelaar_waarde == handelaar_waarde && 후보.mobiel_waarde == mobiel_waarde) {
                return 후보;
            }
        }
        return null;
    }
}

