// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中國.JChnOS.장치;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI 장치 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class 장치 {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public 장치(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
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

    private final List<장치> 장치들 = new ArrayList<장치>();

    public void 발견(장치 장치) {
        장치들.add(장치);
    }

    public List<장치> 장치들() {
        return Collections.unmodifiableList(장치들);
    }

    public 장치 찾기(int 판매자식별자, int 장치식별자) {
        for (장치 후보 : 장치들) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

