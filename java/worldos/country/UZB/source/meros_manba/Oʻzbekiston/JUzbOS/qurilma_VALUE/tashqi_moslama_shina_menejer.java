// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.qurilma_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI qurilma_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class tashqi_moslama_shina_menejer {
    public static final class qurilma_VALUE {
        private final int firma_identifikator;
        private final int qurilma_identifikator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public qurilma_VALUE(int firma_identifikator, int qurilma_identifikator, int 입출력바탕, int 개입중단번호) {
            this.firma_identifikator = firma_identifikator;
            this.qurilma_identifikator = qurilma_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int firma_identifikator() { return firma_identifikator; }
        public int qurilma_identifikator() { return qurilma_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<qurilma_VALUE> Qurilmalar_Ro_yxat = new ArrayList<qurilma_VALUE>();

    public void 발견(qurilma_VALUE qurilma_VALUE) {
        Qurilmalar_Ro_yxat.add(qurilma_VALUE);
    }

    public List<qurilma_VALUE> Qurilmalar_Ro_yxat() {
        return Collections.unmodifiableList(Qurilmalar_Ro_yxat);
    }

    public qurilma_VALUE FIND_kiritish(int firma_identifikator, int qurilma_identifikator) {
        for (qurilma_VALUE 후보 : Qurilmalar_Ro_yxat) {
            if (후보.firma_identifikator == firma_identifikator && 후보.qurilma_identifikator == qurilma_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

