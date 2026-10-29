// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.гар_утас_утга;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI гар_утас_утга 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class гар_утас_утга {
        private final int 판매자식별자;
        private final int гар_утас_танигч;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public гар_утас_утга(int 판매자식별자, int гар_утас_танигч, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.гар_утас_танигч = гар_утас_танигч;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int гар_утас_танигч() { return гар_утас_танигч; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<гар_утас_утга> Төхөөрөмжүүд_Жагсаалт = new ArrayList<гар_утас_утга>();

    public void 발견(гар_утас_утга гар_утас_утга) {
        Төхөөрөмжүүд_Жагсаалт.add(гар_утас_утга);
    }

    public List<гар_утас_утга> Төхөөрөмжүүд_Жагсаалт() {
        return Collections.unmodifiableList(Төхөөрөмжүүд_Жагсаалт);
    }

    public гар_утас_утга хайх_оролт(int 판매자식별자, int гар_утас_танигч) {
        for (гар_утас_утга 후보 : Төхөөрөмжүүд_Жагсаалт) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.гар_утас_танигч == гар_утас_танигч) {
                return 후보;
            }
        }
        return null;
    }
}

