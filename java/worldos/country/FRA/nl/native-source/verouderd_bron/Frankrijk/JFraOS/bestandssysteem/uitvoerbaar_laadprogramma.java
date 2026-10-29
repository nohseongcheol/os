// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankrijk.JFraOS.bestandssysteem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Uitvoeren_opdracht 파일의 머리부와 적재 구역을 검증한다. */
public final class uitvoerbaar_laadprogramma {
    public static final class sectie_WAARDE {
        private final int soort_WAARDE;
        private final int vlag_WAARDE;
        private final int ADRES;
        private final int Bestand_functie;
        private final int Grootte;

        sectie_WAARDE(int soort_WAARDE, int vlag_WAARDE, int ADRES, int Bestand_functie, int Grootte) {
            this.soort_WAARDE = soort_WAARDE;
            this.vlag_WAARDE = vlag_WAARDE;
            this.ADRES = ADRES;
            this.Bestand_functie = Bestand_functie;
            this.Grootte = Grootte;
        }

        public int soort_WAARDE() {
            return soort_WAARDE;
        }

        public int vlag_WAARDE() {
            return vlag_WAARDE;
        }

        public int ADRES() {
            return ADRES;
        }

        public int Bestand_functie() {
            return Bestand_functie;
        }

        public int Grootte() {
            return Grootte;
        }
    }

    public static final class kopie {
        private final int START_ADRES;
        private final List<sectie_WAARDE> 구역들;

        kopie(int START_ADRES, List<sectie_WAARDE> 구역들) {
            this.START_ADRES = START_ADRES;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ADRES() {
            return START_ADRES;
        }

        public List<sectie_WAARDE> 구역들() {
            return 구역들;
        }
    }

    public kopie 검사(byte[] gegevens) {
        if (gegevens == null || gegevens.length < 52
                || gegevens[0] != 0x7f || gegevens[1] != 'E' || gegevens[2] != 'L' || gegevens[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (gegevens[4] != 1 || gegevens[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ADRES = parseren_geheel_getal(gegevens, 24);
        int sectie_tabel_functie = parseren_geheel_getal(gegevens, 32);
        int sectie_invoer_formaat_wijzigen = 짧은정수읽기(gegevens, 46);
        int sectie_AANTAL = 짧은정수읽기(gegevens, 48);
        if (sectie_invoer_formaat_wijzigen < 40 || sectie_tabel_functie < 0
                || (long) sectie_tabel_functie + (long) sectie_invoer_formaat_wijzigen * sectie_AANTAL > gegevens.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sectie_WAARDE> 구역들 = new ArrayList<sectie_WAARDE>();
        for (int INDEX = 0; INDEX < sectie_AANTAL; INDEX++) {
            int positie = sectie_tabel_functie + INDEX * sectie_invoer_formaat_wijzigen;
            int soort_WAARDE = parseren_geheel_getal(gegevens, positie + 4);
            int vlag_WAARDE = parseren_geheel_getal(gegevens, positie + 8);
            int ADRES = parseren_geheel_getal(gegevens, positie + 12);
            int Bestand_functie = parseren_geheel_getal(gegevens, positie + 16);
            int Grootte = parseren_geheel_getal(gegevens, positie + 20);
            if (Grootte < 0 || (soort_WAARDE != 8 && ((long) Bestand_functie + Grootte > gegevens.length || Bestand_functie < 0))) {
                throw new IllegalArgumentException("ELF sectie_WAARDE gegevens 범위가 올바르지 않습니다.");
            }
            구역들.add(new sectie_WAARDE(soort_WAARDE, vlag_WAARDE, ADRES, Bestand_functie, Grootte));
        }
        return new kopie(START_ADRES, 구역들);
    }

    private int parseren_geheel_getal(byte[] gegevens, int positie) {
        if (positie < 0 || positie > gegevens.length - 4) {
            throw new IllegalArgumentException("ELF geheel_getal 범위를 벗어났습니다.");
        }
        return (gegevens[positie] & 0xff)
                | ((gegevens[positie + 1] & 0xff) << 8)
                | ((gegevens[positie + 2] & 0xff) << 16)
                | ((gegevens[positie + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] gegevens, int positie) {
        if (positie < 0 || positie > gegevens.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 geheel_getal 범위를 벗어났습니다.");
        }
        return (gegevens[positie] & 0xff) | ((gegevens[positie + 1] & 0xff) << 8);
    }
}
