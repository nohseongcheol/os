// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଡିଭାଇସ_ମୂଲ୍ୟ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ଡିଭାଇସ_ମୂଲ୍ୟ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ସରଞ୍ଜାମ_ବସ୍_ପରିଚାଳକ {
    public static final class ଡିଭାଇସ_ମୂଲ୍ୟ {
        private final int 판매자식별자;
        private final int ଡିଭାଇସ_ପରିଚାୟକ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ଡିଭାଇସ_ମୂଲ୍ୟ(int 판매자식별자, int ଡିଭାଇସ_ପରିଚାୟକ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ଡିଭାଇସ_ପରିଚାୟକ = ଡିଭାଇସ_ପରିଚାୟକ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ଡିଭାଇସ_ପରିଚାୟକ() { return ଡିଭାଇସ_ପରିଚାୟକ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ଡିଭାଇସ_ମୂଲ୍ୟ> ଡିଭାଇସ୍_ସମୂହ_ତାଲିକା = new ArrayList<ଡିଭାଇସ_ମୂଲ୍ୟ>();

    public void 발견(ଡିଭାଇସ_ମୂଲ୍ୟ ଡିଭାଇସ_ମୂଲ୍ୟ) {
        ଡିଭାଇସ୍_ସମୂହ_ତାଲିକା.add(ଡିଭାଇସ_ମୂଲ୍ୟ);
    }

    public List<ଡିଭାଇସ_ମୂଲ୍ୟ> ଡିଭାଇସ୍_ସମୂହ_ତାଲିକା() {
        return Collections.unmodifiableList(ଡିଭାଇସ୍_ସମୂହ_ତାଲିକା);
    }

    public ଡିଭାଇସ_ମୂଲ୍ୟ ଖୋଜିବା_ଏଣ୍ଟ୍ରି(int 판매자식별자, int ଡିଭାଇସ_ପରିଚାୟକ) {
        for (ଡିଭାଇସ_ମୂଲ୍ୟ 후보 : ଡିଭାଇସ୍_ସମୂହ_ତାଲିକା) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ଡିଭାଇସ_ପରିଚାୟକ == ଡିଭାଇସ_ପରିଚାୟକ) {
                return 후보;
            }
        }
        return null;
    }
}

