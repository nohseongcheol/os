// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuva.JLtuOS.failų_sistema;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Vykdyti_komanda 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sekcija_VALUE {
        private final int 종류;
        private final int žymė_VALUE;
        private final int ADDRESS;
        private final int Failas_padėtis;
        private final int Dydis;

        sekcija_VALUE(int 종류, int žymė_VALUE, int ADDRESS, int Failas_padėtis, int Dydis) {
            this.종류 = 종류;
            this.žymė_VALUE = žymė_VALUE;
            this.ADDRESS = ADDRESS;
            this.Failas_padėtis = Failas_padėtis;
            this.Dydis = Dydis;
        }

        public int 종류() {
            return 종류;
        }

        public int žymė_VALUE() {
            return žymė_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int Failas_padėtis() {
            return Failas_padėtis;
        }

        public int Dydis() {
            return Dydis;
        }
    }

    public static final class IMAGE {
        private final int Start_ADDRESS;
        private final List<sekcija_VALUE> 구역들;

        IMAGE(int Start_ADDRESS, List<sekcija_VALUE> 구역들) {
            this.Start_ADDRESS = Start_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_ADDRESS() {
            return Start_ADDRESS;
        }

        public List<sekcija_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] duomenys) {
        if (duomenys == null || duomenys.length < 52
                || duomenys[0] != 0x7f || duomenys[1] != 'E' || duomenys[2] != 'L' || duomenys[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (duomenys[4] != 1 || duomenys[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_ADDRESS = analizuoti_sintaksę_sveikasis_skaičius(duomenys, 24);
        int sekcija_lentelė_padėtis = analizuoti_sintaksę_sveikasis_skaičius(duomenys, 32);
        int sekcija_įrašas_dydis = 짧은정수읽기(duomenys, 46);
        int sekcija_COUNT = 짧은정수읽기(duomenys, 48);
        if (sekcija_įrašas_dydis < 40 || sekcija_lentelė_padėtis < 0
                || (long) sekcija_lentelė_padėtis + (long) sekcija_įrašas_dydis * sekcija_COUNT > duomenys.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sekcija_VALUE> 구역들 = new ArrayList<sekcija_VALUE>();
        for (int INDEX = 0; INDEX < sekcija_COUNT; INDEX++) {
            int Pozicija = sekcija_lentelė_padėtis + INDEX * sekcija_įrašas_dydis;
            int 종류 = analizuoti_sintaksę_sveikasis_skaičius(duomenys, Pozicija + 4);
            int žymė_VALUE = analizuoti_sintaksę_sveikasis_skaičius(duomenys, Pozicija + 8);
            int ADDRESS = analizuoti_sintaksę_sveikasis_skaičius(duomenys, Pozicija + 12);
            int Failas_padėtis = analizuoti_sintaksę_sveikasis_skaičius(duomenys, Pozicija + 16);
            int Dydis = analizuoti_sintaksę_sveikasis_skaičius(duomenys, Pozicija + 20);
            if (Dydis < 0 || (종류 != 8 && ((long) Failas_padėtis + Dydis > duomenys.length || Failas_padėtis < 0))) {
                throw new IllegalArgumentException("ELF sekcija_VALUE duomenys 범위가 올바르지 않습니다.");
            }
            구역들.add(new sekcija_VALUE(종류, žymė_VALUE, ADDRESS, Failas_padėtis, Dydis));
        }
        return new IMAGE(Start_ADDRESS, 구역들);
    }

    private int analizuoti_sintaksę_sveikasis_skaičius(byte[] duomenys, int Pozicija) {
        if (Pozicija < 0 || Pozicija > duomenys.length - 4) {
            throw new IllegalArgumentException("ELF sveikasis_skaičius 범위를 벗어났습니다.");
        }
        return (duomenys[Pozicija] & 0xff)
                | ((duomenys[Pozicija + 1] & 0xff) << 8)
                | ((duomenys[Pozicija + 2] & 0xff) << 16)
                | ((duomenys[Pozicija + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] duomenys, int Pozicija) {
        if (Pozicija < 0 || Pozicija > duomenys.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 sveikasis_skaičius 범위를 벗어났습니다.");
        }
        return (duomenys[Pozicija] & 0xff) | ((duomenys[Pozicija + 1] & 0xff) << 8);
    }
}
