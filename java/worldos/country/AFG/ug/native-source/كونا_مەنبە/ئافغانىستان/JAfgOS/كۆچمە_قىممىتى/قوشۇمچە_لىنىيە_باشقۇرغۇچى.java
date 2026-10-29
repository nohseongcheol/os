// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.كۆچمە_قىممىتى;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI كۆچمە_قىممىتى 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class قوشۇمچە_لىنىيە_باشقۇرغۇچى {
    public static final class كۆچمە_قىممىتى {
        private final int 판매자식별자;
        private final int كۆچمە_پەرقلەندۈرگۈچ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public كۆچمە_قىممىتى(int 판매자식별자, int كۆچمە_پەرقلەندۈرگۈچ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.كۆچمە_پەرقلەندۈرگۈچ = كۆچمە_پەرقلەندۈرگۈچ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int كۆچمە_پەرقلەندۈرگۈچ() { return كۆچمە_پەرقلەندۈرگۈچ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<كۆچمە_قىممىتى> ئۈسكۈنىلەر_تىزىم = new ArrayList<كۆچمە_قىممىتى>();

    public void 발견(كۆچمە_قىممىتى كۆچمە_قىممىتى) {
        ئۈسكۈنىلەر_تىزىم.add(كۆچمە_قىممىتى);
    }

    public List<كۆچمە_قىممىتى> ئۈسكۈنىلەر_تىزىم() {
        return Collections.unmodifiableList(ئۈسكۈنىلەر_تىزىم);
    }

    public كۆچمە_قىممىتى ئىزدەش_كىرگۈزۈش(int 판매자식별자, int كۆچمە_پەرقلەندۈرگۈچ) {
        for (كۆچمە_قىممىتى 후보 : ئۈسكۈنىلەر_تىزىم) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.كۆچمە_پەرقلەندۈرگۈچ == كۆچمە_پەرقلەندۈرگۈچ) {
                return 후보;
            }
        }
        return null;
    }
}

