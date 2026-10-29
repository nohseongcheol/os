// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azərbaycan.JAzeOS.cihaz_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI cihaz_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class əlavə_qurğu_şin_menecer {
    public static final class cihaz_VALUE {
        private final int təchizatçı_identifikator;
        private final int cihaz_identifikator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public cihaz_VALUE(int təchizatçı_identifikator, int cihaz_identifikator, int 입출력바탕, int 개입중단번호) {
            this.təchizatçı_identifikator = təchizatçı_identifikator;
            this.cihaz_identifikator = cihaz_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int təchizatçı_identifikator() { return təchizatçı_identifikator; }
        public int cihaz_identifikator() { return cihaz_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<cihaz_VALUE> Cihazlar_Siyahı = new ArrayList<cihaz_VALUE>();

    public void 발견(cihaz_VALUE cihaz_VALUE) {
        Cihazlar_Siyahı.add(cihaz_VALUE);
    }

    public List<cihaz_VALUE> Cihazlar_Siyahı() {
        return Collections.unmodifiableList(Cihazlar_Siyahı);
    }

    public cihaz_VALUE FIND_daxiletmə(int təchizatçı_identifikator, int cihaz_identifikator) {
        for (cihaz_VALUE 후보 : Cihazlar_Siyahı) {
            if (후보.təchizatçı_identifikator == təchizatçı_identifikator && 후보.cihaz_identifikator == cihaz_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

