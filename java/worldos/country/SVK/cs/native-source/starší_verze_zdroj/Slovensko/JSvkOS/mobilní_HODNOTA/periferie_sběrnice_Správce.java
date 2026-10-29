// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.mobilní_HODNOTA;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobilní_HODNOTA 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class periferie_sběrnice_Správce {
    public static final class mobilní_HODNOTA {
        private final int dodavatel_identifikátor;
        private final int mobilní_identifikátor;
        private final int 입출력바탕;
        private final int přerušení_číslo;

        public mobilní_HODNOTA(int dodavatel_identifikátor, int mobilní_identifikátor, int 입출력바탕, int přerušení_číslo) {
            this.dodavatel_identifikátor = dodavatel_identifikátor;
            this.mobilní_identifikátor = mobilní_identifikátor;
            this.입출력바탕 = 입출력바탕;
            this.přerušení_číslo = přerušení_číslo;
        }

        public int dodavatel_identifikátor() { return dodavatel_identifikátor; }
        public int mobilní_identifikátor() { return mobilní_identifikátor; }
        public int 입출력바탕() { return 입출력바탕; }
        public int přerušení_číslo() { return přerušení_číslo; }
    }

    private final List<mobilní_HODNOTA> Zařízení_Seznam = new ArrayList<mobilní_HODNOTA>();

    public void 발견(mobilní_HODNOTA mobilní_HODNOTA) {
        Zařízení_Seznam.add(mobilní_HODNOTA);
    }

    public List<mobilní_HODNOTA> Zařízení_Seznam() {
        return Collections.unmodifiableList(Zařízení_Seznam);
    }

    public mobilní_HODNOTA NAJÍT_položka(int dodavatel_identifikátor, int mobilní_identifikátor) {
        for (mobilní_HODNOTA 후보 : Zařízení_Seznam) {
            if (후보.dodavatel_identifikátor == dodavatel_identifikátor && 후보.mobilní_identifikátor == mobilní_identifikátor) {
                return 후보;
            }
        }
        return null;
    }
}

