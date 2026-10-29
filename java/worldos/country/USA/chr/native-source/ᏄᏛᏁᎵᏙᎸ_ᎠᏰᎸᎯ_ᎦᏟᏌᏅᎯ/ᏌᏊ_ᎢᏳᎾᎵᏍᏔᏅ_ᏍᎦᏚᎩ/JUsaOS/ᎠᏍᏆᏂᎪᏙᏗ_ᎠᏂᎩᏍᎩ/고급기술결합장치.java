// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏂᎩᏍᎩ;

import java.util.Arrays;

/** ATA 28비트 ᎤᏁᏤᎸᎩ 계층과 같은 512바이트 논리 ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ 장치다. */
public final class 고급기술결합장치 {
    public static final int ᎤᏓᎯᏢᎢ_ᎢᎩᏓ = 512;
    private final byte[] ᎦᏟᏌᏅᎯ;
    private final boolean ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ;

    public 고급기술결합장치(int 구역수, boolean ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ 수가 올바르지 않습니다.");
        }
        ᎦᏟᏌᏅᎯ = new byte[Math.multiplyExact(구역수, ᎤᏓᎯᏢᎢ_ᎢᎩᏓ)];
        this.ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ = ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ;
    }

    public int 구역수() {
        return ᎦᏟᏌᏅᎯ.length / ᎤᏓᎯᏢᎢ_ᎢᎩᏓ;
    }

    public void 읽기(int ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, byte[] 받을곳) {
        범위확인(ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 받을곳);
        System.arraycopy(ᎦᏟᏌᏅᎯ, ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * ᎤᏓᎯᏢᎢ_ᎢᎩᏓ, 받을곳, 0, ᎤᏓᎯᏢᎢ_ᎢᎩᏓ);
    }

    public void ᎪᏪᎶᏗ(int ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, byte[] 쓸자료) {
        if (ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 쓸자료);
        System.arraycopy(쓸자료, 0, ᎦᏟᏌᏅᎯ, ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * ᎤᏓᎯᏢᎢ_ᎢᎩᏓ, ᎤᏓᎯᏢᎢ_ᎢᎩᏓ);
    }

    public void 지우기() {
        if (ᎠᎪᎵᏰᏗᏊ_ᎢᎦᎢ_ᏧᎬᏩᎶᏗᏯ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(ᎦᏟᏌᏅᎯ, (byte) 0);
    }

    private void 범위확인(int ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, byte[] 임시공간) {
        if (ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 0 || ᎤᏓᎯᏢᎢ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ >= 구역수() || 임시공간.length < ᎤᏓᎯᏢᎢ_ᎢᎩᏓ) {
            throw new IllegalArgumentException("ATA ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ 범위가 올바르지 않습니다.");
        }
    }
}

