// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 standardvärde 분할 영역을 읽는다. */
public final class primär_partition_tabell {
    public static final class partition_värde {
        private final int variant_värde;
        private final long START_avsnitt;
        private final long avsnitt_ANTAL;

        partition_värde(int variant_värde, long START_avsnitt, long avsnitt_ANTAL) {
            this.variant_värde = variant_värde;
            this.START_avsnitt = START_avsnitt;
            this.avsnitt_ANTAL = avsnitt_ANTAL;
        }

        public int variant_värde() { return variant_värde; }
        public long START_avsnitt() { return START_avsnitt; }
        public long avsnitt_ANTAL() { return avsnitt_ANTAL; }
    }

    public List<partition_värde> Läs(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partition_värde> RESULTAT = new ArrayList<partition_värde>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int position = 446 + INDEX * 16;
            int variant_värde = 첫구역[position + 4] & 0xff;
            long Kör = little_endian_heltal(첫구역, position + 8);
            long Storlek = little_endian_heltal(첫구역, position + 12);
            if (variant_värde != 0 && Storlek != 0) {
                RESULTAT.add(new partition_värde(variant_värde, Kör, Storlek));
            }
        }
        return Collections.unmodifiableList(RESULTAT);
    }

    private long little_endian_heltal(byte[] data, int position) {
        return (data[position] & 0xffL)
                | ((data[position + 1] & 0xffL) << 8)
                | ((data[position + 2] & 0xffL) << 16)
                | ((data[position + 3] & 0xffL) << 24);
    }
}

