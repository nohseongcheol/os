// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.failisüsteem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 vaikeväärtus 분할 영역을 읽는다. */
public final class primaarsektsioon_tabel {
    public static final class sektsioon_VALUE {
        private final int 종류;
        private final long START_jaotis;
        private final long jaotis_COUNT;

        sektsioon_VALUE(int 종류, long START_jaotis, long jaotis_COUNT) {
            this.종류 = 종류;
            this.START_jaotis = START_jaotis;
            this.jaotis_COUNT = jaotis_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_jaotis() { return START_jaotis; }
        public long jaotis_COUNT() { return jaotis_COUNT; }
    }

    public List<sektsioon_VALUE> Lugemine(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<sektsioon_VALUE> TULEMUS = new ArrayList<sektsioon_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Asukoht = 446 + INDEX * 16;
            int 종류 = 첫구역[Asukoht + 4] & 0xff;
            long Käivita_2 = pöördjärjestusega_täisarv(첫구역, Asukoht + 8);
            long Suurus = pöördjärjestusega_täisarv(첫구역, Asukoht + 12);
            if (종류 != 0 && Suurus != 0) {
                TULEMUS.add(new sektsioon_VALUE(종류, Käivita_2, Suurus));
            }
        }
        return Collections.unmodifiableList(TULEMUS);
    }

    private long pöördjärjestusega_täisarv(byte[] andmed, int Asukoht) {
        return (andmed[Asukoht] & 0xffL)
                | ((andmed[Asukoht + 1] & 0xffL) << 8)
                | ((andmed[Asukoht + 2] & 0xffL) << 16)
                | ((andmed[Asukoht + 3] & 0xffL) << 24);
    }
}

