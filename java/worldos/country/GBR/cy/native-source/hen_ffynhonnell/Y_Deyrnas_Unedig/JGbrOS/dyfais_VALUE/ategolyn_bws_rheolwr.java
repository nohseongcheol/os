// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.dyfais_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI dyfais_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ategolyn_bws_rheolwr {
    public static final class dyfais_VALUE {
        private final int 판매자식별자;
        private final int dyfais_dynodwr;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public dyfais_VALUE(int 판매자식별자, int dyfais_dynodwr, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.dyfais_dynodwr = dyfais_dynodwr;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int dyfais_dynodwr() { return dyfais_dynodwr; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<dyfais_VALUE> Dyfeisiau_Rhestr = new ArrayList<dyfais_VALUE>();

    public void 발견(dyfais_VALUE dyfais_VALUE) {
        Dyfeisiau_Rhestr.add(dyfais_VALUE);
    }

    public List<dyfais_VALUE> Dyfeisiau_Rhestr() {
        return Collections.unmodifiableList(Dyfeisiau_Rhestr);
    }

    public dyfais_VALUE FIND_cofnod(int 판매자식별자, int dyfais_dynodwr) {
        for (dyfais_VALUE 후보 : Dyfeisiau_Rhestr) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.dyfais_dynodwr == dyfais_dynodwr) {
                return 후보;
            }
        }
        return null;
    }
}

