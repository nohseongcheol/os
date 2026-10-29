// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ZWE.JZweOS.mobaele_Boleng;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobaele_Boleng 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class sethusi_setsamaisamelaetsa_motsamaisi {
    public static final class mobaele_Boleng {
        private final int 판매자식별자;
        private final int mobaele_setlhaodi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public mobaele_Boleng(int 판매자식별자, int mobaele_setlhaodi, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.mobaele_setlhaodi = mobaele_setlhaodi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int mobaele_setlhaodi() { return mobaele_setlhaodi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<mobaele_Boleng> Didiriswa_lenaane = new ArrayList<mobaele_Boleng>();

    public void 발견(mobaele_Boleng mobaele_Boleng) {
        Didiriswa_lenaane.add(mobaele_Boleng);
    }

    public List<mobaele_Boleng> Didiriswa_lenaane() {
        return Collections.unmodifiableList(Didiriswa_lenaane);
    }

    public mobaele_Boleng batla_tsenyo(int 판매자식별자, int mobaele_setlhaodi) {
        for (mobaele_Boleng 후보 : Didiriswa_lenaane) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.mobaele_setlhaodi == mobaele_setlhaodi) {
                return 후보;
            }
        }
        return null;
    }
}

