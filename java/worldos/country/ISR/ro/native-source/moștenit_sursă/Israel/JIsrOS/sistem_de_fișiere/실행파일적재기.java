// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Israel.JIsrOS.sistem_de_fișiere;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian executa_comandă 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class secțiune_VALUE {
        private final int 종류;
        private final int fanion_VALUE;
        private final int adresa;
        private final int Fișier_poziție;
        private final int Mărime;

        secțiune_VALUE(int 종류, int fanion_VALUE, int adresa, int Fișier_poziție, int Mărime) {
            this.종류 = 종류;
            this.fanion_VALUE = fanion_VALUE;
            this.adresa = adresa;
            this.Fișier_poziție = Fișier_poziție;
            this.Mărime = Mărime;
        }

        public int 종류() {
            return 종류;
        }

        public int fanion_VALUE() {
            return fanion_VALUE;
        }

        public int adresa() {
            return adresa;
        }

        public int Fișier_poziție() {
            return Fișier_poziție;
        }

        public int Mărime() {
            return Mărime;
        }
    }

    public static final class IMAGE {
        private final int buta_adresa;
        private final List<secțiune_VALUE> 구역들;

        IMAGE(int buta_adresa, List<secțiune_VALUE> 구역들) {
            this.buta_adresa = buta_adresa;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int buta_adresa() {
            return buta_adresa;
        }

        public List<secțiune_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] date) {
        if (date == null || date.length < 52
                || date[0] != 0x7f || date[1] != 'E' || date[2] != 'L' || date[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (date[4] != 1 || date[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int buta_adresa = analiza_întreg(date, 24);
        int secțiune_tabel_poziție = analiza_întreg(date, 32);
        int secțiune_intrare_dimensiona = 짧은정수읽기(date, 46);
        int secțiune_COUNT = 짧은정수읽기(date, 48);
        if (secțiune_intrare_dimensiona < 40 || secțiune_tabel_poziție < 0
                || (long) secțiune_tabel_poziție + (long) secțiune_intrare_dimensiona * secțiune_COUNT > date.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<secțiune_VALUE> 구역들 = new ArrayList<secțiune_VALUE>();
        for (int INDEX = 0; INDEX < secțiune_COUNT; INDEX++) {
            int Poziție = secțiune_tabel_poziție + INDEX * secțiune_intrare_dimensiona;
            int 종류 = analiza_întreg(date, Poziție + 4);
            int fanion_VALUE = analiza_întreg(date, Poziție + 8);
            int adresa = analiza_întreg(date, Poziție + 12);
            int Fișier_poziție = analiza_întreg(date, Poziție + 16);
            int Mărime = analiza_întreg(date, Poziție + 20);
            if (Mărime < 0 || (종류 != 8 && ((long) Fișier_poziție + Mărime > date.length || Fișier_poziție < 0))) {
                throw new IllegalArgumentException("ELF secțiune_VALUE date 범위가 올바르지 않습니다.");
            }
            구역들.add(new secțiune_VALUE(종류, fanion_VALUE, adresa, Fișier_poziție, Mărime));
        }
        return new IMAGE(buta_adresa, 구역들);
    }

    private int analiza_întreg(byte[] date, int Poziție) {
        if (Poziție < 0 || Poziție > date.length - 4) {
            throw new IllegalArgumentException("ELF întreg 범위를 벗어났습니다.");
        }
        return (date[Poziție] & 0xff)
                | ((date[Poziție + 1] & 0xff) << 8)
                | ((date[Poziție + 2] & 0xff) << 16)
                | ((date[Poziție + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] date, int Poziție) {
        if (Poziție < 0 || Poziție > date.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 întreg 범위를 벗어났습니다.");
        }
        return (date[Poziție] & 0xff) | ((date[Poziție + 1] & 0xff) << 8);
    }
}
