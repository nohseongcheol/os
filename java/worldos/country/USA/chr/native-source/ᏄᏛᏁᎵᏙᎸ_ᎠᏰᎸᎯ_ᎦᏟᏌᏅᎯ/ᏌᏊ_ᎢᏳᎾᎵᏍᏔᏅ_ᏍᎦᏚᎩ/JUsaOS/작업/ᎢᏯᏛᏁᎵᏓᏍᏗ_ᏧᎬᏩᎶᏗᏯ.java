// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.작업;

import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.기억공간.ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ;
import ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.파일서술자표;

public final class ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ {
    private final int ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ;
    private final int 부모식별자;
    private final ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE;
    private final 파일서술자표 파일서술자;
    private ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏄᏍᏗᏓᏅ ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏄᏍᏗᏓᏅ.ᎭᏛᏅᎢᏍᏓ;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ(int ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ, int 부모식별자, ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE, 파일서술자표 파일서술자) {
        this.ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ;
        this.부모식별자 = 부모식별자;
        this.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE = ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE;
        this.파일서술자 = 파일서술자;
    }

    public int ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ() {
        return ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ᎤᎦᏅᏓᏛᎢ_ᏗᎫᎪᏔᏂᏙᎯ.ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE() {
        return ᎪᏪᎵ_ᏫᏗᎦᏅᏗ_SPACE;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏄᏍᏗᏓᏅ ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ() {
        return ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ;
    }

    public void ᎦᎪᏗ_ᏄᏍᏗᏓᏅ(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏄᏍᏗᏓᏅ 새상태) {
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ(int ᏧᎬᏩᎶᏗᏯ) {
        종료값 = ᏧᎬᏩᎶᏗᏯ & 0xff;
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏄᏍᏗᏓᏅ.ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ᎬᏙᏗ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, String[] 인자, String[] 환경) {
        실행시작주소 = ᎭᏂᎩᏍᏓ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
