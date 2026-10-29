// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.התקן_ערך_e13f0cd9;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI התקן_ערך_e13f0cd9 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class עזר_אפיק_מנהל {
    public static final class התקן_ערך_e13f0cd9 {
        private final int ספק_מזהה;
        private final int התקן_מזהה;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public התקן_ערך_e13f0cd9(int ספק_מזהה, int התקן_מזהה, int 입출력바탕, int 개입중단번호) {
            this.ספק_מזהה = ספק_מזהה;
            this.התקן_מזהה = התקן_מזהה;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int ספק_מזהה() { return ספק_מזהה; }
        public int התקן_מזהה() { return התקן_מזהה; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<התקן_ערך_e13f0cd9> מכשירים_רשימה = new ArrayList<התקן_ערך_e13f0cd9>();

    public void 발견(התקן_ערך_e13f0cd9 התקן_ערך_e13f0cd9) {
        מכשירים_רשימה.add(התקן_ערך_e13f0cd9);
    }

    public List<התקן_ערך_e13f0cd9> מכשירים_רשימה() {
        return Collections.unmodifiableList(מכשירים_רשימה);
    }

    public התקן_ערך_e13f0cd9 חפש_ערך_832f7474(int ספק_מזהה, int התקן_מזהה) {
        for (התקן_ערך_e13f0cd9 후보 : מכשירים_רשימה) {
            if (후보.ספק_מזהה == ספק_מזהה && 후보.התקן_מזהה == התקן_מזהה) {
                return 후보;
            }
        }
        return null;
    }
}

