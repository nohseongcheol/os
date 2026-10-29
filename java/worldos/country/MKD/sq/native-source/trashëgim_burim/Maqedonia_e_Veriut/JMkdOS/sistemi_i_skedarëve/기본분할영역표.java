// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Maqedonia_e_Veriut.JMkdOS.sistemi_i_skedarëve;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 vlerë_e_parazgjedhur 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ndarje_VALUE {
        private final int 종류;
        private final long nis_seksion;
        private final long seksion_COUNT;

        ndarje_VALUE(int 종류, long nis_seksion, long seksion_COUNT) {
            this.종류 = 종류;
            this.nis_seksion = nis_seksion;
            this.seksion_COUNT = seksion_COUNT;
        }

        public int 종류() { return 종류; }
        public long nis_seksion() { return nis_seksion; }
        public long seksion_COUNT() { return seksion_COUNT; }
    }

    public List<ndarje_VALUE> Leximi(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ndarje_VALUE> llogaritje = new ArrayList<ndarje_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Pozicioni = 446 + INDEX * 16;
            int 종류 = 첫구역[Pozicioni + 4] & 0xff;
            long Ekzekuto = 작은순서정수(첫구역, Pozicioni + 8);
            long Madhësi = 작은순서정수(첫구역, Pozicioni + 12);
            if (종류 != 0 && Madhësi != 0) {
                llogaritje.add(new ndarje_VALUE(종류, Ekzekuto, Madhësi));
            }
        }
        return Collections.unmodifiableList(llogaritje);
    }

    private long 작은순서정수(byte[] të_dhëna, int Pozicioni) {
        return (të_dhëna[Pozicioni] & 0xffL)
                | ((të_dhëna[Pozicioni + 1] & 0xffL) << 8)
                | ((të_dhëna[Pozicioni + 2] & 0xffL) << 16)
                | ((të_dhëna[Pozicioni + 3] & 0xffL) << 24);
    }
}

