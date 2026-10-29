// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.failu_sistēma;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 noklusējuma_vērtība 분할 영역을 읽는다. */
public final class primārais_nodalījums_tabula {
    public static final class nodalījums_VALUE {
        private final int 종류;
        private final long Sākt_sadaļa;
        private final long sadaļa_COUNT;

        nodalījums_VALUE(int 종류, long Sākt_sadaļa, long sadaļa_COUNT) {
            this.종류 = 종류;
            this.Sākt_sadaļa = Sākt_sadaļa;
            this.sadaļa_COUNT = sadaļa_COUNT;
        }

        public int 종류() { return 종류; }
        public long Sākt_sadaļa() { return Sākt_sadaļa; }
        public long sadaļa_COUNT() { return sadaļa_COUNT; }
    }

    public List<nodalījums_VALUE> Lasīt(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<nodalījums_VALUE> mērs = new ArrayList<nodalījums_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Novietojums = 446 + INDEX * 16;
            int 종류 = 첫구역[Novietojums + 4] & 0xff;
            long Palaist = tiešsecības_vesels_skaitlis(첫구역, Novietojums + 8);
            long Izmērs = tiešsecības_vesels_skaitlis(첫구역, Novietojums + 12);
            if (종류 != 0 && Izmērs != 0) {
                mērs.add(new nodalījums_VALUE(종류, Palaist, Izmērs));
            }
        }
        return Collections.unmodifiableList(mērs);
    }

    private long tiešsecības_vesels_skaitlis(byte[] dati, int Novietojums) {
        return (dati[Novietojums] & 0xffL)
                | ((dati[Novietojums + 1] & 0xffL) << 8)
                | ((dati[Novietojums + 2] & 0xffL) << 16)
                | ((dati[Novietojums + 3] & 0xffL) << 24);
    }
}

