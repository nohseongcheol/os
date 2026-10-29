// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standardværdi 분할 영역을 읽는다. */
public final class primær_partition_tabel {
    public static final class partition_VÆRDI {
        private final int 종류;
        private final long START_sektion;
        private final long sektion_TÆL;

        partition_VÆRDI(int 종류, long START_sektion, long sektion_TÆL) {
            this.종류 = 종류;
            this.START_sektion = START_sektion;
            this.sektion_TÆL = sektion_TÆL;
        }

        public int 종류() { return 종류; }
        public long START_sektion() { return START_sektion; }
        public long sektion_TÆL() { return sektion_TÆL; }
    }

    public List<partition_VÆRDI> Læse(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partition_VÆRDI> KR = new ArrayList<partition_VÆRDI>();
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            int Placering = 446 + INDEKS * 16;
            int 종류 = 첫구역[Placering + 4] & 0xff;
            long Kør_2 = little_endian_heltal(첫구역, Placering + 8);
            long Størrelse = little_endian_heltal(첫구역, Placering + 12);
            if (종류 != 0 && Størrelse != 0) {
                KR.add(new partition_VÆRDI(종류, Kør_2, Størrelse));
            }
        }
        return Collections.unmodifiableList(KR);
    }

    private long little_endian_heltal(byte[] data, int Placering) {
        return (data[Placering] & 0xffL)
                | ((data[Placering + 1] & 0xffL) << 8)
                | ((data[Placering + 2] & 0xffL) << 16)
                | ((data[Placering + 3] & 0xffL) << 24);
    }
}

