// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ايران.JIrnOS.وزله_ارزښت;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI وزله_ارزښت 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class وزله_ارزښت {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public وزله_ارزښت(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
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

    private final List<وزله_ارزښت> 장치들 = new ArrayList<وزله_ارزښت>();

    public void 발견(وزله_ارزښت وزله_ارزښت) {
        장치들.add(وزله_ارزښت);
    }

    public List<وزله_ارزښت> 장치들() {
        return Collections.unmodifiableList(장치들);
    }

    public وزله_ارزښت 찾기(int 판매자식별자, int 장치식별자) {
        for (وزله_ارزښت 후보 : 장치들) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

