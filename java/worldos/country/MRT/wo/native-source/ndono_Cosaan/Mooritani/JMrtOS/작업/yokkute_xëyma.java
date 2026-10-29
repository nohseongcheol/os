// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.작업;

import Mooritani.JMrtOS.기억공간.xët_doxalkat;
import Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal.파일서술자표;

public final class yokkute_xëyma {
    private final int raññeekaay_xëyma;
    private final int 부모식별자;
    private final xët_doxalkat.dëkkuwaay_Espace dëkkuwaay_Espace;
    private final 파일서술자표 파일서술자;
    private yokkute_nekkin nekkin_xëyma = yokkute_nekkin.jël_matuwaay;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    yokkute_xëyma(int raññeekaay_xëyma, int 부모식별자, xët_doxalkat.dëkkuwaay_Espace dëkkuwaay_Espace, 파일서술자표 파일서술자) {
        this.raññeekaay_xëyma = raññeekaay_xëyma;
        this.부모식별자 = 부모식별자;
        this.dëkkuwaay_Espace = dëkkuwaay_Espace;
        this.파일서술자 = 파일서술자;
    }

    public int raññeekaay_xëyma() {
        return raññeekaay_xëyma;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public xët_doxalkat.dëkkuwaay_Espace dëkkuwaay_Espace() {
        return dëkkuwaay_Espace;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public yokkute_nekkin nekkin_xëyma() {
        return nekkin_xëyma;
    }

    public void Boole_gi_nekkin(yokkute_nekkin 새상태) {
        nekkin_xëyma = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void Génn_jëfekaay(int xëyma) {
        종료값 = xëyma & 0xff;
        nekkin_xëyma = yokkute_nekkin.Génn_jëfekaay;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("jëfekaay_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Door_dëkkuwaay, String[] 인자, String[] 환경) {
        실행시작주소 = Door_dëkkuwaay;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
