// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.lêerstelsel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian uitvoer_bevel 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class seksie_VALUE {
        private final int 종류;
        private final int vlag_VALUE;
        private final int adres;
        private final int lêer_plaas;
        private final int Grootte;

        seksie_VALUE(int 종류, int vlag_VALUE, int adres, int lêer_plaas, int Grootte) {
            this.종류 = 종류;
            this.vlag_VALUE = vlag_VALUE;
            this.adres = adres;
            this.lêer_plaas = lêer_plaas;
            this.Grootte = Grootte;
        }

        public int 종류() {
            return 종류;
        }

        public int vlag_VALUE() {
            return vlag_VALUE;
        }

        public int adres() {
            return adres;
        }

        public int lêer_plaas() {
            return lêer_plaas;
        }

        public int Grootte() {
            return Grootte;
        }
    }

    public static final class foto {
        private final int BEGIN_adres;
        private final List<seksie_VALUE> 구역들;

        foto(int BEGIN_adres, List<seksie_VALUE> 구역들) {
            this.BEGIN_adres = BEGIN_adres;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int BEGIN_adres() {
            return BEGIN_adres;
        }

        public List<seksie_VALUE> 구역들() {
            return 구역들;
        }
    }

    public foto 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int BEGIN_adres = ontleed_heelgetal(data, 24);
        int seksie_tabel_plaas = ontleed_heelgetal(data, 32);
        int seksie_inskrywing_verstel = 짧은정수읽기(data, 46);
        int seksie_COUNT = 짧은정수읽기(data, 48);
        if (seksie_inskrywing_verstel < 40 || seksie_tabel_plaas < 0
                || (long) seksie_tabel_plaas + (long) seksie_inskrywing_verstel * seksie_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seksie_VALUE> 구역들 = new ArrayList<seksie_VALUE>();
        for (int INDEX = 0; INDEX < seksie_COUNT; INDEX++) {
            int Posisie = seksie_tabel_plaas + INDEX * seksie_inskrywing_verstel;
            int 종류 = ontleed_heelgetal(data, Posisie + 4);
            int vlag_VALUE = ontleed_heelgetal(data, Posisie + 8);
            int adres = ontleed_heelgetal(data, Posisie + 12);
            int lêer_plaas = ontleed_heelgetal(data, Posisie + 16);
            int Grootte = ontleed_heelgetal(data, Posisie + 20);
            if (Grootte < 0 || (종류 != 8 && ((long) lêer_plaas + Grootte > data.length || lêer_plaas < 0))) {
                throw new IllegalArgumentException("ELF seksie_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new seksie_VALUE(종류, vlag_VALUE, adres, lêer_plaas, Grootte));
        }
        return new foto(BEGIN_adres, 구역들);
    }

    private int ontleed_heelgetal(byte[] data, int Posisie) {
        if (Posisie < 0 || Posisie > data.length - 4) {
            throw new IllegalArgumentException("ELF heelgetal 범위를 벗어났습니다.");
        }
        return (data[Posisie] & 0xff)
                | ((data[Posisie + 1] & 0xff) << 8)
                | ((data[Posisie + 2] & 0xff) << 16)
                | ((data[Posisie + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int Posisie) {
        if (Posisie < 0 || Posisie > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heelgetal 범위를 벗어났습니다.");
        }
        return (data[Posisie] & 0xff) | ((data[Posisie + 1] & 0xff) << 8);
    }
}
