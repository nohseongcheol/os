// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Caribisch_Nederland.JBesOS.bestandssysteem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standaardwaarde 분할 영역을 읽는다. */
public final class primaire_partitie_tabel {
    public static final class partitie_WAARDE {
        private final int soort_WAARDE;
        private final long START_sectie;
        private final long sectie_AANTAL;

        partitie_WAARDE(int soort_WAARDE, long START_sectie, long sectie_AANTAL) {
            this.soort_WAARDE = soort_WAARDE;
            this.START_sectie = START_sectie;
            this.sectie_AANTAL = sectie_AANTAL;
        }

        public int soort_WAARDE() { return soort_WAARDE; }
        public long START_sectie() { return START_sectie; }
        public long sectie_AANTAL() { return sectie_AANTAL; }
    }

    public List<partitie_WAARDE> Lezen(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partitie_WAARDE> resultaat = new ArrayList<partitie_WAARDE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int positie = 446 + INDEX * 16;
            int soort_WAARDE = 첫구역[positie + 4] & 0xff;
            long starten = little_endian_geheel_getal(첫구역, positie + 8);
            long Grootte = little_endian_geheel_getal(첫구역, positie + 12);
            if (soort_WAARDE != 0 && Grootte != 0) {
                resultaat.add(new partitie_WAARDE(soort_WAARDE, starten, Grootte));
            }
        }
        return Collections.unmodifiableList(resultaat);
    }

    private long little_endian_geheel_getal(byte[] gegevens, int positie) {
        return (gegevens[positie] & 0xffL)
                | ((gegevens[positie + 1] & 0xffL) << 8)
                | ((gegevens[positie + 2] & 0xffL) << 16)
                | ((gegevens[positie + 3] & 0xffL) << 24);
    }
}

