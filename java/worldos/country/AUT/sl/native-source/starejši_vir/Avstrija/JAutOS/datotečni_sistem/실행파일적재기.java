// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.datotečni_sistem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Izvedi_ukaz 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class odsek_VALUE {
        private final int 종류;
        private final int zastavica_VALUE;
        private final int naslov;
        private final int Datoteka_položaj;
        private final int Velikost;

        odsek_VALUE(int 종류, int zastavica_VALUE, int naslov, int Datoteka_položaj, int Velikost) {
            this.종류 = 종류;
            this.zastavica_VALUE = zastavica_VALUE;
            this.naslov = naslov;
            this.Datoteka_položaj = Datoteka_položaj;
            this.Velikost = Velikost;
        }

        public int 종류() {
            return 종류;
        }

        public int zastavica_VALUE() {
            return zastavica_VALUE;
        }

        public int naslov() {
            return naslov;
        }

        public int Datoteka_položaj() {
            return Datoteka_položaj;
        }

        public int Velikost() {
            return Velikost;
        }
    }

    public static final class IMAGE {
        private final int Start_naslov;
        private final List<odsek_VALUE> 구역들;

        IMAGE(int Start_naslov, List<odsek_VALUE> 구역들) {
            this.Start_naslov = Start_naslov;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_naslov() {
            return Start_naslov;
        }

        public List<odsek_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] podatki) {
        if (podatki == null || podatki.length < 52
                || podatki[0] != 0x7f || podatki[1] != 'E' || podatki[2] != 'L' || podatki[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (podatki[4] != 1 || podatki[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_naslov = razčlenjevati_celo_število(podatki, 24);
        int odsek_tabela_položaj = razčlenjevati_celo_število(podatki, 32);
        int odsek_vnos_spremeniti_velikost = 짧은정수읽기(podatki, 46);
        int odsek_COUNT = 짧은정수읽기(podatki, 48);
        if (odsek_vnos_spremeniti_velikost < 40 || odsek_tabela_položaj < 0
                || (long) odsek_tabela_položaj + (long) odsek_vnos_spremeniti_velikost * odsek_COUNT > podatki.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<odsek_VALUE> 구역들 = new ArrayList<odsek_VALUE>();
        for (int INDEX = 0; INDEX < odsek_COUNT; INDEX++) {
            int Položaj = odsek_tabela_položaj + INDEX * odsek_vnos_spremeniti_velikost;
            int 종류 = razčlenjevati_celo_število(podatki, Položaj + 4);
            int zastavica_VALUE = razčlenjevati_celo_število(podatki, Položaj + 8);
            int naslov = razčlenjevati_celo_število(podatki, Položaj + 12);
            int Datoteka_položaj = razčlenjevati_celo_število(podatki, Položaj + 16);
            int Velikost = razčlenjevati_celo_število(podatki, Položaj + 20);
            if (Velikost < 0 || (종류 != 8 && ((long) Datoteka_položaj + Velikost > podatki.length || Datoteka_položaj < 0))) {
                throw new IllegalArgumentException("ELF odsek_VALUE podatki 범위가 올바르지 않습니다.");
            }
            구역들.add(new odsek_VALUE(종류, zastavica_VALUE, naslov, Datoteka_položaj, Velikost));
        }
        return new IMAGE(Start_naslov, 구역들);
    }

    private int razčlenjevati_celo_število(byte[] podatki, int Položaj) {
        if (Položaj < 0 || Položaj > podatki.length - 4) {
            throw new IllegalArgumentException("ELF celo_število 범위를 벗어났습니다.");
        }
        return (podatki[Položaj] & 0xff)
                | ((podatki[Položaj + 1] & 0xff) << 8)
                | ((podatki[Položaj + 2] & 0xff) << 16)
                | ((podatki[Položaj + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] podatki, int Položaj) {
        if (Položaj < 0 || Položaj > podatki.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 celo_število 범위를 벗어났습니다.");
        }
        return (podatki[Položaj] & 0xff) | ((podatki[Položaj + 1] & 0xff) << 8);
    }
}
