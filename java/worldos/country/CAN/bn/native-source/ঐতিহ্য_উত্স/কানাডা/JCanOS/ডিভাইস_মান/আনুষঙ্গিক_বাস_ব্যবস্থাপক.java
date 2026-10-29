// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package কানাডা.JCanOS.ডিভাইস_মান;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ডিভাইস_মান 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class আনুষঙ্গিক_বাস_ব্যবস্থাপক {
    public static final class ডিভাইস_মান {
        private final int বিক্রেতা_সনাক্তকারী;
        private final int ডিভাইস_সনাক্তকারী;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ডিভাইস_মান(int বিক্রেতা_সনাক্তকারী, int ডিভাইস_সনাক্তকারী, int 입출력바탕, int 개입중단번호) {
            this.বিক্রেতা_সনাক্তকারী = বিক্রেতা_সনাক্তকারী;
            this.ডিভাইস_সনাক্তকারী = ডিভাইস_সনাক্তকারী;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int বিক্রেতা_সনাক্তকারী() { return বিক্রেতা_সনাক্তকারী; }
        public int ডিভাইস_সনাক্তকারী() { return ডিভাইস_সনাক্তকারী; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ডিভাইস_মান> ডিভাইস_তালিকা = new ArrayList<ডিভাইস_মান>();

    public void 발견(ডিভাইস_মান ডিভাইস_মান) {
        ডিভাইস_তালিকা.add(ডিভাইস_মান);
    }

    public List<ডিভাইস_মান> ডিভাইস_তালিকা() {
        return Collections.unmodifiableList(ডিভাইস_তালিকা);
    }

    public ডিভাইস_মান খোঁজা_ভুক্তি(int বিক্রেতা_সনাক্তকারী, int ডিভাইস_সনাক্তকারী) {
        for (ডিভাইস_মান 후보 : ডিভাইস_তালিকা) {
            if (후보.বিক্রেতা_সনাক্তকারী == বিক্রেতা_সনাক্তকারী && 후보.ডিভাইস_সনাক্তকারী == ডিভাইস_সনাক্তকারী) {
                return 후보;
            }
        }
        return null;
    }
}

