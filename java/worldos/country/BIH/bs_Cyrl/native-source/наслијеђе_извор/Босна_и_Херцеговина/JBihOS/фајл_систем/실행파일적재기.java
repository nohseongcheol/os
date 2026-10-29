// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.фајл_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class секција_вриједност {
        private final int 종류;
        private final int заставица_вриједност;
        private final int адреса;
        private final int 파일위치;
        private final int подесити_величину;

        секција_вриједност(int 종류, int заставица_вриједност, int адреса, int 파일위치, int подесити_величину) {
            this.종류 = 종류;
            this.заставица_вриједност = заставица_вриједност;
            this.адреса = адреса;
            this.파일위치 = 파일위치;
            this.подесити_величину = подесити_величину;
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

        public int 파일위치() {
            return 파일위치;
        }

        public int подесити_величину() {
            return подесити_величину;
        }
    }

    public static final class слика {
        private final int почети_адреса;
        private final List<секција_вриједност> 구역들;

        слика(int почети_адреса, List<секција_вриједност> 구역들) {
            this.почети_адреса = почети_адреса;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int почети_адреса() {
            return почети_адреса;
        }

        public List<секција_вриједност> 구역들() {
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
        int почети_адреса = рашчлањивати_цијели_број(подаци, 24);
        int 구역표위치 = рашчлањивати_цијели_број(подаци, 32);
        int секција_унос_подесити_величину = 짧은정수읽기(подаци, 46);
        int 구역수 = 짧은정수읽기(подаци, 48);
        if (секција_унос_подесити_величину < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) секција_унос_подесити_величину * 구역수 > подаци.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<секција_вриједност> 구역들 = new ArrayList<секција_вриједност>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int 위치 = 구역표위치 + индекс * секција_унос_подесити_величину;
            int 종류 = рашчлањивати_цијели_број(подаци, 위치 + 4);
            int заставица_вриједност = рашчлањивати_цијели_број(подаци, 위치 + 8);
            int адреса = рашчлањивати_цијели_број(подаци, 위치 + 12);
            int 파일위치 = рашчлањивати_цијели_број(подаци, 위치 + 16);
            int подесити_величину = рашчлањивати_цијели_број(подаци, 위치 + 20);
            if (подесити_величину < 0 || (종류 != 8 && ((long) 파일위치 + подесити_величину > подаци.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF секција_вриједност подаци 범위가 올바르지 않습니다.");
            }
            구역들.add(new секција_вриједност(종류, заставица_вриједност, адреса, 파일위치, подесити_величину));
        }
        return new слика(почети_адреса, 구역들);
    }

    private int рашчлањивати_цијели_број(byte[] подаци, int 위치) {
        if (위치 < 0 || 위치 > подаци.length - 4) {
            throw new IllegalArgumentException("ELF цијели_број 범위를 벗어났습니다.");
        }
        return (подаци[위치] & 0xff)
                | ((подаци[위치 + 1] & 0xff) << 8)
                | ((подаци[위치 + 2] & 0xff) << 16)
                | ((подаци[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] подаци, int 위치) {
        if (위치 < 0 || 위치 > подаци.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 цијели_број 범위를 벗어났습니다.");
        }
        return (подаци[위치] & 0xff) | ((подаци[위치 + 1] & 0xff) << 8);
    }
}
