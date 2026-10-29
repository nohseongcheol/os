// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Israel.JIsrOS.sistem_de_fișiere;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valoare_implicită 분할 영역을 읽는다. */
public final class partiție_principală_tabel {
    public static final class partiție_VALUE {
        private final int 종류;
        private final long buta_secțiune;
        private final long secțiune_COUNT;

        partiție_VALUE(int 종류, long buta_secțiune, long secțiune_COUNT) {
            this.종류 = 종류;
            this.buta_secțiune = buta_secțiune;
            this.secțiune_COUNT = secțiune_COUNT;
        }

        public int 종류() { return 종류; }
        public long buta_secțiune() { return buta_secțiune; }
        public long secțiune_COUNT() { return secțiune_COUNT; }
    }

    public List<partiție_VALUE> Citire(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partiție_VALUE> KR = new ArrayList<partiție_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Poziție = 446 + INDEX * 16;
            int 종류 = 첫구역[Poziție + 4] & 0xff;
            long Pornește = little_endian_întreg(첫구역, Poziție + 8);
            long Mărime = little_endian_întreg(첫구역, Poziție + 12);
            if (종류 != 0 && Mărime != 0) {
                KR.add(new partiție_VALUE(종류, Pornește, Mărime));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long little_endian_întreg(byte[] date, int Poziție) {
        return (date[Poziție] & 0xffL)
                | ((date[Poziție + 1] & 0xffL) << 8)
                | ((date[Poziție + 2] & 0xffL) << 16)
                | ((date[Poziție + 3] & 0xffL) << 24);
    }
}

