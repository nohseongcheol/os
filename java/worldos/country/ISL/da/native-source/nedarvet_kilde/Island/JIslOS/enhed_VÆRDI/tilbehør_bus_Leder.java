// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Island.JIslOS.enhed_VÆRDI;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI enhed_VÆRDI 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class tilbehør_bus_Leder {
    public static final class enhed_VÆRDI {
        private final int kreditor_identifikator;
        private final int enhed_identifikator;
        private final int 입출력바탕;
        private final int IRQ_tal;

        public enhed_VÆRDI(int kreditor_identifikator, int enhed_identifikator, int 입출력바탕, int IRQ_tal) {
            this.kreditor_identifikator = kreditor_identifikator;
            this.enhed_identifikator = enhed_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_tal = IRQ_tal;
        }

        public int kreditor_identifikator() { return kreditor_identifikator; }
        public int enhed_identifikator() { return enhed_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_tal() { return IRQ_tal; }
    }

    private final List<enhed_VÆRDI> Enheder_Liste = new ArrayList<enhed_VÆRDI>();

    public void 발견(enhed_VÆRDI enhed_VÆRDI) {
        Enheder_Liste.add(enhed_VÆRDI);
    }

    public List<enhed_VÆRDI> Enheder_Liste() {
        return Collections.unmodifiableList(Enheder_Liste);
    }

    public enhed_VÆRDI Søg_post(int kreditor_identifikator, int enhed_identifikator) {
        for (enhed_VÆRDI 후보 : Enheder_Liste) {
            if (후보.kreditor_identifikator == kreditor_identifikator && 후보.enhed_identifikator == enhed_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

