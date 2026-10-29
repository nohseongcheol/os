// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.ડિવાઇસ_મૂલ્ય;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ડિવાઇસ_મૂલ્ય 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class એસેસરી_બસ_પ્રબંધક {
    public static final class ડિવાઇસ_મૂલ્ય {
        private final int 판매자식별자;
        private final int ડિવાઇસ_ઓળખકર્તા;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ડિવાઇસ_મૂલ્ય(int 판매자식별자, int ડિવાઇસ_ઓળખકર્તા, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ડિવાઇસ_ઓળખકર્તા = ડિવાઇસ_ઓળખકર્તા;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ડિવાઇસ_ઓળખકર્તા() { return ડિવાઇસ_ઓળખકર્તા; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ડિવાઇસ_મૂલ્ય> ઉપકરણો_સૂચી = new ArrayList<ડિવાઇસ_મૂલ્ય>();

    public void 발견(ડિવાઇસ_મૂલ્ય ડિવાઇસ_મૂલ્ય) {
        ઉપકરણો_સૂચી.add(ડિવાઇસ_મૂલ્ય);
    }

    public List<ડિવાઇસ_મૂલ્ય> ઉપકરણો_સૂચી() {
        return Collections.unmodifiableList(ઉપકરણો_સૂચી);
    }

    public ડિવાઇસ_મૂલ્ય શોધો_પ્રવેશ(int 판매자식별자, int ડિવાઇસ_ઓળખકર્તા) {
        for (ડિવાઇસ_મૂલ્ય 후보 : ઉપકરણો_સૂચી) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ડિવાઇસ_ઓળખકર્તા == ડિવાઇસ_ઓળખકર્તા) {
                return 후보;
            }
        }
        return null;
    }
}

