// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.systém_súborov;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 predvolená_hodnota 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class oblasť_VALUE_105b7afb {
        private final int 종류;
        private final long START_sekcia;
        private final long sekcia_COUNT;

        oblasť_VALUE_105b7afb(int 종류, long START_sekcia, long sekcia_COUNT) {
            this.종류 = 종류;
            this.START_sekcia = START_sekcia;
            this.sekcia_COUNT = sekcia_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_sekcia() { return START_sekcia; }
        public long sekcia_COUNT() { return sekcia_COUNT; }
    }

    public List<oblasť_VALUE_105b7afb> Čítanie(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<oblasť_VALUE_105b7afb> KR = new ArrayList<oblasť_VALUE_105b7afb>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Pozícia = 446 + INDEX * 16;
            int 종류 = 첫구역[Pozícia + 4] & 0xff;
            long Spustiť_2 = Little_Endian_celé_číslo(첫구역, Pozícia + 8);
            long Veľkosť = Little_Endian_celé_číslo(첫구역, Pozícia + 12);
            if (종류 != 0 && Veľkosť != 0) {
                KR.add(new oblasť_VALUE_105b7afb(종류, Spustiť_2, Veľkosť));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long Little_Endian_celé_číslo(byte[] údaje, int Pozícia) {
        return (údaje[Pozícia] & 0xffL)
                | ((údaje[Pozícia + 1] & 0xffL) << 8)
                | ((údaje[Pozícia + 2] & 0xffL) << 16)
                | ((údaje[Pozícia + 3] & 0xffL) << 24);
    }
}

