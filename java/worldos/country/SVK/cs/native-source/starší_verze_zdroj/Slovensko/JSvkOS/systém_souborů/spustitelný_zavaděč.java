// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.systém_souborů;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Provést_příkaz 파일의 머리부와 적재 구역을 검증한다. */
public final class spustitelný_zavaděč {
    public static final class oddíl_HODNOTA_366e0bfa {
        private final int Druh_HODNOTA;
        private final int příznak_HODNOTA;
        private final int Adresa;
        private final int Soubor_pozice;
        private final int Velikost;

        oddíl_HODNOTA_366e0bfa(int Druh_HODNOTA, int příznak_HODNOTA, int Adresa, int Soubor_pozice, int Velikost) {
            this.Druh_HODNOTA = Druh_HODNOTA;
            this.příznak_HODNOTA = příznak_HODNOTA;
            this.Adresa = Adresa;
            this.Soubor_pozice = Soubor_pozice;
            this.Velikost = Velikost;
        }

        public int Druh_HODNOTA() {
            return Druh_HODNOTA;
        }

        public int příznak_HODNOTA() {
            return příznak_HODNOTA;
        }

        public int Adresa() {
            return Adresa;
        }

        public int Soubor_pozice() {
            return Soubor_pozice;
        }

        public int Velikost() {
            return Velikost;
        }
    }

    public static final class image {
        private final int START_ODKAZ;
        private final List<oddíl_HODNOTA_366e0bfa> 구역들;

        image(int START_ODKAZ, List<oddíl_HODNOTA_366e0bfa> 구역들) {
            this.START_ODKAZ = START_ODKAZ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ODKAZ() {
            return START_ODKAZ;
        }

        public List<oddíl_HODNOTA_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public image 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ODKAZ = parsovat_integer(data, 24);
        int oddíl_tabulka_pozice = parsovat_integer(data, 32);
        int oddíl_položka_změnit_velikost = 짧은정수읽기(data, 46);
        int oddíl_POČET = 짧은정수읽기(data, 48);
        if (oddíl_položka_změnit_velikost < 40 || oddíl_tabulka_pozice < 0
                || (long) oddíl_tabulka_pozice + (long) oddíl_položka_změnit_velikost * oddíl_POČET > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<oddíl_HODNOTA_366e0bfa> 구역들 = new ArrayList<oddíl_HODNOTA_366e0bfa>();
        for (int INDEX = 0; INDEX < oddíl_POČET; INDEX++) {
            int pozice = oddíl_tabulka_pozice + INDEX * oddíl_položka_změnit_velikost;
            int Druh_HODNOTA = parsovat_integer(data, pozice + 4);
            int příznak_HODNOTA = parsovat_integer(data, pozice + 8);
            int Adresa = parsovat_integer(data, pozice + 12);
            int Soubor_pozice = parsovat_integer(data, pozice + 16);
            int Velikost = parsovat_integer(data, pozice + 20);
            if (Velikost < 0 || (Druh_HODNOTA != 8 && ((long) Soubor_pozice + Velikost > data.length || Soubor_pozice < 0))) {
                throw new IllegalArgumentException("ELF oddíl_HODNOTA_366e0bfa data 범위가 올바르지 않습니다.");
            }
            구역들.add(new oddíl_HODNOTA_366e0bfa(Druh_HODNOTA, příznak_HODNOTA, Adresa, Soubor_pozice, Velikost));
        }
        return new image(START_ODKAZ, 구역들);
    }

    private int parsovat_integer(byte[] data, int pozice) {
        if (pozice < 0 || pozice > data.length - 4) {
            throw new IllegalArgumentException("ELF integer 범위를 벗어났습니다.");
        }
        return (data[pozice] & 0xff)
                | ((data[pozice + 1] & 0xff) << 8)
                | ((data[pozice + 2] & 0xff) << 16)
                | ((data[pozice + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int pozice) {
        if (pozice < 0 || pozice > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 integer 범위를 벗어났습니다.");
        }
        return (data[pozice] & 0xff) | ((data[pozice + 1] & 0xff) << 8);
    }
}
