// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.mowbajl_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mowbajl_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aċċessorju_bus_maniġer {
    public static final class mowbajl_VALUE {
        private final int 판매자식별자;
        private final int mowbajl_identifikatur;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public mowbajl_VALUE(int 판매자식별자, int mowbajl_identifikatur, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.mowbajl_identifikatur = mowbajl_identifikatur;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int mowbajl_identifikatur() { return mowbajl_identifikatur; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<mowbajl_VALUE> Tagħmir_Lista = new ArrayList<mowbajl_VALUE>();

    public void 발견(mowbajl_VALUE mowbajl_VALUE) {
        Tagħmir_Lista.add(mowbajl_VALUE);
    }

    public List<mowbajl_VALUE> Tagħmir_Lista() {
        return Collections.unmodifiableList(Tagħmir_Lista);
    }

    public mowbajl_VALUE sab_entrata(int 판매자식별자, int mowbajl_identifikatur) {
        for (mowbajl_VALUE 후보 : Tagħmir_Lista) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.mowbajl_identifikatur == mowbajl_identifikatur) {
                return 후보;
            }
        }
        return null;
    }
}

