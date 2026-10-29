// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.mobil_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobil_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ekstern_eining_buss_leiar {
    public static final class mobil_VALUE {
        private final int 판매자식별자;
        private final int mobil_identifikator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public mobil_VALUE(int 판매자식별자, int mobil_identifikator, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.mobil_identifikator = mobil_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int mobil_identifikator() { return mobil_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<mobil_VALUE> Einingar_Liste = new ArrayList<mobil_VALUE>();

    public void 발견(mobil_VALUE mobil_VALUE) {
        Einingar_Liste.add(mobil_VALUE);
    }

    public List<mobil_VALUE> Einingar_Liste() {
        return Collections.unmodifiableList(Einingar_Liste);
    }

    public mobil_VALUE Søk_oppføring(int 판매자식별자, int mobil_identifikator) {
        for (mobil_VALUE 후보 : Einingar_Liste) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.mobil_identifikator == mobil_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

