// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.పరికరం_మూల్యం;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI పరికరం_మూల్యం 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class సాధకం_బస్_కార్యనిర్వాహి {
    public static final class పరికరం_మూల్యం {
        private final int విక్రేత_ఐడెంటిఫయర్;
        private final int పరికరం_ఐడెంటిఫయర్;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public పరికరం_మూల్యం(int విక్రేత_ఐడెంటిఫయర్, int పరికరం_ఐడెంటిఫయర్, int 입출력바탕, int 개입중단번호) {
            this.విక్రేత_ఐడెంటిఫయర్ = విక్రేత_ఐడెంటిఫయర్;
            this.పరికరం_ఐడెంటిఫయర్ = పరికరం_ఐడెంటిఫయర్;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int విక్రేత_ఐడెంటిఫయర్() { return విక్రేత_ఐడెంటిఫయర్; }
        public int పరికరం_ఐడెంటిఫయర్() { return పరికరం_ఐడెంటిఫయర్; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<పరికరం_మూల్యం> పరికరాలు_జాబితా = new ArrayList<పరికరం_మూల్యం>();

    public void 발견(పరికరం_మూల్యం పరికరం_మూల్యం) {
        పరికరాలు_జాబితా.add(పరికరం_మూల్యం);
    }

    public List<పరికరం_మూల్యం> పరికరాలు_జాబితా() {
        return Collections.unmodifiableList(పరికరాలు_జాబితా);
    }

    public పరికరం_మూల్యం వెతుకు_ప్రవేశం(int విక్రేత_ఐడెంటిఫయర్, int పరికరం_ఐడెంటిఫయర్) {
        for (పరికరం_మూల్యం 후보 : పరికరాలు_జాబితా) {
            if (후보.విక్రేత_ఐడెంటిఫయర్ == విక్రేత_ఐడెంటిఫయర్ && 후보.పరికరం_ఐడెంటిఫయర్ == పరికరం_ఐడెంటిఫయర్) {
                return 후보;
            }
        }
        return null;
    }
}

