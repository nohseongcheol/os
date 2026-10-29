// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.peranti_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI peranti_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aksesori_bas_pengurus {
    public static final class peranti_VALUE {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public peranti_VALUE(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.장치식별자 = 장치식별자;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int 장치식별자() { return 장치식별자; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<peranti_VALUE> Peranti_Senarai = new ArrayList<peranti_VALUE>();

    public void 발견(peranti_VALUE peranti_VALUE) {
        Peranti_Senarai.add(peranti_VALUE);
    }

    public List<peranti_VALUE> Peranti_Senarai() {
        return Collections.unmodifiableList(Peranti_Senarai);
    }

    public peranti_VALUE Cari_pemasukan(int 판매자식별자, int 장치식별자) {
        for (peranti_VALUE 후보 : Peranti_Senarai) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

