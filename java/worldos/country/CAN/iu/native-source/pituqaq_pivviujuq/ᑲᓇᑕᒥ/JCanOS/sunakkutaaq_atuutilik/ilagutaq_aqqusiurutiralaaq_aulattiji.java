// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.sunakkutaaq_atuutilik;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI sunakkutaaq_atuutilik 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ilagutaq_aqqusiurutiralaaq_aulattiji {
    public static final class sunakkutaaq_atuutilik {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public sunakkutaaq_atuutilik(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
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

    private final List<sunakkutaaq_atuutilik> Sunakkutaat_Titiqpalliagaq = new ArrayList<sunakkutaaq_atuutilik>();

    public void 발견(sunakkutaaq_atuutilik sunakkutaaq_atuutilik) {
        Sunakkutaat_Titiqpalliagaq.add(sunakkutaaq_atuutilik);
    }

    public List<sunakkutaaq_atuutilik> Sunakkutaat_Titiqpalliagaq() {
        return Collections.unmodifiableList(Sunakkutaat_Titiqpalliagaq);
    }

    public sunakkutaaq_atuutilik nanili_Iliniku(int 판매자식별자, int 장치식별자) {
        for (sunakkutaaq_atuutilik 후보 : Sunakkutaat_Titiqpalliagaq) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

