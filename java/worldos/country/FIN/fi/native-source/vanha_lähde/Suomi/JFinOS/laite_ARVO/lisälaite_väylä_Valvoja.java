// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.laite_ARVO;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI laite_ARVO 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class lisälaite_väylä_Valvoja {
    public static final class laite_ARVO {
        private final int myyjä_tunniste;
        private final int laite_tunniste;
        private final int 입출력바탕;
        private final int IRQ_numero;

        public laite_ARVO(int myyjä_tunniste, int laite_tunniste, int 입출력바탕, int IRQ_numero) {
            this.myyjä_tunniste = myyjä_tunniste;
            this.laite_tunniste = laite_tunniste;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_numero = IRQ_numero;
        }

        public int myyjä_tunniste() { return myyjä_tunniste; }
        public int laite_tunniste() { return laite_tunniste; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_numero() { return IRQ_numero; }
    }

    private final List<laite_ARVO> Laitteet_luettelo = new ArrayList<laite_ARVO>();

    public void 발견(laite_ARVO laite_ARVO) {
        Laitteet_luettelo.add(laite_ARVO);
    }

    public List<laite_ARVO> Laitteet_luettelo() {
        return Collections.unmodifiableList(Laitteet_luettelo);
    }

    public laite_ARVO ETSI_merkintä(int myyjä_tunniste, int laite_tunniste) {
        for (laite_ARVO 후보 : Laitteet_luettelo) {
            if (후보.myyjä_tunniste == myyjä_tunniste && 후보.laite_tunniste == laite_tunniste) {
                return 후보;
            }
        }
        return null;
    }
}

