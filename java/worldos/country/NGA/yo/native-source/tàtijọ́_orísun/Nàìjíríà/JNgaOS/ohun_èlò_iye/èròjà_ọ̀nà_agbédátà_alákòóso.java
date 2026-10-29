// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.ohun_èlò_iye;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ohun_èlò_iye 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class èròjà_ọ̀nà_agbédátà_alákòóso {
    public static final class ohun_èlò_iye {
        private final int 판매자식별자;
        private final int ohun_èlò_Àfidámọ̀;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ohun_èlò_iye(int 판매자식별자, int ohun_èlò_Àfidámọ̀, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ohun_èlò_Àfidámọ̀ = ohun_èlò_Àfidámọ̀;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ohun_èlò_Àfidámọ̀() { return ohun_èlò_Àfidámọ̀; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ohun_èlò_iye> Ohun_èlò_Àtòkọ = new ArrayList<ohun_èlò_iye>();

    public void 발견(ohun_èlò_iye ohun_èlò_iye) {
        Ohun_èlò_Àtòkọ.add(ohun_èlò_iye);
    }

    public List<ohun_èlò_iye> Ohun_èlò_Àtòkọ() {
        return Collections.unmodifiableList(Ohun_èlò_Àtòkọ);
    }

    public ohun_èlò_iye wá_ìgbéwọlé(int 판매자식별자, int ohun_èlò_Àfidámọ̀) {
        for (ohun_èlò_iye 후보 : Ohun_èlò_Àtòkọ) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ohun_èlò_Àfidámọ̀ == ohun_èlò_Àfidámọ̀) {
                return 후보;
            }
        }
        return null;
    }
}

