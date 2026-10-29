// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.tiedostojärjestelmä;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Suorita_komento 파일의 머리부와 적재 구역을 검증한다. */
public final class suoritettava_tiedosto_latausohjelma {
    public static final class osa_ARVO {
        private final int 종류;
        private final int merkitä_ARVO;
        private final int OSOITE;
        private final int Tiedosto_toimi;
        private final int Koko;

        osa_ARVO(int 종류, int merkitä_ARVO, int OSOITE, int Tiedosto_toimi, int Koko) {
            this.종류 = 종류;
            this.merkitä_ARVO = merkitä_ARVO;
            this.OSOITE = OSOITE;
            this.Tiedosto_toimi = Tiedosto_toimi;
            this.Koko = Koko;
        }

        public int 종류() {
            return 종류;
        }

        public int merkitä_ARVO() {
            return merkitä_ARVO;
        }

        public int OSOITE() {
            return OSOITE;
        }

        public int Tiedosto_toimi() {
            return Tiedosto_toimi;
        }

        public int Koko() {
            return Koko;
        }
    }

    public static final class KUVA {
        private final int alku_OSOITE;
        private final List<osa_ARVO> 구역들;

        KUVA(int alku_OSOITE, List<osa_ARVO> 구역들) {
            this.alku_OSOITE = alku_OSOITE;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int alku_OSOITE() {
            return alku_OSOITE;
        }

        public List<osa_ARVO> 구역들() {
            return 구역들;
        }
    }

    public KUVA 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int alku_OSOITE = jäsentää_kokonaisluku(data, 24);
        int osa_taulukko_toimi = jäsentää_kokonaisluku(data, 32);
        int osa_merkintä_muuttaa_kokoa = 짧은정수읽기(data, 46);
        int osa_LASKE = 짧은정수읽기(data, 48);
        if (osa_merkintä_muuttaa_kokoa < 40 || osa_taulukko_toimi < 0
                || (long) osa_taulukko_toimi + (long) osa_merkintä_muuttaa_kokoa * osa_LASKE > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<osa_ARVO> 구역들 = new ArrayList<osa_ARVO>();
        for (int INDEKSI = 0; INDEKSI < osa_LASKE; INDEKSI++) {
            int paikka = osa_taulukko_toimi + INDEKSI * osa_merkintä_muuttaa_kokoa;
            int 종류 = jäsentää_kokonaisluku(data, paikka + 4);
            int merkitä_ARVO = jäsentää_kokonaisluku(data, paikka + 8);
            int OSOITE = jäsentää_kokonaisluku(data, paikka + 12);
            int Tiedosto_toimi = jäsentää_kokonaisluku(data, paikka + 16);
            int Koko = jäsentää_kokonaisluku(data, paikka + 20);
            if (Koko < 0 || (종류 != 8 && ((long) Tiedosto_toimi + Koko > data.length || Tiedosto_toimi < 0))) {
                throw new IllegalArgumentException("ELF osa_ARVO data 범위가 올바르지 않습니다.");
            }
            구역들.add(new osa_ARVO(종류, merkitä_ARVO, OSOITE, Tiedosto_toimi, Koko));
        }
        return new KUVA(alku_OSOITE, 구역들);
    }

    private int jäsentää_kokonaisluku(byte[] data, int paikka) {
        if (paikka < 0 || paikka > data.length - 4) {
            throw new IllegalArgumentException("ELF kokonaisluku 범위를 벗어났습니다.");
        }
        return (data[paikka] & 0xff)
                | ((data[paikka + 1] & 0xff) << 8)
                | ((data[paikka + 2] & 0xff) << 16)
                | ((data[paikka + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int paikka) {
        if (paikka < 0 || paikka > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 kokonaisluku 범위를 벗어났습니다.");
        }
        return (data[paikka] & 0xff) | ((data[paikka + 1] & 0xff) << 8);
    }
}
