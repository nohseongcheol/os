// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.fajl_sistem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 zadana_vrijednost 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class particija_VALUE {
        private final int 종류;
        private final long START_sekcija;
        private final long sekcija_COUNT;

        particija_VALUE(int 종류, long START_sekcija, long sekcija_COUNT) {
            this.종류 = 종류;
            this.START_sekcija = START_sekcija;
            this.sekcija_COUNT = sekcija_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_sekcija() { return START_sekcija; }
        public long sekcija_COUNT() { return sekcija_COUNT; }
    }

    public List<particija_VALUE> Čitaj(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<particija_VALUE> mjera = new ArrayList<particija_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Pozicija = 446 + INDEX * 16;
            int 종류 = 첫구역[Pozicija + 4] & 0xff;
            long Pokreni = 작은순서정수(첫구역, Pozicija + 8);
            long Veličina = 작은순서정수(첫구역, Pozicija + 12);
            if (종류 != 0 && Veličina != 0) {
                mjera.add(new particija_VALUE(종류, Pokreni, Veličina));
            }
        }
        return Collections.unmodifiableList(mjera);
    }

    private long 작은순서정수(byte[] podaci, int Pozicija) {
        return (podaci[Pozicija] & 0xffL)
                | ((podaci[Pozicija + 1] & 0xffL) << 8)
                | ((podaci[Pozicija + 2] & 0xffL) << 16)
                | ((podaci[Pozicija + 3] & 0xffL) << 24);
    }
}

