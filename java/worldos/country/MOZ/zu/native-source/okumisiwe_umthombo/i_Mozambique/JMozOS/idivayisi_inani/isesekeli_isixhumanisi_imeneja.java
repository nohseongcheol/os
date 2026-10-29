// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.idivayisi_inani;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI idivayisi_inani 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class isesekeli_isixhumanisi_imeneja {
    public static final class idivayisi_inani {
        private final int 판매자식별자;
        private final int idivayisi_isivezi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public idivayisi_inani(int 판매자식별자, int idivayisi_isivezi, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.idivayisi_isivezi = idivayisi_isivezi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int idivayisi_isivezi() { return idivayisi_isivezi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<idivayisi_inani> Amadivayisi_Uhlu = new ArrayList<idivayisi_inani>();

    public void 발견(idivayisi_inani idivayisi_inani) {
        Amadivayisi_Uhlu.add(idivayisi_inani);
    }

    public List<idivayisi_inani> Amadivayisi_Uhlu() {
        return Collections.unmodifiableList(Amadivayisi_Uhlu);
    }

    public idivayisi_inani thola_okufakwayo(int 판매자식별자, int idivayisi_isivezi) {
        for (idivayisi_inani 후보 : Amadivayisi_Uhlu) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.idivayisi_isivezi == idivayisi_isivezi) {
                return 후보;
            }
        }
        return null;
    }
}

