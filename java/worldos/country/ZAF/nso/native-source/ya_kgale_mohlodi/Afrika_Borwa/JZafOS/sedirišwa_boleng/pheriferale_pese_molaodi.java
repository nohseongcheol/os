// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.sedirišwa_boleng;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI sedirišwa_boleng 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class pheriferale_pese_molaodi {
    public static final class sedirišwa_boleng {
        private final int 판매자식별자;
        private final int sedirišwa_sešupi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public sedirišwa_boleng(int 판매자식별자, int sedirišwa_sešupi, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.sedirišwa_sešupi = sedirišwa_sešupi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int sedirišwa_sešupi() { return sedirišwa_sešupi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<sedirišwa_boleng> Didirišwa_Lenaneo = new ArrayList<sedirišwa_boleng>();

    public void 발견(sedirišwa_boleng sedirišwa_boleng) {
        Didirišwa_Lenaneo.add(sedirišwa_boleng);
    }

    public List<sedirišwa_boleng> Didirišwa_Lenaneo() {
        return Collections.unmodifiableList(Didirišwa_Lenaneo);
    }

    public sedirišwa_boleng hwetša_go_tsenya_tshedimošo(int 판매자식별자, int sedirišwa_sešupi) {
        for (sedirišwa_boleng 후보 : Didirišwa_Lenaneo) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.sedirišwa_sešupi == sedirišwa_sešupi) {
                return 후보;
            }
        }
        return null;
    }
}

