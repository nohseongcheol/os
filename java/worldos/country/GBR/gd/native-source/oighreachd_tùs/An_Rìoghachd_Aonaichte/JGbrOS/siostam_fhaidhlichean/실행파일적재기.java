// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian gnìomhaich_àithne 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class earrann_VALUE {
        private final int 종류;
        private final int bratach_VALUE;
        private final int ADDRESS;
        private final int faidhle_suidhich;
        private final int atharraich_am_meud;

        earrann_VALUE(int 종류, int bratach_VALUE, int ADDRESS, int faidhle_suidhich, int atharraich_am_meud) {
            this.종류 = 종류;
            this.bratach_VALUE = bratach_VALUE;
            this.ADDRESS = ADDRESS;
            this.faidhle_suidhich = faidhle_suidhich;
            this.atharraich_am_meud = atharraich_am_meud;
        }

        public int 종류() {
            return 종류;
        }

        public int bratach_VALUE() {
            return bratach_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int faidhle_suidhich() {
            return faidhle_suidhich;
        }

        public int atharraich_am_meud() {
            return atharraich_am_meud;
        }
    }

    public static final class IMAGE {
        private final int Start_ADDRESS;
        private final List<earrann_VALUE> 구역들;

        IMAGE(int Start_ADDRESS, List<earrann_VALUE> 구역들) {
            this.Start_ADDRESS = Start_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_ADDRESS() {
            return Start_ADDRESS;
        }

        public List<earrann_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] dàta) {
        if (dàta == null || dàta.length < 52
                || dàta[0] != 0x7f || dàta[1] != 'E' || dàta[2] != 'L' || dàta[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dàta[4] != 1 || dàta[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_ADDRESS = 정수읽기(dàta, 24);
        int earrann_clàr_suidhich = 정수읽기(dàta, 32);
        int earrann_cur_a_steach_atharraich_am_meud = 짧은정수읽기(dàta, 46);
        int earrann_COUNT = 짧은정수읽기(dàta, 48);
        if (earrann_cur_a_steach_atharraich_am_meud < 40 || earrann_clàr_suidhich < 0
                || (long) earrann_clàr_suidhich + (long) earrann_cur_a_steach_atharraich_am_meud * earrann_COUNT > dàta.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<earrann_VALUE> 구역들 = new ArrayList<earrann_VALUE>();
        for (int INDEX = 0; INDEX < earrann_COUNT; INDEX++) {
            int suidhich = earrann_clàr_suidhich + INDEX * earrann_cur_a_steach_atharraich_am_meud;
            int 종류 = 정수읽기(dàta, suidhich + 4);
            int bratach_VALUE = 정수읽기(dàta, suidhich + 8);
            int ADDRESS = 정수읽기(dàta, suidhich + 12);
            int faidhle_suidhich = 정수읽기(dàta, suidhich + 16);
            int atharraich_am_meud = 정수읽기(dàta, suidhich + 20);
            if (atharraich_am_meud < 0 || (종류 != 8 && ((long) faidhle_suidhich + atharraich_am_meud > dàta.length || faidhle_suidhich < 0))) {
                throw new IllegalArgumentException("ELF earrann_VALUE dàta 범위가 올바르지 않습니다.");
            }
            구역들.add(new earrann_VALUE(종류, bratach_VALUE, ADDRESS, faidhle_suidhich, atharraich_am_meud));
        }
        return new IMAGE(Start_ADDRESS, 구역들);
    }

    private int 정수읽기(byte[] dàta, int suidhich) {
        if (suidhich < 0 || suidhich > dàta.length - 4) {
            throw new IllegalArgumentException("ELF àireamh_shlàn 범위를 벗어났습니다.");
        }
        return (dàta[suidhich] & 0xff)
                | ((dàta[suidhich + 1] & 0xff) << 8)
                | ((dàta[suidhich + 2] & 0xff) << 16)
                | ((dàta[suidhich + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dàta, int suidhich) {
        if (suidhich < 0 || suidhich > dàta.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 àireamh_shlàn 범위를 벗어났습니다.");
        }
        return (dàta[suidhich] & 0xff) | ((dàta[suidhich + 1] & 0xff) << 8);
    }
}
