// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.작업;

import ᑲᓇᑕᒥ.JCanOS.기억공간.mappigaq_aulattiji;
import ᑲᓇᑕᒥ.JCanOS.inikkuvik.파일서술자표;

public final class Pivallianiq_atuutilik {
    private final int 식별자;
    private final int 부모식별자;
    private final mappigaq_aulattiji.turaarut_SPACEBAR turaarut_SPACEBAR;
    private final 파일서술자표 파일서술자;
    private Pivallianiq_qanuilinganiq qanuilinganiq_atuutilik = Pivallianiq_qanuilinganiq.Parnalli;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Pivallianiq_atuutilik(int 식별자, int 부모식별자, mappigaq_aulattiji.turaarut_SPACEBAR turaarut_SPACEBAR, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.turaarut_SPACEBAR = turaarut_SPACEBAR;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public mappigaq_aulattiji.turaarut_SPACEBAR turaarut_SPACEBAR() {
        return turaarut_SPACEBAR;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Pivallianiq_qanuilinganiq qanuilinganiq_atuutilik() {
        return qanuilinganiq_atuutilik;
    }

    public void attiqsimaniit_qanuilinganiq(Pivallianiq_qanuilinganiq 새상태) {
        qanuilinganiq_atuutilik = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void taima_pilirijjut(int atuutilik) {
        종료값 = atuutilik & 0xff;
        qanuilinganiq_atuutilik = Pivallianiq_qanuilinganiq.taima_pilirijjut;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("pilirijjut_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int pigiarli_turaarut, String[] 인자, String[] 환경) {
        실행시작주소 = pigiarli_turaarut;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
