// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.seade_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI seade_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class seade_VALUE {
        private final int hankija_identifikaator;
        private final int seade_identifikaator;
        private final int 입출력바탕;
        private final int IRQ_number;

        public seade_VALUE(int hankija_identifikaator, int seade_identifikaator, int 입출력바탕, int IRQ_number) {
            this.hankija_identifikaator = hankija_identifikaator;
            this.seade_identifikaator = seade_identifikaator;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_number = IRQ_number;
        }

        public int hankija_identifikaator() { return hankija_identifikaator; }
        public int seade_identifikaator() { return seade_identifikaator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_number() { return IRQ_number; }
    }

    private final List<seade_VALUE> Seadmed_Loend = new ArrayList<seade_VALUE>();

    public void 발견(seade_VALUE seade_VALUE) {
        Seadmed_Loend.add(seade_VALUE);
    }

    public List<seade_VALUE> Seadmed_Loend() {
        return Collections.unmodifiableList(Seadmed_Loend);
    }

    public seade_VALUE FIND_kirje(int hankija_identifikaator, int seade_identifikaator) {
        for (seade_VALUE 후보 : Seadmed_Loend) {
            if (후보.hankija_identifikaator == hankija_identifikaator && 후보.seade_identifikaator == seade_identifikaator) {
                return 후보;
            }
        }
        return null;
    }
}

