// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenija.JSvnOS.datotečni_sustav;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Izvrši_naredba 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sekcija_VALUE {
        private final int 종류;
        private final int zastavica_VALUE;
        private final int adresa;
        private final int Datoteka_položaj;
        private final int Veličina;

        sekcija_VALUE(int 종류, int zastavica_VALUE, int adresa, int Datoteka_položaj, int Veličina) {
            this.종류 = 종류;
            this.zastavica_VALUE = zastavica_VALUE;
            this.adresa = adresa;
            this.Datoteka_položaj = Datoteka_položaj;
            this.Veličina = Veličina;
        }

        public int 종류() {
            return 종류;
        }

        public int zastavica_VALUE() {
            return zastavica_VALUE;
        }

        public int adresa() {
            return adresa;
        }

        public int Datoteka_položaj() {
            return Datoteka_položaj;
        }

        public int Veličina() {
            return Veličina;
        }
    }

    public static final class IMAGE {
        private final int START_adresa;
        private final List<sekcija_VALUE> 구역들;

        IMAGE(int START_adresa, List<sekcija_VALUE> 구역들) {
            this.START_adresa = START_adresa;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_adresa() {
            return START_adresa;
        }

        public List<sekcija_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] podaci) {
        if (podaci == null || podaci.length < 52
                || podaci[0] != 0x7f || podaci[1] != 'E' || podaci[2] != 'L' || podaci[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (podaci[4] != 1 || podaci[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_adresa = rastavljati_cijeli_broj(podaci, 24);
        int sekcija_tablica_položaj = rastavljati_cijeli_broj(podaci, 32);
        int sekcija_unos_promijeniti_veličinu = 짧은정수읽기(podaci, 46);
        int sekcija_COUNT = 짧은정수읽기(podaci, 48);
        if (sekcija_unos_promijeniti_veličinu < 40 || sekcija_tablica_položaj < 0
                || (long) sekcija_tablica_položaj + (long) sekcija_unos_promijeniti_veličinu * sekcija_COUNT > podaci.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sekcija_VALUE> 구역들 = new ArrayList<sekcija_VALUE>();
        for (int INDEX = 0; INDEX < sekcija_COUNT; INDEX++) {
            int Položaj = sekcija_tablica_položaj + INDEX * sekcija_unos_promijeniti_veličinu;
            int 종류 = rastavljati_cijeli_broj(podaci, Položaj + 4);
            int zastavica_VALUE = rastavljati_cijeli_broj(podaci, Položaj + 8);
            int adresa = rastavljati_cijeli_broj(podaci, Položaj + 12);
            int Datoteka_položaj = rastavljati_cijeli_broj(podaci, Položaj + 16);
            int Veličina = rastavljati_cijeli_broj(podaci, Položaj + 20);
            if (Veličina < 0 || (종류 != 8 && ((long) Datoteka_položaj + Veličina > podaci.length || Datoteka_položaj < 0))) {
                throw new IllegalArgumentException("ELF sekcija_VALUE podaci 범위가 올바르지 않습니다.");
            }
            구역들.add(new sekcija_VALUE(종류, zastavica_VALUE, adresa, Datoteka_položaj, Veličina));
        }
        return new IMAGE(START_adresa, 구역들);
    }

    private int rastavljati_cijeli_broj(byte[] podaci, int Položaj) {
        if (Položaj < 0 || Položaj > podaci.length - 4) {
            throw new IllegalArgumentException("ELF cijeli_broj 범위를 벗어났습니다.");
        }
        return (podaci[Položaj] & 0xff)
                | ((podaci[Položaj + 1] & 0xff) << 8)
                | ((podaci[Položaj + 2] & 0xff) << 16)
                | ((podaci[Položaj + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] podaci, int Položaj) {
        if (Položaj < 0 || Položaj > podaci.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 cijeli_broj 범위를 벗어났습니다.");
        }
        return (podaci[Položaj] & 0xff) | ((podaci[Položaj + 1] & 0xff) << 8);
    }
}
