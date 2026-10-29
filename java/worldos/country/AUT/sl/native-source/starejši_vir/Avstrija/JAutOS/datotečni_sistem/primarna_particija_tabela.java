// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.datotečni_sistem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 privzeta_vrednost 분할 영역을 읽는다. */
public final class primarna_particija_tabela {
    public static final class particija_VALUE {
        private final int 종류;
        private final long Start_odsek;
        private final long odsek_COUNT;

        particija_VALUE(int 종류, long Start_odsek, long odsek_COUNT) {
            this.종류 = 종류;
            this.Start_odsek = Start_odsek;
            this.odsek_COUNT = odsek_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_odsek() { return Start_odsek; }
        public long odsek_COUNT() { return odsek_COUNT; }
    }

    public List<particija_VALUE> Branje(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<particija_VALUE> REZULTAT = new ArrayList<particija_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Položaj = 446 + INDEX * 16;
            int 종류 = 첫구역[Položaj + 4] & 0xff;
            long Zaženi = little_endian_celo_število(첫구역, Položaj + 8);
            long Velikost = little_endian_celo_število(첫구역, Položaj + 12);
            if (종류 != 0 && Velikost != 0) {
                REZULTAT.add(new particija_VALUE(종류, Zaženi, Velikost));
            }
        }
        return Collections.unmodifiableList(REZULTAT);
    }

    private long little_endian_celo_število(byte[] podatki, int Položaj) {
        return (podatki[Položaj] & 0xffL)
                | ((podatki[Položaj + 1] & 0xffL) << 8)
                | ((podatki[Položaj + 2] & 0xffL) << 16)
                | ((podatki[Položaj + 3] & 0xffL) << 24);
    }
}

