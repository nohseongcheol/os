// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.enhet_VERDI;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI enhet_VERDI 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class tilbehør_buss_overordnet {
    public static final class enhet_VERDI {
        private final int leverandør_identifikator;
        private final int enhet_identifikator;
        private final int 입출력바탕;
        private final int IRQ_nummer;

        public enhet_VERDI(int leverandør_identifikator, int enhet_identifikator, int 입출력바탕, int IRQ_nummer) {
            this.leverandør_identifikator = leverandør_identifikator;
            this.enhet_identifikator = enhet_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_nummer = IRQ_nummer;
        }

        public int leverandør_identifikator() { return leverandør_identifikator; }
        public int enhet_identifikator() { return enhet_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_nummer() { return IRQ_nummer; }
    }

    private final List<enhet_VERDI> Enheter_Liste = new ArrayList<enhet_VERDI>();

    public void 발견(enhet_VERDI enhet_VERDI) {
        Enheter_Liste.add(enhet_VERDI);
    }

    public List<enhet_VERDI> Enheter_Liste() {
        return Collections.unmodifiableList(Enheter_Liste);
    }

    public enhet_VERDI Søk_oppføring(int leverandør_identifikator, int enhet_identifikator) {
        for (enhet_VERDI 후보 : Enheter_Liste) {
            if (후보.leverandør_identifikator == leverandør_identifikator && 후보.enhet_identifikator == enhet_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

