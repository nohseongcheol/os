// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.telefón_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI telefón_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class telefón_VALUE {
        private final int dodávateľ_identifikátor;
        private final int telefón_identifikátor;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public telefón_VALUE(int dodávateľ_identifikátor, int telefón_identifikátor, int 입출력바탕, int 개입중단번호) {
            this.dodávateľ_identifikátor = dodávateľ_identifikátor;
            this.telefón_identifikátor = telefón_identifikátor;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int dodávateľ_identifikátor() { return dodávateľ_identifikátor; }
        public int telefón_identifikátor() { return telefón_identifikátor; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<telefón_VALUE> Zariadenia_Zoznam = new ArrayList<telefón_VALUE>();

    public void 발견(telefón_VALUE telefón_VALUE) {
        Zariadenia_Zoznam.add(telefón_VALUE);
    }

    public List<telefón_VALUE> Zariadenia_Zoznam() {
        return Collections.unmodifiableList(Zariadenia_Zoznam);
    }

    public telefón_VALUE FIND_položka(int dodávateľ_identifikátor, int telefón_identifikátor) {
        for (telefón_VALUE 후보 : Zariadenia_Zoznam) {
            if (후보.dodávateľ_identifikátor == dodávateľ_identifikátor && 후보.telefón_identifikátor == telefón_identifikátor) {
                return 후보;
            }
        }
        return null;
    }
}

