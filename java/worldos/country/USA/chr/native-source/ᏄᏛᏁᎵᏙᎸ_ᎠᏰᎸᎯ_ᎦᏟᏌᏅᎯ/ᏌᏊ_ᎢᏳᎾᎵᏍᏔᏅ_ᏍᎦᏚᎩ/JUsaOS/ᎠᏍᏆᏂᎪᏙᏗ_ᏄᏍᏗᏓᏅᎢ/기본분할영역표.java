// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ {
        private final int 종류;
        private final long ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ;
        private final long 구역수;

        ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ(int 종류, long ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ, long 구역수) {
            this.종류 = 종류;
            this.ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ = ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ() { return ᎭᏂᎩᏍᏓ_ᎤᏓᎯᏢᎢ; }
        public long 구역수() { return 구역수; }
    }

    public List<ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ> 결과 = new ArrayList<ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ>();
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 4; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            int 위치 = 446 + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long ᎠᎢᏎᏍᏗ = 작은순서정수(첫구역, 위치 + 8);
            long ᎢᎩᏓ = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && ᎢᎩᏓ != 0) {
                결과.add(new ᏓᏓᏓᎴᏛᎢ_ᏧᎬᏩᎶᏗᏯ(종류, ᎠᎢᏎᏍᏗ, ᎢᎩᏓ));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        return (ᎦᏟᏌᏅᎯ[위치] & 0xffL)
                | ((ᎦᏟᏌᏅᎯ[위치 + 1] & 0xffL) << 8)
                | ((ᎦᏟᏌᏅᎯ[위치 + 2] & 0xffL) << 16)
                | ((ᎦᏟᏌᏅᎯ[위치 + 3] & 0xffL) << 24);
    }
}

