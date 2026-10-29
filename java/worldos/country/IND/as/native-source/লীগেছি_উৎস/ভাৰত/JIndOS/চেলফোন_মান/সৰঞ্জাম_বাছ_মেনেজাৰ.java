// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.চেলফোন_মান;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI চেলফোন_মান 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class সৰঞ্জাম_বাছ_মেনেজাৰ {
    public static final class চেলফোন_মান {
        private final int 판매자식별자;
        private final int চেলফোন_চিনাক্তকাৰী;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public চেলফোন_মান(int 판매자식별자, int চেলফোন_চিনাক্তকাৰী, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.চেলফোন_চিনাক্তকাৰী = চেলফোন_চিনাক্তকাৰী;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int চেলফোন_চিনাক্তকাৰী() { return চেলফোন_চিনাক্তকাৰী; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<চেলফোন_মান> ডিভাইচ_সূচী = new ArrayList<চেলফোন_মান>();

    public void 발견(চেলফোন_মান চেলফোন_মান) {
        ডিভাইচ_সূচী.add(চেলফোন_মান);
    }

    public List<চেলফোন_মান> ডিভাইচ_সূচী() {
        return Collections.unmodifiableList(ডিভাইচ_সূচী);
    }

    public চেলফোন_মান বিচাৰক_প্রবিষ্ট(int 판매자식별자, int চেলফোন_চিনাক্তকাৰী) {
        for (চেলফোন_মান 후보 : ডিভাইচ_সূচী) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.চেলফোন_চিনাক্তকাৰী == চেলফোন_চিনাক্তকাৰী) {
                return 후보;
            }
        }
        return null;
    }
}

