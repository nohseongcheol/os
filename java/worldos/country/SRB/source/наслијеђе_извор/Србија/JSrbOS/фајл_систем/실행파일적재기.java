// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.фајл_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Изврши_команда 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class одељак_вриједност {
        private final int 종류;
        private final int заставица_вриједност;
        private final int адреса;
        private final int фајл_позиција;
        private final int Величина;

        одељак_вриједност(int 종류, int заставица_вриједност, int адреса, int фајл_позиција, int Величина) {
            this.종류 = 종류;
            this.заставица_вриједност = заставица_вриједност;
            this.адреса = адреса;
            this.фајл_позиција = фајл_позиција;
            this.Величина = Величина;
        }

        public int 종류() {
            return 종류;
        }

        public int заставица_вриједност() {
            return заставица_вриједност;
        }

        public int адреса() {
            return адреса;
        }

        public int фајл_позиција() {
            return фајл_позиција;
        }

        public int Величина() {
            return Величина;
        }
    }

    public static final class слика {
        private final int почетна_адреса;
        private final List<одељак_вриједност> 구역들;

        слика(int почетна_адреса, List<одељак_вриједност> 구역들) {
            this.почетна_адреса = почетна_адреса;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int почетна_адреса() {
            return почетна_адреса;
        }

        public List<одељак_вриједност> 구역들() {
            return 구역들;
        }
    }

    public слика 검사(byte[] подаци) {
        if (подаци == null || подаци.length < 52
                || подаци[0] != 0x7f || подаци[1] != 'E' || подаци[2] != 'L' || подаци[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (подаци[4] != 1 || подаци[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int почетна_адреса = рашчланити_цијели_број(подаци, 24);
        int одељак_табела_позиција = рашчланити_цијели_број(подаци, 32);
        int одељак_унос_подесити_величину = 짧은정수읽기(подаци, 46);
        int 구역수 = 짧은정수읽기(подаци, 48);
        if (одељак_унос_подесити_величину < 40 || одељак_табела_позиција < 0
                || (long) одељак_табела_позиција + (long) одељак_унос_подесити_величину * 구역수 > подаци.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<одељак_вриједност> 구역들 = new ArrayList<одељак_вриједност>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int Положај = одељак_табела_позиција + индекс * одељак_унос_подесити_величину;
            int 종류 = рашчланити_цијели_број(подаци, Положај + 4);
            int заставица_вриједност = рашчланити_цијели_број(подаци, Положај + 8);
            int адреса = рашчланити_цијели_број(подаци, Положај + 12);
            int фајл_позиција = рашчланити_цијели_број(подаци, Положај + 16);
            int Величина = рашчланити_цијели_број(подаци, Положај + 20);
            if (Величина < 0 || (종류 != 8 && ((long) фајл_позиција + Величина > подаци.length || фајл_позиција < 0))) {
                throw new IllegalArgumentException("ELF одељак_вриједност подаци 범위가 올바르지 않습니다.");
            }
            구역들.add(new одељак_вриједност(종류, заставица_вриједност, адреса, фајл_позиција, Величина));
        }
        return new слика(почетна_адреса, 구역들);
    }

    private int рашчланити_цијели_број(byte[] подаци, int Положај) {
        if (Положај < 0 || Положај > подаци.length - 4) {
            throw new IllegalArgumentException("ELF цијели_број 범위를 벗어났습니다.");
        }
        return (подаци[Положај] & 0xff)
                | ((подаци[Положај + 1] & 0xff) << 8)
                | ((подаци[Положај + 2] & 0xff) << 16)
                | ((подаци[Положај + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] подаци, int Положај) {
        if (Положај < 0 || Положај > подаци.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 цијели_број 범위를 벗어났습니다.");
        }
        return (подаци[Положај] & 0xff) | ((подаци[Положај + 1] & 0xff) << 8);
    }
}
