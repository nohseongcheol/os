// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standardverdi 분할 영역을 읽는다. */
public final class primærpartisjon_tabell {
    public static final class partisjon_VERDI {
        private final int 종류;
        private final long START_inndeling;
        private final long inndeling_ANTALL;

        partisjon_VERDI(int 종류, long START_inndeling, long inndeling_ANTALL) {
            this.종류 = 종류;
            this.START_inndeling = START_inndeling;
            this.inndeling_ANTALL = inndeling_ANTALL;
        }

        public int 종류() { return 종류; }
        public long START_inndeling() { return START_inndeling; }
        public long inndeling_ANTALL() { return inndeling_ANTALL; }
    }

    public List<partisjon_VERDI> Les(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partisjon_VERDI> KR = new ArrayList<partisjon_VERDI>();
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            int Posisjon = 446 + INDEKS * 16;
            int 종류 = 첫구역[Posisjon + 4] & 0xff;
            long Kjør_2 = 작은순서정수(첫구역, Posisjon + 8);
            long Størrelse = 작은순서정수(첫구역, Posisjon + 12);
            if (종류 != 0 && Størrelse != 0) {
                KR.add(new partisjon_VERDI(종류, Kjør_2, Størrelse));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long 작은순서정수(byte[] data, int Posisjon) {
        return (data[Posisjon] & 0xffL)
                | ((data[Posisjon + 1] & 0xffL) << 8)
                | ((data[Posisjon + 2] & 0xffL) << 16)
                | ((data[Posisjon + 3] & 0xffL) << 24);
    }
}

