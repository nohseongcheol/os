// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Mobil_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI Mobil_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class Accessoire_Bus_Manager {
    public static final class Mobil_VALUE {
        private final int 판매자식별자;
        private final int Mobil_Identifikateur;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public Mobil_VALUE(int 판매자식별자, int Mobil_Identifikateur, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.Mobil_Identifikateur = Mobil_Identifikateur;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int Mobil_Identifikateur() { return Mobil_Identifikateur; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<Mobil_VALUE> Apparater_Lëscht = new ArrayList<Mobil_VALUE>();

    public void 발견(Mobil_VALUE Mobil_VALUE) {
        Apparater_Lëscht.add(Mobil_VALUE);
    }

    public List<Mobil_VALUE> Apparater_Lëscht() {
        return Collections.unmodifiableList(Apparater_Lëscht);
    }

    public Mobil_VALUE FIND_Agab(int 판매자식별자, int Mobil_Identifikateur) {
        for (Mobil_VALUE 후보 : Apparater_Lëscht) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.Mobil_Identifikateur == Mobil_Identifikateur) {
                return 후보;
            }
        }
        return null;
    }
}

