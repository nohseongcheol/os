// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ {
        private final int 종류;
        private final int ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ;
        private final int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        private final int 파일위치;
        private final int ᎢᎩᏓ;

        ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ(int 종류, int ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ, int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, int 파일위치, int ᎢᎩᏓ) {
            this.종류 = 종류;
            this.ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ = ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ;
            this.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
            this.파일위치 = 파일위치;
            this.ᎢᎩᏓ = ᎢᎩᏓ;
        }

        public int 종류() {
            return 종류;
        }

        public int ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ() {
            return ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ;
        }

        public int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ() {
            return ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int ᎢᎩᏓ() {
            return ᎢᎩᏓ;
        }
    }

    public static final class ᎤᏓᏴᎳᏛ {
        private final int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        private final List<ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ> 구역들;

        ᎤᏓᏴᎳᏛ(int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, List<ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ> 구역들) {
            this.ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ() {
            return ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        }

        public List<ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ> 구역들() {
            return 구역들;
        }
    }

    public ᎤᏓᏴᎳᏛ 검사(byte[] ᎦᏟᏌᏅᎯ) {
        if (ᎦᏟᏌᏅᎯ == null || ᎦᏟᏌᏅᎯ.length < 52
                || ᎦᏟᏌᏅᎯ[0] != 0x7f || ᎦᏟᏌᏅᎯ[1] != 'E' || ᎦᏟᏌᏅᎯ[2] != 'L' || ᎦᏟᏌᏅᎯ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ᎦᏟᏌᏅᎯ[4] != 1 || ᎦᏟᏌᏅᎯ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = 정수읽기(ᎦᏟᏌᏅᎯ, 24);
        int 구역표위치 = 정수읽기(ᎦᏟᏌᏅᎯ, 32);
        int ᎤᏓᎯᏢᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎢᎩᏓ = 짧은정수읽기(ᎦᏟᏌᏅᎯ, 46);
        int 구역수 = 짧은정수읽기(ᎦᏟᏌᏅᎯ, 48);
        if (ᎤᏓᎯᏢᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎢᎩᏓ < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) ᎤᏓᎯᏢᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎢᎩᏓ * 구역수 > ᎦᏟᏌᏅᎯ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ> 구역들 = new ArrayList<ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ>();
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 구역수; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            int 위치 = 구역표위치 + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * ᎤᏓᎯᏢᎢ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎢᎩᏓ;
            int 종류 = 정수읽기(ᎦᏟᏌᏅᎯ, 위치 + 4);
            int ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ = 정수읽기(ᎦᏟᏌᏅᎯ, 위치 + 8);
            int ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = 정수읽기(ᎦᏟᏌᏅᎯ, 위치 + 12);
            int 파일위치 = 정수읽기(ᎦᏟᏌᏅᎯ, 위치 + 16);
            int ᎢᎩᏓ = 정수읽기(ᎦᏟᏌᏅᎯ, 위치 + 20);
            if (ᎢᎩᏓ < 0 || (종류 != 8 && ((long) 파일위치 + ᎢᎩᏓ > ᎦᏟᏌᏅᎯ.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ ᎦᏟᏌᏅᎯ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ(종류, ᎯᏓᏛᎥᎦ_ᏧᎬᏩᎶᏗᏯ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 파일위치, ᎢᎩᏓ));
        }
        return new ᎤᏓᏴᎳᏛ(ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 구역들);
    }

    private int 정수읽기(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        if (위치 < 0 || 위치 > ᎦᏟᏌᏅᎯ.length - 4) {
            throw new IllegalArgumentException("ELF integer 범위를 벗어났습니다.");
        }
        return (ᎦᏟᏌᏅᎯ[위치] & 0xff)
                | ((ᎦᏟᏌᏅᎯ[위치 + 1] & 0xff) << 8)
                | ((ᎦᏟᏌᏅᎯ[위치 + 2] & 0xff) << 16)
                | ((ᎦᏟᏌᏅᎯ[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        if (위치 < 0 || 위치 > ᎦᏟᏌᏅᎯ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 integer 범위를 벗어났습니다.");
        }
        return (ᎦᏟᏌᏅᎯ[위치] & 0xff) | ((ᎦᏟᏌᏅᎯ[위치 + 1] & 0xff) << 8);
    }
}
