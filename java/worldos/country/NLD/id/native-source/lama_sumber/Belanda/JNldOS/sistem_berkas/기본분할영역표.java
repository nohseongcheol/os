// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.sistem_berkas;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 nilai_default 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partisi_VALUE {
        private final int 종류;
        private final long Mulai_seksi;
        private final long seksi_COUNT;

        partisi_VALUE(int 종류, long Mulai_seksi, long seksi_COUNT) {
            this.종류 = 종류;
            this.Mulai_seksi = Mulai_seksi;
            this.seksi_COUNT = seksi_COUNT;
        }

        public int 종류() { return 종류; }
        public long Mulai_seksi() { return Mulai_seksi; }
        public long seksi_COUNT() { return seksi_COUNT; }
    }

    public List<partisi_VALUE> Baca(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partisi_VALUE> hasil = new ArrayList<partisi_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int posisi = 446 + INDEX * 16;
            int 종류 = 첫구역[posisi + 4] & 0xff;
            long jalankan = little_endian_bilangan_bulat(첫구역, posisi + 8);
            long Ukuran = little_endian_bilangan_bulat(첫구역, posisi + 12);
            if (종류 != 0 && Ukuran != 0) {
                hasil.add(new partisi_VALUE(종류, jalankan, Ukuran));
            }
        }
        return Collections.unmodifiableList(hasil);
    }

    private long little_endian_bilangan_bulat(byte[] data, int posisi) {
        return (data[posisi] & 0xffL)
                | ((data[posisi + 1] & 0xffL) << 8)
                | ((data[posisi + 2] & 0xffL) << 16)
                | ((data[posisi + 3] & 0xffL) << 24);
    }
}

