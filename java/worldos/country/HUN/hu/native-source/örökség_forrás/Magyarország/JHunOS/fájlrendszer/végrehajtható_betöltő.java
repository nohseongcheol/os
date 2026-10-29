// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Magyarország.JHunOS.fájlrendszer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian végrehajt_parancs 파일의 머리부와 적재 구역을 검증한다. */
public final class végrehajtható_betöltő {
    public static final class szakasz_ÉRTÉK {
        private final int Altípus_ÉRTÉK;
        private final int jelölő_ÉRTÉK_58846146;
        private final int CÍM;
        private final int Fájl_pozíció;
        private final int Méret;

        szakasz_ÉRTÉK(int Altípus_ÉRTÉK, int jelölő_ÉRTÉK_58846146, int CÍM, int Fájl_pozíció, int Méret) {
            this.Altípus_ÉRTÉK = Altípus_ÉRTÉK;
            this.jelölő_ÉRTÉK_58846146 = jelölő_ÉRTÉK_58846146;
            this.CÍM = CÍM;
            this.Fájl_pozíció = Fájl_pozíció;
            this.Méret = Méret;
        }

        public int Altípus_ÉRTÉK() {
            return Altípus_ÉRTÉK;
        }

        public int jelölő_ÉRTÉK_58846146() {
            return jelölő_ÉRTÉK_58846146;
        }

        public int CÍM() {
            return CÍM;
        }

        public int Fájl_pozíció() {
            return Fájl_pozíció;
        }

        public int Méret() {
            return Méret;
        }
    }

    public static final class KÉP {
        private final int START_CÍM;
        private final List<szakasz_ÉRTÉK> 구역들;

        KÉP(int START_CÍM, List<szakasz_ÉRTÉK> 구역들) {
            this.START_CÍM = START_CÍM;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_CÍM() {
            return START_CÍM;
        }

        public List<szakasz_ÉRTÉK> 구역들() {
            return 구역들;
        }
    }

    public KÉP 검사(byte[] adat) {
        if (adat == null || adat.length < 52
                || adat[0] != 0x7f || adat[1] != 'E' || adat[2] != 'L' || adat[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (adat[4] != 1 || adat[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_CÍM = elemez_egész_szám(adat, 24);
        int szakasz_tábla_pozíció = elemez_egész_szám(adat, 32);
        int szakasz_bejegyzés_méretez = 짧은정수읽기(adat, 46);
        int szakasz_DARAB = 짧은정수읽기(adat, 48);
        if (szakasz_bejegyzés_méretez < 40 || szakasz_tábla_pozíció < 0
                || (long) szakasz_tábla_pozíció + (long) szakasz_bejegyzés_méretez * szakasz_DARAB > adat.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<szakasz_ÉRTÉK> 구역들 = new ArrayList<szakasz_ÉRTÉK>();
        for (int INDEX = 0; INDEX < szakasz_DARAB; INDEX++) {
            int Pozíció = szakasz_tábla_pozíció + INDEX * szakasz_bejegyzés_méretez;
            int Altípus_ÉRTÉK = elemez_egész_szám(adat, Pozíció + 4);
            int jelölő_ÉRTÉK_58846146 = elemez_egész_szám(adat, Pozíció + 8);
            int CÍM = elemez_egész_szám(adat, Pozíció + 12);
            int Fájl_pozíció = elemez_egész_szám(adat, Pozíció + 16);
            int Méret = elemez_egész_szám(adat, Pozíció + 20);
            if (Méret < 0 || (Altípus_ÉRTÉK != 8 && ((long) Fájl_pozíció + Méret > adat.length || Fájl_pozíció < 0))) {
                throw new IllegalArgumentException("ELF szakasz_ÉRTÉK adat 범위가 올바르지 않습니다.");
            }
            구역들.add(new szakasz_ÉRTÉK(Altípus_ÉRTÉK, jelölő_ÉRTÉK_58846146, CÍM, Fájl_pozíció, Méret));
        }
        return new KÉP(START_CÍM, 구역들);
    }

    private int elemez_egész_szám(byte[] adat, int Pozíció) {
        if (Pozíció < 0 || Pozíció > adat.length - 4) {
            throw new IllegalArgumentException("ELF egész_szám 범위를 벗어났습니다.");
        }
        return (adat[Pozíció] & 0xff)
                | ((adat[Pozíció + 1] & 0xff) << 8)
                | ((adat[Pozíció + 2] & 0xff) << 16)
                | ((adat[Pozíció + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] adat, int Pozíció) {
        if (Pozíció < 0 || Pozíció > adat.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 egész_szám 범위를 벗어났습니다.");
        }
        return (adat[Pozíció] & 0xff) | ((adat[Pozíció + 1] & 0xff) << 8);
    }
}
