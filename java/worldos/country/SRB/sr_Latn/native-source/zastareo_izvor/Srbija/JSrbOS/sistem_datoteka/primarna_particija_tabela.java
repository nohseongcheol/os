// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.sistem_datoteka;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 podrazumevana_vrednost 분할 영역을 읽는다. */
public final class primarna_particija_tabela {
    public static final class particija_VALUE {
        private final int 종류;
        private final long START_odeljak;
        private final long odeljak_COUNT;

        particija_VALUE(int 종류, long START_odeljak, long odeljak_COUNT) {
            this.종류 = 종류;
            this.START_odeljak = START_odeljak;
            this.odeljak_COUNT = odeljak_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_odeljak() { return START_odeljak; }
        public long odeljak_COUNT() { return odeljak_COUNT; }
    }

    public List<particija_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<particija_VALUE> KR = new ArrayList<particija_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int pozicija = 446 + INDEX * 16;
            int 종류 = 첫구역[pozicija + 4] & 0xff;
            long koristiti = 작은순서정수(첫구역, pozicija + 8);
            long promeniti_veličinu = 작은순서정수(첫구역, pozicija + 12);
            if (종류 != 0 && promeniti_veličinu != 0) {
                KR.add(new particija_VALUE(종류, koristiti, promeniti_veličinu));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long 작은순서정수(byte[] podaci, int pozicija) {
        return (podaci[pozicija] & 0xffL)
                | ((podaci[pozicija + 1] & 0xffL) << 8)
                | ((podaci[pozicija + 2] & 0xffL) << 16)
                | ((podaci[pozicija + 3] & 0xffL) << 24);
    }
}

