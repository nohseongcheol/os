// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.uidheam_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI uidheam_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class co_inneal_bus_manaidsear {
    public static final class uidheam_VALUE {
        private final int 판매자식별자;
        private final int uidheam_aithnichear;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public uidheam_VALUE(int 판매자식별자, int uidheam_aithnichear, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.uidheam_aithnichear = uidheam_aithnichear;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int uidheam_aithnichear() { return uidheam_aithnichear; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<uidheam_VALUE> Uidheaman_Liosta = new ArrayList<uidheam_VALUE>();

    public void 발견(uidheam_VALUE uidheam_VALUE) {
        Uidheaman_Liosta.add(uidheam_VALUE);
    }

    public List<uidheam_VALUE> Uidheaman_Liosta() {
        return Collections.unmodifiableList(Uidheaman_Liosta);
    }

    public uidheam_VALUE FIND_cur_a_steach(int 판매자식별자, int uidheam_aithnichear) {
        for (uidheam_VALUE 후보 : Uidheaman_Liosta) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.uidheam_aithnichear == uidheam_aithnichear) {
                return 후보;
            }
        }
        return null;
    }
}

