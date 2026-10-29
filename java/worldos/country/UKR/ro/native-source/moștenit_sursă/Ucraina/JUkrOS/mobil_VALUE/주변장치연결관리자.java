// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ucraina.JUkrOS.mobil_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobil_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class mobil_VALUE {
        private final int furnizor_identificator;
        private final int mobil_identificator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public mobil_VALUE(int furnizor_identificator, int mobil_identificator, int 입출력바탕, int 개입중단번호) {
            this.furnizor_identificator = furnizor_identificator;
            this.mobil_identificator = mobil_identificator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int furnizor_identificator() { return furnizor_identificator; }
        public int mobil_identificator() { return mobil_identificator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<mobil_VALUE> Dispozitive_Listă = new ArrayList<mobil_VALUE>();

    public void 발견(mobil_VALUE mobil_VALUE) {
        Dispozitive_Listă.add(mobil_VALUE);
    }

    public List<mobil_VALUE> Dispozitive_Listă() {
        return Collections.unmodifiableList(Dispozitive_Listă);
    }

    public mobil_VALUE FIND_intrare(int furnizor_identificator, int mobil_identificator) {
        for (mobil_VALUE 후보 : Dispozitive_Listă) {
            if (후보.furnizor_identificator == furnizor_identificator && 후보.mobil_identificator == mobil_identificator) {
                return 후보;
            }
        }
        return null;
    }
}

