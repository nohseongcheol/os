// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iLesotho.JLsoOS.작업;

import iLesotho.JLsoOS.기억공간.ikhasi_imeneja;
import iLesotho.JLsoOS.isistimu_yefayela.파일서술자표;

public final class Inqubo_inani {
    private final int isivezi_inani;
    private final int 부모식별자;
    private final ikhasi_imeneja.ikheli_indawo ikheli_indawo;
    private final 파일서술자표 파일서술자;
    private Inqubo_isimo isimo_inani = Inqubo_isimo.Hlela;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Inqubo_inani(int isivezi_inani, int 부모식별자, ikhasi_imeneja.ikheli_indawo ikheli_indawo, 파일서술자표 파일서술자) {
        this.isivezi_inani = isivezi_inani;
        this.부모식별자 = 부모식별자;
        this.ikheli_indawo = ikheli_indawo;
        this.파일서술자 = 파일서술자;
    }

    public int isivezi_inani() {
        return isivezi_inani;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ikhasi_imeneja.ikheli_indawo ikheli_indawo() {
        return ikheli_indawo;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Inqubo_isimo isimo_inani() {
        return isimo_inani;
    }

    public void isethi_isimo(Inqubo_isimo 새상태) {
        isimo_inani = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void phuma_i_app(int inani) {
        종료값 = inani & 0xff;
        isimo_inani = Inqubo_isimo.phuma_i_app;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("i_app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int qala_ikheli, String[] 인자, String[] 환경) {
        실행시작주소 = qala_ikheli;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
