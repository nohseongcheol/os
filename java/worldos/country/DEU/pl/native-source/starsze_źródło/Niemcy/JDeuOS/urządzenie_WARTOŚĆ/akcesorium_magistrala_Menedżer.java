// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Niemcy.JDeuOS.urządzenie_WARTOŚĆ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI urządzenie_WARTOŚĆ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class akcesorium_magistrala_Menedżer {
    public static final class urządzenie_WARTOŚĆ {
        private final int dostawca_identyfikator;
        private final int urządzenie_identyfikator;
        private final int 입출력바탕;
        private final int przerwanie_identyfikator;

        public urządzenie_WARTOŚĆ(int dostawca_identyfikator, int urządzenie_identyfikator, int 입출력바탕, int przerwanie_identyfikator) {
            this.dostawca_identyfikator = dostawca_identyfikator;
            this.urządzenie_identyfikator = urządzenie_identyfikator;
            this.입출력바탕 = 입출력바탕;
            this.przerwanie_identyfikator = przerwanie_identyfikator;
        }

        public int dostawca_identyfikator() { return dostawca_identyfikator; }
        public int urządzenie_identyfikator() { return urządzenie_identyfikator; }
        public int 입출력바탕() { return 입출력바탕; }
        public int przerwanie_identyfikator() { return przerwanie_identyfikator; }
    }

    private final List<urządzenie_WARTOŚĆ> Urządzenia_Lista = new ArrayList<urządzenie_WARTOŚĆ>();

    public void 발견(urządzenie_WARTOŚĆ urządzenie_WARTOŚĆ) {
        Urządzenia_Lista.add(urządzenie_WARTOŚĆ);
    }

    public List<urządzenie_WARTOŚĆ> Urządzenia_Lista() {
        return Collections.unmodifiableList(Urządzenia_Lista);
    }

    public urządzenie_WARTOŚĆ ZNAJDŹ_wpis(int dostawca_identyfikator, int urządzenie_identyfikator) {
        for (urządzenie_WARTOŚĆ kandydat : Urządzenia_Lista) {
            if (kandydat.dostawca_identyfikator == dostawca_identyfikator && kandydat.urządzenie_identyfikator == urządzenie_identyfikator) {
                return kandydat;
            }
        }
        return null;
    }
}

