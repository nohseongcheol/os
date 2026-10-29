// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiye.JTurOS.dosya_sistemi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 varsayılan_değer 분할 영역을 읽는다. */
public final class birincil_bölüm_tablo {
    public static final class bölüm_değer {
        private final int Tip_değer;
        private final long Start_bölüm;
        private final long bölüm_BAĞ_DEĞ_SAY;

        bölüm_değer(int Tip_değer, long Start_bölüm, long bölüm_BAĞ_DEĞ_SAY) {
            this.Tip_değer = Tip_değer;
            this.Start_bölüm = Start_bölüm;
            this.bölüm_BAĞ_DEĞ_SAY = bölüm_BAĞ_DEĞ_SAY;
        }

        public int Tip_değer() { return Tip_değer; }
        public long Start_bölüm() { return Start_bölüm; }
        public long bölüm_BAĞ_DEĞ_SAY() { return bölüm_BAĞ_DEĞ_SAY; }
    }

    public List<bölüm_değer> Okuma(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<bölüm_değer> sonuç = new ArrayList<bölüm_değer>();
        for (int Dizin = 0; Dizin < 4; Dizin++) {
            int konum = 446 + Dizin * 16;
            int Tip_değer = 첫구역[konum + 4] & 0xff;
            long çalıştır = little_endian_bilgi(첫구역, konum + 8);
            long Boyut = little_endian_bilgi(첫구역, konum + 12);
            if (Tip_değer != 0 && Boyut != 0) {
                sonuç.add(new bölüm_değer(Tip_değer, çalıştır, Boyut));
            }
        }
        return Collections.unmodifiableList(sonuç);
    }

    private long little_endian_bilgi(byte[] veri, int konum) {
        return (veri[konum] & 0xffL)
                | ((veri[konum + 1] & 0xffL) << 8)
                | ((veri[konum + 2] & 0xffL) << 16)
                | ((veri[konum + 3] & 0xffL) << 24);
    }
}

