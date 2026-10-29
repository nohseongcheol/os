// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.fajl_sistem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Izvrši_komanda 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sekcija_VALUE {
        private final int 종류;
        private final int zastavica_VALUE;
        private final int adresa;
        private final int fajl_položaj;
        private final int Veličina;

        sekcija_VALUE(int 종류, int zastavica_VALUE, int adresa, int fajl_položaj, int Veličina) {
            this.종류 = 종류;
            this.zastavica_VALUE = zastavica_VALUE;
            this.adresa = adresa;
            this.fajl_položaj = fajl_položaj;
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

        public int fajl_položaj() {
            return fajl_položaj;
        }

        public int Veličina() {
            return Veličina;
        }
    }

    public static final class IMAGE {
        private final int početna_adresa;
        private final List<sekcija_VALUE> 구역들;

        IMAGE(int početna_adresa, List<sekcija_VALUE> 구역들) {
            this.početna_adresa = početna_adresa;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int početna_adresa() {
            return početna_adresa;
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
        int početna_adresa = raščlanjivati_cijeli_broj(podaci, 24);
        int sekcija_tabela_položaj = raščlanjivati_cijeli_broj(podaci, 32);
        int sekcija_unos_podesiti_veličinu = 짧은정수읽기(podaci, 46);
        int sekcija_COUNT = 짧은정수읽기(podaci, 48);
        if (sekcija_unos_podesiti_veličinu < 40 || sekcija_tabela_položaj < 0
                || (long) sekcija_tabela_položaj + (long) sekcija_unos_podesiti_veličinu * sekcija_COUNT > podaci.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sekcija_VALUE> 구역들 = new ArrayList<sekcija_VALUE>();
        for (int INDEX = 0; INDEX < sekcija_COUNT; INDEX++) {
            int Pozicija = sekcija_tabela_položaj + INDEX * sekcija_unos_podesiti_veličinu;
            int 종류 = raščlanjivati_cijeli_broj(podaci, Pozicija + 4);
            int zastavica_VALUE = raščlanjivati_cijeli_broj(podaci, Pozicija + 8);
            int adresa = raščlanjivati_cijeli_broj(podaci, Pozicija + 12);
            int fajl_položaj = raščlanjivati_cijeli_broj(podaci, Pozicija + 16);
            int Veličina = raščlanjivati_cijeli_broj(podaci, Pozicija + 20);
            if (Veličina < 0 || (종류 != 8 && ((long) fajl_položaj + Veličina > podaci.length || fajl_položaj < 0))) {
                throw new IllegalArgumentException("ELF sekcija_VALUE podaci 범위가 올바르지 않습니다.");
            }
            구역들.add(new sekcija_VALUE(종류, zastavica_VALUE, adresa, fajl_položaj, Veličina));
        }
        return new IMAGE(početna_adresa, 구역들);
    }

    private int raščlanjivati_cijeli_broj(byte[] podaci, int Pozicija) {
        if (Pozicija < 0 || Pozicija > podaci.length - 4) {
            throw new IllegalArgumentException("ELF cijeli_broj 범위를 벗어났습니다.");
        }
        return (podaci[Pozicija] & 0xff)
                | ((podaci[Pozicija + 1] & 0xff) << 8)
                | ((podaci[Pozicija + 2] & 0xff) << 16)
                | ((podaci[Pozicija + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] podaci, int Pozicija) {
        if (Pozicija < 0 || Pozicija > podaci.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 cijeli_broj 범위를 벗어났습니다.");
        }
        return (podaci[Pozicija] & 0xff) | ((podaci[Pozicija + 1] & 0xff) << 8);
    }
}
