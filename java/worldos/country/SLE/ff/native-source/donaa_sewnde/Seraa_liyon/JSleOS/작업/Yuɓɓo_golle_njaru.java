// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Seraa_liyon.JSleOS.작업;

import Seraa_liyon.JSleOS.기억공간.hello_kisnoowo;
import Seraa_liyon.JSleOS.yuɓɓo_piille.파일서술자표;

public final class Yuɓɓo_golle_njaru {
    private final int 식별자;
    private final int 부모식별자;
    private final hello_kisnoowo.ñiiɓirde_wonorde ñiiɓirde_wonorde;
    private final 파일서술자표 파일서술자;
    private Yuɓɓo_golle_ngonka ngonka_njaru = Yuɓɓo_golle_ngonka.Heblu;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Yuɓɓo_golle_njaru(int 식별자, int 부모식별자, hello_kisnoowo.ñiiɓirde_wonorde ñiiɓirde_wonorde, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.ñiiɓirde_wonorde = ñiiɓirde_wonorde;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public hello_kisnoowo.ñiiɓirde_wonorde ñiiɓirde_wonorde() {
        return ñiiɓirde_wonorde;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Yuɓɓo_golle_ngonka ngonka_njaru() {
        return ngonka_njaru;
    }

    public void 상태설정(Yuɓɓo_golle_ngonka 새상태) {
        ngonka_njaru = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void yaltude_tafirde(int njaru) {
        종료값 = njaru & 0xff;
        ngonka_njaru = Yuɓɓo_golle_ngonka.yaltude_tafirde;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("tafirde_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int huɓɓude_ñiiɓirde, String[] 인자, String[] 환경) {
        실행시작주소 = huɓɓude_ñiiɓirde;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
