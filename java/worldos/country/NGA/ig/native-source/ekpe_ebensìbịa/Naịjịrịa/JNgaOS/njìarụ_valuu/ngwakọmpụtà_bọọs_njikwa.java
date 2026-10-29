// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.njìarụ_valuu;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI njìarụ_valuu 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ngwakọmpụtà_bọọs_njikwa {
    public static final class njìarụ_valuu {
        private final int 판매자식별자;
        private final int njìarụ_ihe_nkọwapụta;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public njìarụ_valuu(int 판매자식별자, int njìarụ_ihe_nkọwapụta, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.njìarụ_ihe_nkọwapụta = njìarụ_ihe_nkọwapụta;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int njìarụ_ihe_nkọwapụta() { return njìarụ_ihe_nkọwapụta; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<njìarụ_valuu> Njìarụ_ndepụta = new ArrayList<njìarụ_valuu>();

    public void 발견(njìarụ_valuu njìarụ_valuu) {
        Njìarụ_ndepụta.add(njìarụ_valuu);
    }

    public List<njìarụ_valuu> Njìarụ_ndepụta() {
        return Collections.unmodifiableList(Njìarụ_ndepụta);
    }

    public njìarụ_valuu chọta_ndebà(int 판매자식별자, int njìarụ_ihe_nkọwapụta) {
        for (njìarụ_valuu 후보 : Njìarụ_ndepụta) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.njìarụ_ihe_nkọwapụta == njìarụ_ihe_nkọwapụta) {
                return 후보;
            }
        }
        return null;
    }
}

