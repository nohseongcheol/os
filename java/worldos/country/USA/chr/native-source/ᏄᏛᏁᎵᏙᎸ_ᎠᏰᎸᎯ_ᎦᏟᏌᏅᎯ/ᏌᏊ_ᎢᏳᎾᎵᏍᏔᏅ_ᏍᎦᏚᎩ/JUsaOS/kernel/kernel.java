// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.kernel;

import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.기억공간.ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.기억공간.ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.입력.입력관리자;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.작업.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.작업.배정기;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.체계호출.체계호출;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.파일서술자표;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ;
    private final ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ 기억공간 = new ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ(32 * 1024 * 1024);
    private final ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ 쪽관리 = new ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ();
    private final ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ = new ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ 첫과정;
    private final 체계호출 체계호출;

    public kernel(하드웨어 ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ) {
        this.ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ = ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ;
        첫과정 = 배정기.첫과정(new 파일서술자표(ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ));
        체계호출 = new 체계호출(ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ, 쪽관리, 배정기, ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ, 입력관리);
    }

    public void ᎠᎢᏎᏍᏗ() {
        ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.직렬출력("=== JUsaOS 관리 kernel_ᏧᎬᏩᎶᏗᏯ ===\n");
    }

    public void 한단계실행() {
        ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.중앙처리장치멈춤();
    }

    public ᎠᏅᏓᏗᏍᏙ_ᏗᎫᎪᏔᏂᏙᎯ 기억공간() {
        return 기억공간;
    }

    public ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ 쪽관리() {
        return 쪽관리;
    }

    public ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ() {
        return ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
