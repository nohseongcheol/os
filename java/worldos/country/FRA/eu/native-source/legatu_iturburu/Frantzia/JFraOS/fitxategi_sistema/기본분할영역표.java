// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frantzia.JFraOS.fitxategi_sistema;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 balio_lehenetsi 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partizio_balio {
        private final int 종류;
        private final long HASI_sekzio;
        private final long sekzio_ZENBATU;

        partizio_balio(int 종류, long HASI_sekzio, long sekzio_ZENBATU) {
            this.종류 = 종류;
            this.HASI_sekzio = HASI_sekzio;
            this.sekzio_ZENBATU = sekzio_ZENBATU;
        }

        public int 종류() { return 종류; }
        public long HASI_sekzio() { return HASI_sekzio; }
        public long sekzio_ZENBATU() { return sekzio_ZENBATU; }
    }

    public List<partizio_balio> Irakurri(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partizio_balio> EMAITZA = new ArrayList<partizio_balio>();
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) {
            int Posizioa = 446 + INDIZE * 16;
            int 종류 = 첫구역[Posizioa + 4] & 0xff;
            long Exekutatu_2 = 작은순서정수(첫구역, Posizioa + 8);
            long Tamaina = 작은순서정수(첫구역, Posizioa + 12);
            if (종류 != 0 && Tamaina != 0) {
                EMAITZA.add(new partizio_balio(종류, Exekutatu_2, Tamaina));
            }
        }
        return Collections.unmodifiableList(EMAITZA);
    }

    private long 작은순서정수(byte[] datuak, int Posizioa) {
        return (datuak[Posizioa] & 0xffL)
                | ((datuak[Posizioa + 1] & 0xffL) << 8)
                | ((datuak[Posizioa + 2] & 0xffL) << 16)
                | ((datuak[Posizioa + 3] & 0xffL) << 24);
    }
}

