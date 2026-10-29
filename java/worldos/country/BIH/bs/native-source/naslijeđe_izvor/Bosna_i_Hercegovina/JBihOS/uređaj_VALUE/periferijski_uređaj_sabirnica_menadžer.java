// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.uređaj_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI uređaj_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class periferijski_uređaj_sabirnica_menadžer {
    public static final class uređaj_VALUE {
        private final int prodavač_identifikator;
        private final int uređaj_identifikator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public uređaj_VALUE(int prodavač_identifikator, int uređaj_identifikator, int 입출력바탕, int 개입중단번호) {
            this.prodavač_identifikator = prodavač_identifikator;
            this.uređaj_identifikator = uređaj_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int prodavač_identifikator() { return prodavač_identifikator; }
        public int uređaj_identifikator() { return uređaj_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<uređaj_VALUE> Uređaji_spisak = new ArrayList<uređaj_VALUE>();

    public void 발견(uređaj_VALUE uređaj_VALUE) {
        Uređaji_spisak.add(uređaj_VALUE);
    }

    public List<uređaj_VALUE> Uređaji_spisak() {
        return Collections.unmodifiableList(Uređaji_spisak);
    }

    public uređaj_VALUE FIND_unos(int prodavač_identifikator, int uređaj_identifikator) {
        for (uređaj_VALUE 후보 : Uređaji_spisak) {
            if (후보.prodavač_identifikator == prodavač_identifikator && 후보.uređaj_identifikator == uređaj_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

