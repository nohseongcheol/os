// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.naprava_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI naprava_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class zunanji_vodilo_Upravitelj {
    public static final class naprava_VALUE {
        private final int dobavitelj_identifikator;
        private final int naprava_identifikator;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public naprava_VALUE(int dobavitelj_identifikator, int naprava_identifikator, int 입출력바탕, int 개입중단번호) {
            this.dobavitelj_identifikator = dobavitelj_identifikator;
            this.naprava_identifikator = naprava_identifikator;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int dobavitelj_identifikator() { return dobavitelj_identifikator; }
        public int naprava_identifikator() { return naprava_identifikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<naprava_VALUE> Naprave_Seznam = new ArrayList<naprava_VALUE>();

    public void 발견(naprava_VALUE naprava_VALUE) {
        Naprave_Seznam.add(naprava_VALUE);
    }

    public List<naprava_VALUE> Naprave_Seznam() {
        return Collections.unmodifiableList(Naprave_Seznam);
    }

    public naprava_VALUE FIND_vnos(int dobavitelj_identifikator, int naprava_identifikator) {
        for (naprava_VALUE 후보 : Naprave_Seznam) {
            if (후보.dobavitelj_identifikator == dobavitelj_identifikator && 후보.naprava_identifikator == naprava_identifikator) {
                return 후보;
            }
        }
        return null;
    }
}

