// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ganaa.JGhaOS.kaɓirgal_njaru;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI kaɓirgal_njaru 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class gollirgal_biis_kisnoowo {
    public static final class kaɓirgal_njaru {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public kaɓirgal_njaru(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
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

    private final List<kaɓirgal_njaru> Kaɓirɗi_Doggol = new ArrayList<kaɓirgal_njaru>();

    public void 발견(kaɓirgal_njaru kaɓirgal_njaru) {
        Kaɓirɗi_Doggol.add(kaɓirgal_njaru);
    }

    public List<kaɓirgal_njaru> Kaɓirɗi_Doggol() {
        return Collections.unmodifiableList(Kaɓirɗi_Doggol);
    }

    public kaɓirgal_njaru yiylaade_naatnugol(int 판매자식별자, int 장치식별자) {
        for (kaɓirgal_njaru 후보 : Kaɓirɗi_Doggol) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

