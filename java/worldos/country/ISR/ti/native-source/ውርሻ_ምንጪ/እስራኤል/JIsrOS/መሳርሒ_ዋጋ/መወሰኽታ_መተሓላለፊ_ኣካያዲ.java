// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.መሳርሒ_ዋጋ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI መሳርሒ_ዋጋ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class መወሰኽታ_መተሓላለፊ_ኣካያዲ {
    public static final class መሳርሒ_ዋጋ {
        private final int 판매자식별자;
        private final int መሳርሒ_ፈላዪ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public መሳርሒ_ዋጋ(int 판매자식별자, int መሳርሒ_ፈላዪ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.መሳርሒ_ፈላዪ = መሳርሒ_ፈላዪ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int መሳርሒ_ፈላዪ() { return መሳርሒ_ፈላዪ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<መሳርሒ_ዋጋ> መሳርሕታት_ዝርዝር = new ArrayList<መሳርሒ_ዋጋ>();

    public void 발견(መሳርሒ_ዋጋ መሳርሒ_ዋጋ) {
        መሳርሕታት_ዝርዝር.add(መሳርሒ_ዋጋ);
    }

    public List<መሳርሒ_ዋጋ> መሳርሕታት_ዝርዝር() {
        return Collections.unmodifiableList(መሳርሕታት_ዝርዝር);
    }

    public መሳርሒ_ዋጋ ርኸብ_ምእታው(int 판매자식별자, int መሳርሒ_ፈላዪ) {
        for (መሳርሒ_ዋጋ 후보 : መሳርሕታት_ዝርዝር) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.መሳርሒ_ፈላዪ == መሳርሒ_ፈላዪ) {
                return 후보;
            }
        }
        return null;
    }
}

