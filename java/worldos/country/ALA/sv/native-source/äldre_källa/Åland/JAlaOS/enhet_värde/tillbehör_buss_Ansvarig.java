// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Åland.JAlaOS.enhet_värde;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI enhet_värde 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class tillbehör_buss_Ansvarig {
    public static final class enhet_värde {
        private final int säljare_identifierare;
        private final int enhet_identifierare;
        private final int 입출력바탕;
        private final int IRQ_nummer;

        public enhet_värde(int säljare_identifierare, int enhet_identifierare, int 입출력바탕, int IRQ_nummer) {
            this.säljare_identifierare = säljare_identifierare;
            this.enhet_identifierare = enhet_identifierare;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_nummer = IRQ_nummer;
        }

        public int säljare_identifierare() { return säljare_identifierare; }
        public int enhet_identifierare() { return enhet_identifierare; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_nummer() { return IRQ_nummer; }
    }

    private final List<enhet_värde> Enheter_ange = new ArrayList<enhet_värde>();

    public void 발견(enhet_värde enhet_värde) {
        Enheter_ange.add(enhet_värde);
    }

    public List<enhet_värde> Enheter_ange() {
        return Collections.unmodifiableList(Enheter_ange);
    }

    public enhet_värde Sök_post(int säljare_identifierare, int enhet_identifierare) {
        for (enhet_värde kandidat : Enheter_ange) {
            if (kandidat.säljare_identifierare == säljare_identifierare && kandidat.enhet_identifierare == enhet_identifierare) {
                return kandidat;
            }
        }
        return null;
    }
}

