// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.failisüsteem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Täida_käsk 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class jaotis_VALUE {
        private final int 종류;
        private final int lipp_VALUE;
        private final int ADDRESS;
        private final int Fail_ametikoht;
        private final int Suurus;

        jaotis_VALUE(int 종류, int lipp_VALUE, int ADDRESS, int Fail_ametikoht, int Suurus) {
            this.종류 = 종류;
            this.lipp_VALUE = lipp_VALUE;
            this.ADDRESS = ADDRESS;
            this.Fail_ametikoht = Fail_ametikoht;
            this.Suurus = Suurus;
        }

        public int 종류() {
            return 종류;
        }

        public int lipp_VALUE() {
            return lipp_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int Fail_ametikoht() {
            return Fail_ametikoht;
        }

        public int Suurus() {
            return Suurus;
        }
    }

    public static final class pilt {
        private final int START_ADDRESS;
        private final List<jaotis_VALUE> 구역들;

        pilt(int START_ADDRESS, List<jaotis_VALUE> 구역들) {
            this.START_ADDRESS = START_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ADDRESS() {
            return START_ADDRESS;
        }

        public List<jaotis_VALUE> 구역들() {
            return 구역들;
        }
    }

    public pilt 검사(byte[] andmed) {
        if (andmed == null || andmed.length < 52
                || andmed[0] != 0x7f || andmed[1] != 'E' || andmed[2] != 'L' || andmed[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (andmed[4] != 1 || andmed[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ADDRESS = sõeluma_täisarv(andmed, 24);
        int jaotis_tabel_ametikoht = sõeluma_täisarv(andmed, 32);
        int jaotis_kirje_suurust_muutma = 짧은정수읽기(andmed, 46);
        int jaotis_COUNT = 짧은정수읽기(andmed, 48);
        if (jaotis_kirje_suurust_muutma < 40 || jaotis_tabel_ametikoht < 0
                || (long) jaotis_tabel_ametikoht + (long) jaotis_kirje_suurust_muutma * jaotis_COUNT > andmed.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<jaotis_VALUE> 구역들 = new ArrayList<jaotis_VALUE>();
        for (int INDEX = 0; INDEX < jaotis_COUNT; INDEX++) {
            int Asukoht = jaotis_tabel_ametikoht + INDEX * jaotis_kirje_suurust_muutma;
            int 종류 = sõeluma_täisarv(andmed, Asukoht + 4);
            int lipp_VALUE = sõeluma_täisarv(andmed, Asukoht + 8);
            int ADDRESS = sõeluma_täisarv(andmed, Asukoht + 12);
            int Fail_ametikoht = sõeluma_täisarv(andmed, Asukoht + 16);
            int Suurus = sõeluma_täisarv(andmed, Asukoht + 20);
            if (Suurus < 0 || (종류 != 8 && ((long) Fail_ametikoht + Suurus > andmed.length || Fail_ametikoht < 0))) {
                throw new IllegalArgumentException("ELF jaotis_VALUE andmed 범위가 올바르지 않습니다.");
            }
            구역들.add(new jaotis_VALUE(종류, lipp_VALUE, ADDRESS, Fail_ametikoht, Suurus));
        }
        return new pilt(START_ADDRESS, 구역들);
    }

    private int sõeluma_täisarv(byte[] andmed, int Asukoht) {
        if (Asukoht < 0 || Asukoht > andmed.length - 4) {
            throw new IllegalArgumentException("ELF täisarv 범위를 벗어났습니다.");
        }
        return (andmed[Asukoht] & 0xff)
                | ((andmed[Asukoht + 1] & 0xff) << 8)
                | ((andmed[Asukoht + 2] & 0xff) << 16)
                | ((andmed[Asukoht + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] andmed, int Asukoht) {
        if (Asukoht < 0 || Asukoht > andmed.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 täisarv 범위를 벗어났습니다.");
        }
        return (andmed[Asukoht] & 0xff) | ((andmed[Asukoht + 1] & 0xff) << 8);
    }
}
