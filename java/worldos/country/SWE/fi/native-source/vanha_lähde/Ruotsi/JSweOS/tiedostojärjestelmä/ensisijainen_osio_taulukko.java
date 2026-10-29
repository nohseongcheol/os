// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ruotsi.JSweOS.tiedostojärjestelmä;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 oletusarvo 분할 영역을 읽는다. */
public final class ensisijainen_osio_taulukko {
    public static final class osio_ARVO {
        private final int 종류;
        private final long alku_osa;
        private final long osa_LASKE;

        osio_ARVO(int 종류, long alku_osa, long osa_LASKE) {
            this.종류 = 종류;
            this.alku_osa = alku_osa;
            this.osa_LASKE = osa_LASKE;
        }

        public int 종류() { return 종류; }
        public long alku_osa() { return alku_osa; }
        public long osa_LASKE() { return osa_LASKE; }
    }

    public List<osio_ARVO> Luku(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<osio_ARVO> TULOS = new ArrayList<osio_ARVO>();
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) {
            int paikka = 446 + INDEKSI * 16;
            int 종류 = 첫구역[paikka + 4] & 0xff;
            long Suorita_2 = little_endian_kokonaisluku(첫구역, paikka + 8);
            long Koko = little_endian_kokonaisluku(첫구역, paikka + 12);
            if (종류 != 0 && Koko != 0) {
                TULOS.add(new osio_ARVO(종류, Suorita_2, Koko));
            }
        }
        return Collections.unmodifiableList(TULOS);
    }

    private long little_endian_kokonaisluku(byte[] data, int paikka) {
        return (data[paikka] & 0xffL)
                | ((data[paikka + 1] & 0xffL) << 8)
                | ((data[paikka + 2] & 0xffL) << 16)
                | ((data[paikka + 3] & 0xffL) << 24);
    }
}

