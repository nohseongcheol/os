// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.작업;

import COL.JColOS.기억공간.쪽관리자;
import COL.JColOS.a_yatawaajiraaya_anaajaalaairua.파일서술자표;

public final class 과정 {
    private final int 식별자;
    private final int 부모식별자;
    private final 쪽관리자.ejepüsee_WAARAKATAJÜLÜ ejepüsee_WAARAKATAJÜLÜ;
    private final 파일서술자표 파일서술자;
    private 과정상태 jamakua_iparülein_ajutuu = 과정상태.준비;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    과정(int 식별자, int 부모식별자, 쪽관리자.ejepüsee_WAARAKATAJÜLÜ ejepüsee_WAARAKATAJÜLÜ, 파일서술자표 파일서술자) {
        this.식별자 = 식별자;
        this.부모식별자 = 부모식별자;
        this.ejepüsee_WAARAKATAJÜLÜ = ejepüsee_WAARAKATAJÜLÜ;
        this.파일서술자 = 파일서술자;
    }

    public int 식별자() {
        return 식별자;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public 쪽관리자.ejepüsee_WAARAKATAJÜLÜ ejepüsee_WAARAKATAJÜLÜ() {
        return ejepüsee_WAARAKATAJÜLÜ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public 과정상태 jamakua_iparülein_ajutuu() {
        return jamakua_iparülein_ajutuu;
    }

    public void 상태설정(과정상태 새상태) {
        jamakua_iparülein_ajutuu = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void aju_itaa_akumajiaa(int ajutuu) {
        종료값 = ajutuu & 0xff;
        jamakua_iparülein_ajutuu = 과정상태.aju_itaa_akumajiaa;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("akumajiaa_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int achuwalaa_ejepüsee, String[] 인자, String[] 환경) {
        실행시작주소 = achuwalaa_ejepüsee;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
