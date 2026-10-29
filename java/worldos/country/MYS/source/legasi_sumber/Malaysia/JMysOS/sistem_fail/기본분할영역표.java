// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malaysia.JMysOS.sistem_fail;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 nilai_lalai 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class petak_VALUE {
        private final int 종류;
        private final long Mula_seksyen;
        private final long seksyen_COUNT;

        petak_VALUE(int 종류, long Mula_seksyen, long seksyen_COUNT) {
            this.종류 = 종류;
            this.Mula_seksyen = Mula_seksyen;
            this.seksyen_COUNT = seksyen_COUNT;
        }

        public int 종류() { return 종류; }
        public long Mula_seksyen() { return Mula_seksyen; }
        public long seksyen_COUNT() { return seksyen_COUNT; }
    }

    public List<petak_VALUE> Baca(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<petak_VALUE> ukuran = new ArrayList<petak_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Kedudukan = 446 + INDEX * 16;
            int 종류 = 첫구역[Kedudukan + 4] & 0xff;
            long Jalan = little_endian_integer(첫구역, Kedudukan + 8);
            long Saiz = little_endian_integer(첫구역, Kedudukan + 12);
            if (종류 != 0 && Saiz != 0) {
                ukuran.add(new petak_VALUE(종류, Jalan, Saiz));
            }
        }
        return Collections.unmodifiableList(ukuran);
    }

    private long little_endian_integer(byte[] data, int Kedudukan) {
        return (data[Kedudukan] & 0xffL)
                | ((data[Kedudukan + 1] & 0xffL) << 8)
                | ((data[Kedudukan + 2] & 0xffL) << 16)
                | ((data[Kedudukan + 3] & 0xffL) << 24);
    }
}

