// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.pūkoro_uara;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI pūkoro_uara 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class apatoko_pahi_pouwhakahaere {
    public static final class pūkoro_uara {
        private final int 판매자식별자;
        private final int pūkoro_pūtāutu;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public pūkoro_uara(int 판매자식별자, int pūkoro_pūtāutu, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.pūkoro_pūtāutu = pūkoro_pūtāutu;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int pūkoro_pūtāutu() { return pūkoro_pūtāutu; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<pūkoro_uara> Pūrere_Rārangi = new ArrayList<pūkoro_uara>();

    public void 발견(pūkoro_uara pūkoro_uara) {
        Pūrere_Rārangi.add(pūkoro_uara);
    }

    public List<pūkoro_uara> Pūrere_Rārangi() {
        return Collections.unmodifiableList(Pūrere_Rārangi);
    }

    public pūkoro_uara FIND_tāurunga(int 판매자식별자, int pūkoro_pūtāutu) {
        for (pūkoro_uara 후보 : Pūrere_Rārangi) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.pūkoro_pūtāutu == pūkoro_pūtāutu) {
                return 후보;
            }
        }
        return null;
    }
}

