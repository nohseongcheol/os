// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.serulaalü_ajutuu;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI serulaalü_ajutuu 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class serulaalü_ajutuu {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public serulaalü_ajutuu(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
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

    private final List<serulaalü_ajutuu> 장치들 = new ArrayList<serulaalü_ajutuu>();

    public void 발견(serulaalü_ajutuu serulaalü_ajutuu) {
        장치들.add(serulaalü_ajutuu);
    }

    public List<serulaalü_ajutuu> 장치들() {
        return Collections.unmodifiableList(장치들);
    }

    public serulaalü_ajutuu 찾기(int 판매자식별자, int 장치식별자) {
        for (serulaalü_ajutuu 후보 : 장치들) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

