// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.آلو_قدر;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI آلو_قدر 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class لوازمات_بس_مئنيجر {
    public static final class آلو_قدر {
        private final int 판매자식별자;
        private final int آلو_سڃاڻپ_ڪندڙ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public آلو_قدر(int 판매자식별자, int آلو_سڃاڻپ_ڪندڙ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.آلو_سڃاڻپ_ڪندڙ = آلو_سڃاڻپ_ڪندڙ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int آلو_سڃاڻپ_ڪندڙ() { return آلو_سڃاڻپ_ڪندڙ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<آلو_قدر> آلا_فهرست = new ArrayList<آلو_قدر>();

    public void 발견(آلو_قدر آلو_قدر) {
        آلا_فهرست.add(آلو_قدر);
    }

    public List<آلو_قدر> آلا_فهرست() {
        return Collections.unmodifiableList(آلا_فهرست);
    }

    public آلو_قدر ڳوليو_داخلا(int 판매자식별자, int آلو_سڃاڻپ_ڪندڙ) {
        for (آلو_قدر 후보 : آلا_فهرست) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.آلو_سڃاڻپ_ڪندڙ == آلو_سڃاڻپ_ڪندڙ) {
                return 후보;
            }
        }
        return null;
    }
}

