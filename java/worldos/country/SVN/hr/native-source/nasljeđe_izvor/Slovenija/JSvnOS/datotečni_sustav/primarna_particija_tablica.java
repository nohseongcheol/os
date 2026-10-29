// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.datotečni_sustav;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 zadana_vrijednost 분할 영역을 읽는다. */
public final class primarna_particija_tablica {
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
        List<particija_VALUE> REZULTAT = new ArrayList<particija_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Položaj = 446 + INDEX * 16;
            int 종류 = 첫구역[Položaj + 4] & 0xff;
            long Pokreni = Little_Endian_cijeli_broj(첫구역, Položaj + 8);
            long Veličina = Little_Endian_cijeli_broj(첫구역, Položaj + 12);
            if (종류 != 0 && Veličina != 0) {
                REZULTAT.add(new particija_VALUE(종류, Pokreni, Veličina));
            }
        }
        return Collections.unmodifiableList(REZULTAT);
    }

    private long Little_Endian_cijeli_broj(byte[] podaci, int Položaj) {
        return (podaci[Položaj] & 0xffL)
                | ((podaci[Položaj + 1] & 0xffL) << 8)
                | ((podaci[Položaj + 2] & 0xffL) << 16)
                | ((podaci[Položaj + 3] & 0xffL) << 24);
    }
}

