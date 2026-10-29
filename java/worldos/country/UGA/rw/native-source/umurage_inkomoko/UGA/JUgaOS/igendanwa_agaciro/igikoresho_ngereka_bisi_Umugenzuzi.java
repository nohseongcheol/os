// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package UGA.JUgaOS.igendanwa_agaciro;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI igendanwa_agaciro 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class igikoresho_ngereka_bisi_Umugenzuzi {
    public static final class igendanwa_agaciro {
        private final int 판매자식별자;
        private final int igendanwa_indanga;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public igendanwa_agaciro(int 판매자식별자, int igendanwa_indanga, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.igendanwa_indanga = igendanwa_indanga;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int igendanwa_indanga() { return igendanwa_indanga; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<igendanwa_agaciro> Ibikoresho_Urutonde = new ArrayList<igendanwa_agaciro>();

    public void 발견(igendanwa_agaciro igendanwa_agaciro) {
        Ibikoresho_Urutonde.add(igendanwa_agaciro);
    }

    public List<igendanwa_agaciro> Ibikoresho_Urutonde() {
        return Collections.unmodifiableList(Ibikoresho_Urutonde);
    }

    public igendanwa_agaciro gushaka_icyinjizwa(int 판매자식별자, int igendanwa_indanga) {
        for (igendanwa_agaciro 후보 : Ibikoresho_Urutonde) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.igendanwa_indanga == igendanwa_indanga) {
                return 후보;
            }
        }
        return null;
    }
}

