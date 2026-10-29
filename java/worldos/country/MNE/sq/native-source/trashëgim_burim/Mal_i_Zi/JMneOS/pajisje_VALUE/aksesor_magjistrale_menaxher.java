// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mal_i_Zi.JMneOS.pajisje_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI pajisje_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aksesor_magjistrale_menaxher {
    public static final class pajisje_VALUE {
        private final int shitës_identifikues;
        private final int pajisje_identifikues;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public pajisje_VALUE(int shitës_identifikues, int pajisje_identifikues, int 입출력바탕, int 개입중단번호) {
            this.shitës_identifikues = shitës_identifikues;
            this.pajisje_identifikues = pajisje_identifikues;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int shitës_identifikues() { return shitës_identifikues; }
        public int pajisje_identifikues() { return pajisje_identifikues; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<pajisje_VALUE> Pajisjet_Listë = new ArrayList<pajisje_VALUE>();

    public void 발견(pajisje_VALUE pajisje_VALUE) {
        Pajisjet_Listë.add(pajisje_VALUE);
    }

    public List<pajisje_VALUE> Pajisjet_Listë() {
        return Collections.unmodifiableList(Pajisjet_Listë);
    }

    public pajisje_VALUE FIND_futje(int shitës_identifikues, int pajisje_identifikues) {
        for (pajisje_VALUE 후보 : Pajisjet_Listë) {
            if (후보.shitës_identifikues == shitës_identifikues && 후보.pajisje_identifikues == pajisje_identifikues) {
                return 후보;
            }
        }
        return null;
    }
}

