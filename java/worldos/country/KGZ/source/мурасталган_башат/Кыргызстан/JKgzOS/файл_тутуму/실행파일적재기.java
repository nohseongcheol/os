// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.файл_тутуму;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian аткаруу_буйрук 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class бөлүк_маани_366e0bfa {
        private final int 종류;
        private final int желек_маани;
        private final int дарек;
        private final int 파일위치;
        private final int Өлчөмү;

        бөлүк_маани_366e0bfa(int 종류, int желек_маани, int дарек, int 파일위치, int Өлчөмү) {
            this.종류 = 종류;
            this.желек_маани = желек_маани;
            this.дарек = дарек;
            this.파일위치 = 파일위치;
            this.Өлчөмү = Өлчөмү;
        }

        public int 종류() {
            return 종류;
        }

        public int желек_маани() {
            return желек_маани;
        }

        public int дарек() {
            return дарек;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Өлчөмү() {
            return Өлчөмү;
        }
    }

    public static final class сүрөт {
        private final int Баштоо_дарек;
        private final List<бөлүк_маани_366e0bfa> 구역들;

        сүрөт(int Баштоо_дарек, List<бөлүк_маани_366e0bfa> 구역들) {
            this.Баштоо_дарек = Баштоо_дарек;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Баштоо_дарек() {
            return Баштоо_дарек;
        }

        public List<бөлүк_маани_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public сүрөт 검사(byte[] берилмелер) {
        if (берилмелер == null || берилмелер.length < 52
                || берилмелер[0] != 0x7f || берилмелер[1] != 'E' || берилмелер[2] != 'L' || берилмелер[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (берилмелер[4] != 1 || берилмелер[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Баштоо_дарек = талдоо_бүтүн_сан(берилмелер, 24);
        int 구역표위치 = талдоо_бүтүн_сан(берилмелер, 32);
        int бөлүк_киргизме_жазуу_көлөм = 짧은정수읽기(берилмелер, 46);
        int 구역수 = 짧은정수읽기(берилмелер, 48);
        if (бөлүк_киргизме_жазуу_көлөм < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) бөлүк_киргизме_жазуу_көлөм * 구역수 > берилмелер.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<бөлүк_маани_366e0bfa> 구역들 = new ArrayList<бөлүк_маани_366e0bfa>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int Турган_жери = 구역표위치 + индекс * бөлүк_киргизме_жазуу_көлөм;
            int 종류 = талдоо_бүтүн_сан(берилмелер, Турган_жери + 4);
            int желек_маани = талдоо_бүтүн_сан(берилмелер, Турган_жери + 8);
            int дарек = талдоо_бүтүн_сан(берилмелер, Турган_жери + 12);
            int 파일위치 = талдоо_бүтүн_сан(берилмелер, Турган_жери + 16);
            int Өлчөмү = талдоо_бүтүн_сан(берилмелер, Турган_жери + 20);
            if (Өлчөмү < 0 || (종류 != 8 && ((long) 파일위치 + Өлчөмү > берилмелер.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF бөлүк_маани_366e0bfa берилмелер 범위가 올바르지 않습니다.");
            }
            구역들.add(new бөлүк_маани_366e0bfa(종류, желек_маани, дарек, 파일위치, Өлчөмү));
        }
        return new сүрөт(Баштоо_дарек, 구역들);
    }

    private int талдоо_бүтүн_сан(byte[] берилмелер, int Турган_жери) {
        if (Турган_жери < 0 || Турган_жери > берилмелер.length - 4) {
            throw new IllegalArgumentException("ELF бүтүн_сан 범위를 벗어났습니다.");
        }
        return (берилмелер[Турган_жери] & 0xff)
                | ((берилмелер[Турган_жери + 1] & 0xff) << 8)
                | ((берилмелер[Турган_жери + 2] & 0xff) << 16)
                | ((берилмелер[Турган_жери + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] берилмелер, int Турган_жери) {
        if (Турган_жери < 0 || Турган_жери > берилмелер.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 бүтүн_сан 범위를 벗어났습니다.");
        }
        return (берилмелер[Турган_жери] & 0xff) | ((берилмелер[Турган_жери + 1] & 0xff) << 8);
    }
}
