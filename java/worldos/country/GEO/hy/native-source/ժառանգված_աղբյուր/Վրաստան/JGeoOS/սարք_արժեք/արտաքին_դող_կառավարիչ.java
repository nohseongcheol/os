// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Վրաստան.JGeoOS.սարք_արժեք;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI սարք_արժեք 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class արտաքին_դող_կառավարիչ {
    public static final class սարք_արժեք {
        private final int 판매자식별자;
        private final int սարք_նույնացուցիչ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public սարք_արժեք(int 판매자식별자, int սարք_նույնացուցիչ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.սարք_նույնացուցիչ = սարք_նույնացուցիչ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int սարք_նույնացուցիչ() { return սարք_նույնացուցիչ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<սարք_արժեք> Սարքեր_Ցուցակ = new ArrayList<սարք_արժեք>();

    public void 발견(սարք_արժեք սարք_արժեք) {
        Սարքեր_Ցուցակ.add(սարք_արժեք);
    }

    public List<սարք_արժեք> Սարքեր_Ցուցակ() {
        return Collections.unmodifiableList(Սարքեր_Ցուցակ);
    }

    public սարք_արժեք գտնել_մուտքագրում(int 판매자식별자, int սարք_նույնացուցիչ) {
        for (սարք_արժեք 후보 : Սարքեր_Ցուցակ) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.սարք_նույնացուցիչ == սարք_նույնացուցիչ) {
                return 후보;
            }
        }
        return null;
    }
}

