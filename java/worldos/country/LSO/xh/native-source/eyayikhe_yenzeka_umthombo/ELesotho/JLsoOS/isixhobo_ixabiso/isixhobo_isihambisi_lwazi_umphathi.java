// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.isixhobo_ixabiso;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI isixhobo_ixabiso 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class isixhobo_isihambisi_lwazi_umphathi {
    public static final class isixhobo_ixabiso {
        private final int 판매자식별자;
        private final int isixhobo_isalathisi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public isixhobo_ixabiso(int 판매자식별자, int isixhobo_isalathisi, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.isixhobo_isalathisi = isixhobo_isalathisi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int isixhobo_isalathisi() { return isixhobo_isalathisi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<isixhobo_ixabiso> Izixhobo_uludwe = new ArrayList<isixhobo_ixabiso>();

    public void 발견(isixhobo_ixabiso isixhobo_ixabiso) {
        Izixhobo_uludwe.add(isixhobo_ixabiso);
    }

    public List<isixhobo_ixabiso> Izixhobo_uludwe() {
        return Collections.unmodifiableList(Izixhobo_uludwe);
    }

    public isixhobo_ixabiso fumana_ufako_nkcukacha(int 판매자식별자, int isixhobo_isalathisi) {
        for (isixhobo_ixabiso 후보 : Izixhobo_uludwe) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.isixhobo_isalathisi == isixhobo_isalathisi) {
                return 후보;
            }
        }
        return null;
    }
}

