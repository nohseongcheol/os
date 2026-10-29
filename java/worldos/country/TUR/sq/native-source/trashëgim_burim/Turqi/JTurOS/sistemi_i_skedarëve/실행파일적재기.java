// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turqi.JTurOS.sistemi_i_skedarëve;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian zbatoj_komandë 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class seksion_VALUE {
        private final int 종류;
        private final int flamur_VALUE;
        private final int email;
        private final int skedar_pozicioni;
        private final int Madhësi;

        seksion_VALUE(int 종류, int flamur_VALUE, int email, int skedar_pozicioni, int Madhësi) {
            this.종류 = 종류;
            this.flamur_VALUE = flamur_VALUE;
            this.email = email;
            this.skedar_pozicioni = skedar_pozicioni;
            this.Madhësi = Madhësi;
        }

        public int 종류() {
            return 종류;
        }

        public int flamur_VALUE() {
            return flamur_VALUE;
        }

        public int email() {
            return email;
        }

        public int skedar_pozicioni() {
            return skedar_pozicioni;
        }

        public int Madhësi() {
            return Madhësi;
        }
    }

    public static final class IMAGE {
        private final int nis_email;
        private final List<seksion_VALUE> 구역들;

        IMAGE(int nis_email, List<seksion_VALUE> 구역들) {
            this.nis_email = nis_email;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int nis_email() {
            return nis_email;
        }

        public List<seksion_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] të_dhëna) {
        if (të_dhëna == null || të_dhëna.length < 52
                || të_dhëna[0] != 0x7f || të_dhëna[1] != 'E' || të_dhëna[2] != 'L' || të_dhëna[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (të_dhëna[4] != 1 || të_dhëna[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int nis_email = analizoj_numër_i_plotë(të_dhëna, 24);
        int seksion_tabelë_pozicioni = analizoj_numër_i_plotë(të_dhëna, 32);
        int seksion_futje_ndryshoj_përmasat = 짧은정수읽기(të_dhëna, 46);
        int seksion_COUNT = 짧은정수읽기(të_dhëna, 48);
        if (seksion_futje_ndryshoj_përmasat < 40 || seksion_tabelë_pozicioni < 0
                || (long) seksion_tabelë_pozicioni + (long) seksion_futje_ndryshoj_përmasat * seksion_COUNT > të_dhëna.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seksion_VALUE> 구역들 = new ArrayList<seksion_VALUE>();
        for (int INDEX = 0; INDEX < seksion_COUNT; INDEX++) {
            int Pozicioni = seksion_tabelë_pozicioni + INDEX * seksion_futje_ndryshoj_përmasat;
            int 종류 = analizoj_numër_i_plotë(të_dhëna, Pozicioni + 4);
            int flamur_VALUE = analizoj_numër_i_plotë(të_dhëna, Pozicioni + 8);
            int email = analizoj_numër_i_plotë(të_dhëna, Pozicioni + 12);
            int skedar_pozicioni = analizoj_numër_i_plotë(të_dhëna, Pozicioni + 16);
            int Madhësi = analizoj_numër_i_plotë(të_dhëna, Pozicioni + 20);
            if (Madhësi < 0 || (종류 != 8 && ((long) skedar_pozicioni + Madhësi > të_dhëna.length || skedar_pozicioni < 0))) {
                throw new IllegalArgumentException("ELF seksion_VALUE të_dhëna 범위가 올바르지 않습니다.");
            }
            구역들.add(new seksion_VALUE(종류, flamur_VALUE, email, skedar_pozicioni, Madhësi));
        }
        return new IMAGE(nis_email, 구역들);
    }

    private int analizoj_numër_i_plotë(byte[] të_dhëna, int Pozicioni) {
        if (Pozicioni < 0 || Pozicioni > të_dhëna.length - 4) {
            throw new IllegalArgumentException("ELF numër_i_plotë 범위를 벗어났습니다.");
        }
        return (të_dhëna[Pozicioni] & 0xff)
                | ((të_dhëna[Pozicioni + 1] & 0xff) << 8)
                | ((të_dhëna[Pozicioni + 2] & 0xff) << 16)
                | ((të_dhëna[Pozicioni + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] të_dhëna, int Pozicioni) {
        if (Pozicioni < 0 || Pozicioni > të_dhëna.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 numër_i_plotë 범위를 벗어났습니다.");
        }
        return (të_dhëna[Pozicioni] & 0xff) | ((të_dhëna[Pozicioni + 1] & 0xff) << 8);
    }
}
