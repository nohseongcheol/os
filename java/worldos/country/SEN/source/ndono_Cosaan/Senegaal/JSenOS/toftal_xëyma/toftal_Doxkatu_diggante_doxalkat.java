// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.toftal_xëyma;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI toftal_xëyma 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class toftal_Doxkatu_diggante_doxalkat {
    public static final class toftal_xëyma {
        private final int 판매자식별자;
        private final int toftal_raññeekaay;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public toftal_xëyma(int 판매자식별자, int toftal_raññeekaay, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.toftal_raññeekaay = toftal_raññeekaay;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int toftal_raññeekaay() { return toftal_raññeekaay; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<toftal_xëyma> Toftalu_lim = new ArrayList<toftal_xëyma>();

    public void 발견(toftal_xëyma toftal_xëyma) {
        Toftalu_lim.add(toftal_xëyma);
    }

    public List<toftal_xëyma> Toftalu_lim() {
        return Collections.unmodifiableList(Toftalu_lim);
    }

    public toftal_xëyma seet_dugal_xabaar(int 판매자식별자, int toftal_raññeekaay) {
        for (toftal_xëyma 후보 : Toftalu_lim) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.toftal_raññeekaay == toftal_raññeekaay) {
                return 후보;
            }
        }
        return null;
    }
}

