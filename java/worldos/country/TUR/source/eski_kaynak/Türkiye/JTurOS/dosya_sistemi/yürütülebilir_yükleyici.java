// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiye.JTurOS.dosya_sistemi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian yürütmek_komut 파일의 머리부와 적재 구역을 검증한다. */
public final class yürütülebilir_yükleyici {
    public static final class bölüm_değer_366e0bfa {
        private final int Tip_değer;
        private final int bayrak_değer;
        private final int ADRES;
        private final int Dosya_konum;
        private final int Boyut;

        bölüm_değer_366e0bfa(int Tip_değer, int bayrak_değer, int ADRES, int Dosya_konum, int Boyut) {
            this.Tip_değer = Tip_değer;
            this.bayrak_değer = bayrak_değer;
            this.ADRES = ADRES;
            this.Dosya_konum = Dosya_konum;
            this.Boyut = Boyut;
        }

        public int Tip_değer() {
            return Tip_değer;
        }

        public int bayrak_değer() {
            return bayrak_değer;
        }

        public int ADRES() {
            return ADRES;
        }

        public int Dosya_konum() {
            return Dosya_konum;
        }

        public int Boyut() {
            return Boyut;
        }
    }

    public static final class RESİM {
        private final int Start_ADRES;
        private final List<bölüm_değer_366e0bfa> 구역들;

        RESİM(int Start_ADRES, List<bölüm_değer_366e0bfa> 구역들) {
            this.Start_ADRES = Start_ADRES;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_ADRES() {
            return Start_ADRES;
        }

        public List<bölüm_değer_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public RESİM 검사(byte[] veri) {
        if (veri == null || veri.length < 52
                || veri[0] != 0x7f || veri[1] != 'E' || veri[2] != 'L' || veri[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (veri[4] != 1 || veri[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_ADRES = ayrıştırmak_bilgi(veri, 24);
        int bölüm_tablo_konum = ayrıştırmak_bilgi(veri, 32);
        int bölüm_girdi_boyutlandırmak = 짧은정수읽기(veri, 46);
        int bölüm_BAĞ_DEĞ_SAY = 짧은정수읽기(veri, 48);
        if (bölüm_girdi_boyutlandırmak < 40 || bölüm_tablo_konum < 0
                || (long) bölüm_tablo_konum + (long) bölüm_girdi_boyutlandırmak * bölüm_BAĞ_DEĞ_SAY > veri.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<bölüm_değer_366e0bfa> 구역들 = new ArrayList<bölüm_değer_366e0bfa>();
        for (int Dizin = 0; Dizin < bölüm_BAĞ_DEĞ_SAY; Dizin++) {
            int konum = bölüm_tablo_konum + Dizin * bölüm_girdi_boyutlandırmak;
            int Tip_değer = ayrıştırmak_bilgi(veri, konum + 4);
            int bayrak_değer = ayrıştırmak_bilgi(veri, konum + 8);
            int ADRES = ayrıştırmak_bilgi(veri, konum + 12);
            int Dosya_konum = ayrıştırmak_bilgi(veri, konum + 16);
            int Boyut = ayrıştırmak_bilgi(veri, konum + 20);
            if (Boyut < 0 || (Tip_değer != 8 && ((long) Dosya_konum + Boyut > veri.length || Dosya_konum < 0))) {
                throw new IllegalArgumentException("ELF bölüm_değer_366e0bfa veri 범위가 올바르지 않습니다.");
            }
            구역들.add(new bölüm_değer_366e0bfa(Tip_değer, bayrak_değer, ADRES, Dosya_konum, Boyut));
        }
        return new RESİM(Start_ADRES, 구역들);
    }

    private int ayrıştırmak_bilgi(byte[] veri, int konum) {
        if (konum < 0 || konum > veri.length - 4) {
            throw new IllegalArgumentException("ELF bilgi 범위를 벗어났습니다.");
        }
        return (veri[konum] & 0xff)
                | ((veri[konum + 1] & 0xff) << 8)
                | ((veri[konum + 2] & 0xff) << 16)
                | ((veri[konum + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] veri, int konum) {
        if (konum < 0 || konum > veri.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 bilgi 범위를 벗어났습니다.");
        }
        return (veri[konum] & 0xff) | ((veri[konum + 1] & 0xff) << 8);
    }
}
