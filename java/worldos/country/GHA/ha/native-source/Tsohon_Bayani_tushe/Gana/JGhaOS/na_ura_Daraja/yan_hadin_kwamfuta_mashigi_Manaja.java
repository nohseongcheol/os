// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.na_ura_Daraja;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI na_ura_Daraja 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class yan_hadin_kwamfuta_mashigi_Manaja {
    public static final class na_ura_Daraja {
        private final int mai_ƙirƙira_mai_ganewa;
        private final int na_ura_mai_ganewa;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public na_ura_Daraja(int mai_ƙirƙira_mai_ganewa, int na_ura_mai_ganewa, int 입출력바탕, int 개입중단번호) {
            this.mai_ƙirƙira_mai_ganewa = mai_ƙirƙira_mai_ganewa;
            this.na_ura_mai_ganewa = na_ura_mai_ganewa;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int mai_ƙirƙira_mai_ganewa() { return mai_ƙirƙira_mai_ganewa; }
        public int na_ura_mai_ganewa() { return na_ura_mai_ganewa; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<na_ura_Daraja> Na_urori_Jeri = new ArrayList<na_ura_Daraja>();

    public void 발견(na_ura_Daraja na_ura_Daraja) {
        Na_urori_Jeri.add(na_ura_Daraja);
    }

    public List<na_ura_Daraja> Na_urori_Jeri() {
        return Collections.unmodifiableList(Na_urori_Jeri);
    }

    public na_ura_Daraja nema_Mashigar_bayanai(int mai_ƙirƙira_mai_ganewa, int na_ura_mai_ganewa) {
        for (na_ura_Daraja 후보 : Na_urori_Jeri) {
            if (후보.mai_ƙirƙira_mai_ganewa == mai_ƙirƙira_mai_ganewa && 후보.na_ura_mai_ganewa == na_ura_mai_ganewa) {
                return 후보;
            }
        }
        return null;
    }
}

