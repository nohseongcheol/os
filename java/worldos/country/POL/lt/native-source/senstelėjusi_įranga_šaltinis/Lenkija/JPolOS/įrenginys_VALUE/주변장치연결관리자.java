// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lenkija.JPolOS.įrenginys_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI įrenginys_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class įrenginys_VALUE {
        private final int tiekėjas_identifikatorius;
        private final int įrenginys_identifikatorius;
        private final int 입출력바탕;
        private final int IRQ_numeris;

        public įrenginys_VALUE(int tiekėjas_identifikatorius, int įrenginys_identifikatorius, int 입출력바탕, int IRQ_numeris) {
            this.tiekėjas_identifikatorius = tiekėjas_identifikatorius;
            this.įrenginys_identifikatorius = įrenginys_identifikatorius;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_numeris = IRQ_numeris;
        }

        public int tiekėjas_identifikatorius() { return tiekėjas_identifikatorius; }
        public int įrenginys_identifikatorius() { return įrenginys_identifikatorius; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_numeris() { return IRQ_numeris; }
    }

    private final List<įrenginys_VALUE> Įrenginiai_Sąrašas = new ArrayList<įrenginys_VALUE>();

    public void 발견(įrenginys_VALUE įrenginys_VALUE) {
        Įrenginiai_Sąrašas.add(įrenginys_VALUE);
    }

    public List<įrenginys_VALUE> Įrenginiai_Sąrašas() {
        return Collections.unmodifiableList(Įrenginiai_Sąrašas);
    }

    public įrenginys_VALUE FIND_įrašas(int tiekėjas_identifikatorius, int įrenginys_identifikatorius) {
        for (įrenginys_VALUE 후보 : Įrenginiai_Sąrašas) {
            if (후보.tiekėjas_identifikatorius == tiekėjas_identifikatorius && 후보.įrenginys_identifikatorius == įrenginys_identifikatorius) {
                return 후보;
            }
        }
        return null;
    }
}

