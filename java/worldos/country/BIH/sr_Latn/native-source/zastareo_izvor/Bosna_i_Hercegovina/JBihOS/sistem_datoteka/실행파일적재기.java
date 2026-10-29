// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.sistem_datoteka;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Izvrši_komanda 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class odeljak_VALUE {
        private final int 종류;
        private final int zastavica_VALUE;
        private final int adresa;
        private final int Datoteka_pozicija;
        private final int promeniti_veličinu;

        odeljak_VALUE(int 종류, int zastavica_VALUE, int adresa, int Datoteka_pozicija, int promeniti_veličinu) {
            this.종류 = 종류;
            this.zastavica_VALUE = zastavica_VALUE;
            this.adresa = adresa;
            this.Datoteka_pozicija = Datoteka_pozicija;
            this.promeniti_veličinu = promeniti_veličinu;
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

        public int Datoteka_pozicija() {
            return Datoteka_pozicija;
        }

        public int promeniti_veličinu() {
            return promeniti_veličinu;
        }
    }

    public static final class IMAGE {
        private final int START_adresa;
        private final List<odeljak_VALUE> 구역들;

        IMAGE(int START_adresa, List<odeljak_VALUE> 구역들) {
            this.START_adresa = START_adresa;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_adresa() {
            return START_adresa;
        }

        public List<odeljak_VALUE> 구역들() {
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
        int START_adresa = raščlaniti_ceo_broj(podaci, 24);
        int odeljak_tabela_pozicija = raščlaniti_ceo_broj(podaci, 32);
        int odeljak_stavka_promeniti_veličinu = 짧은정수읽기(podaci, 46);
        int odeljak_COUNT = 짧은정수읽기(podaci, 48);
        if (odeljak_stavka_promeniti_veličinu < 40 || odeljak_tabela_pozicija < 0
                || (long) odeljak_tabela_pozicija + (long) odeljak_stavka_promeniti_veličinu * odeljak_COUNT > podaci.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<odeljak_VALUE> 구역들 = new ArrayList<odeljak_VALUE>();
        for (int INDEX = 0; INDEX < odeljak_COUNT; INDEX++) {
            int pozicija = odeljak_tabela_pozicija + INDEX * odeljak_stavka_promeniti_veličinu;
            int 종류 = raščlaniti_ceo_broj(podaci, pozicija + 4);
            int zastavica_VALUE = raščlaniti_ceo_broj(podaci, pozicija + 8);
            int adresa = raščlaniti_ceo_broj(podaci, pozicija + 12);
            int Datoteka_pozicija = raščlaniti_ceo_broj(podaci, pozicija + 16);
            int promeniti_veličinu = raščlaniti_ceo_broj(podaci, pozicija + 20);
            if (promeniti_veličinu < 0 || (종류 != 8 && ((long) Datoteka_pozicija + promeniti_veličinu > podaci.length || Datoteka_pozicija < 0))) {
                throw new IllegalArgumentException("ELF odeljak_VALUE podaci 범위가 올바르지 않습니다.");
            }
            구역들.add(new odeljak_VALUE(종류, zastavica_VALUE, adresa, Datoteka_pozicija, promeniti_veličinu));
        }
        return new IMAGE(START_adresa, 구역들);
    }

    private int raščlaniti_ceo_broj(byte[] podaci, int pozicija) {
        if (pozicija < 0 || pozicija > podaci.length - 4) {
            throw new IllegalArgumentException("ELF ceo_broj 범위를 벗어났습니다.");
        }
        return (podaci[pozicija] & 0xff)
                | ((podaci[pozicija + 1] & 0xff) << 8)
                | ((podaci[pozicija + 2] & 0xff) << 16)
                | ((podaci[pozicija + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] podaci, int pozicija) {
        if (pozicija < 0 || pozicija > podaci.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ceo_broj 범위를 벗어났습니다.");
        }
        return (podaci[pozicija] & 0xff) | ((podaci[pozicija + 1] & 0xff) << 8);
    }
}
