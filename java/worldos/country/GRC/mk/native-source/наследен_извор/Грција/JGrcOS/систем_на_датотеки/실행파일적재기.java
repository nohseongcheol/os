// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Грција.JGrcOS.систем_на_датотеки;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Изврши_наредба 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class секција_VALUE {
        private final int 종류;
        private final int знаменце_VALUE;
        private final int адреса;
        private final int датотека_позиционирање;
        private final int Големина;

        секција_VALUE(int 종류, int знаменце_VALUE, int адреса, int датотека_позиционирање, int Големина) {
            this.종류 = 종류;
            this.знаменце_VALUE = знаменце_VALUE;
            this.адреса = адреса;
            this.датотека_позиционирање = датотека_позиционирање;
            this.Големина = Големина;
        }

        public int 종류() {
            return 종류;
        }

        public int знаменце_VALUE() {
            return знаменце_VALUE;
        }

        public int адреса() {
            return адреса;
        }

        public int датотека_позиционирање() {
            return датотека_позиционирање;
        }

        public int Големина() {
            return Големина;
        }
    }

    public static final class IMAGE {
        private final int почетна_адреса;
        private final List<секција_VALUE> 구역들;

        IMAGE(int почетна_адреса, List<секција_VALUE> 구역들) {
            this.почетна_адреса = почетна_адреса;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int почетна_адреса() {
            return почетна_адреса;
        }

        public List<секција_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] податоци) {
        if (податоци == null || податоци.length < 52
                || податоци[0] != 0x7f || податоци[1] != 'E' || податоци[2] != 'L' || податоци[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (податоци[4] != 1 || податоци[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int почетна_адреса = разложи_цел_број(податоци, 24);
        int секција_табела_позиционирање = разложи_цел_број(податоци, 32);
        int секција_внес_големина = 짧은정수읽기(податоци, 46);
        int секција_COUNT = 짧은정수읽기(податоци, 48);
        if (секција_внес_големина < 40 || секција_табела_позиционирање < 0
                || (long) секција_табела_позиционирање + (long) секција_внес_големина * секција_COUNT > податоци.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<секција_VALUE> 구역들 = new ArrayList<секција_VALUE>();
        for (int INDEX = 0; INDEX < секција_COUNT; INDEX++) {
            int Позиција = секција_табела_позиционирање + INDEX * секција_внес_големина;
            int 종류 = разложи_цел_број(податоци, Позиција + 4);
            int знаменце_VALUE = разложи_цел_број(податоци, Позиција + 8);
            int адреса = разложи_цел_број(податоци, Позиција + 12);
            int датотека_позиционирање = разложи_цел_број(податоци, Позиција + 16);
            int Големина = разложи_цел_број(податоци, Позиција + 20);
            if (Големина < 0 || (종류 != 8 && ((long) датотека_позиционирање + Големина > податоци.length || датотека_позиционирање < 0))) {
                throw new IllegalArgumentException("ELF секција_VALUE податоци 범위가 올바르지 않습니다.");
            }
            구역들.add(new секција_VALUE(종류, знаменце_VALUE, адреса, датотека_позиционирање, Големина));
        }
        return new IMAGE(почетна_адреса, 구역들);
    }

    private int разложи_цел_број(byte[] податоци, int Позиција) {
        if (Позиција < 0 || Позиција > податоци.length - 4) {
            throw new IllegalArgumentException("ELF цел_број 범위를 벗어났습니다.");
        }
        return (податоци[Позиција] & 0xff)
                | ((податоци[Позиција + 1] & 0xff) << 8)
                | ((податоци[Позиција + 2] & 0xff) << 16)
                | ((податоци[Позиција + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] податоци, int Позиција) {
        if (Позиција < 0 || Позиција > податоци.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 цел_број 범위를 벗어났습니다.");
        }
        return (податоци[Позиција] & 0xff) | ((податоци[Позиција + 1] & 0xff) << 8);
    }
}
