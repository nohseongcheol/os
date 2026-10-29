// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkmenistan.JTkmOS.enjam_baha;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI enjam_baha 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class kömekçi_enjam_şina_iş_dolandyryjy {
    public static final class enjam_baha {
        private final int 판매자식별자;
        private final int enjam_tanaýjy;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public enjam_baha(int 판매자식별자, int enjam_tanaýjy, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.enjam_tanaýjy = enjam_tanaýjy;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int enjam_tanaýjy() { return enjam_tanaýjy; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<enjam_baha> Enjamlar_Sanaw = new ArrayList<enjam_baha>();

    public void 발견(enjam_baha enjam_baha) {
        Enjamlar_Sanaw.add(enjam_baha);
    }

    public List<enjam_baha> Enjamlar_Sanaw() {
        return Collections.unmodifiableList(Enjamlar_Sanaw);
    }

    public enjam_baha tap_girizmeklik(int 판매자식별자, int enjam_tanaýjy) {
        for (enjam_baha 후보 : Enjamlar_Sanaw) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.enjam_tanaýjy == enjam_tanaýjy) {
                return 후보;
            }
        }
        return null;
    }
}

