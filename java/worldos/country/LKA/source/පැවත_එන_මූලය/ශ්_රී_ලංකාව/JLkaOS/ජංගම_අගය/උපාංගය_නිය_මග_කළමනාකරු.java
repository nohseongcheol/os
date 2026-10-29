// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ජංගම_අගය;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ජංගම_අගය 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class උපාංගය_නිය_මග_කළමනාකරු {
    public static final class ජංගම_අගය {
        private final int 판매자식별자;
        private final int ජංගම_හඳුන්වනය;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ජංගම_අගය(int 판매자식별자, int ජංගම_හඳුන්වනය, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ජංගම_හඳුන්වනය = ජංගම_හඳුන්වනය;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ජංගම_හඳුන්වනය() { return ජංගම_හඳුන්වනය; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ජංගම_අගය> උපාංග_ලැයිස්තුව = new ArrayList<ජංගම_අගය>();

    public void 발견(ජංගම_අගය ජංගම_අගය) {
        උපාංග_ලැයිස්තුව.add(ජංගම_අගය);
    }

    public List<ජංගම_අගය> උපාංග_ලැයිස්තුව() {
        return Collections.unmodifiableList(උපාංග_ලැයිස්තුව);
    }

    public ජංගම_අගය සොයන්න_පිවිසුම(int 판매자식별자, int ජංගම_හඳුන්වනය) {
        for (ජංගම_අගය 후보 : උපාංග_ලැයිස්තුව) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ජංගම_හඳුන්වනය == ජංගම_හඳුන්වනය) {
                return 후보;
            }
        }
        return null;
    }
}

