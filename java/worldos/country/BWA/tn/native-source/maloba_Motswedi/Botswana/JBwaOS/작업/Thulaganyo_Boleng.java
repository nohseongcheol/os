// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.작업;

import Botswana.JBwaOS.기억공간.tsebe_motsamaisi;
import Botswana.JBwaOS.setsamaisadifaele.파일서술자표;

public final class Thulaganyo_Boleng {
    private final int setlhaodi_Boleng;
    private final int 부모식별자;
    private final tsebe_motsamaisi.aterese_sebaka aterese_sebaka;
    private final 파일서술자표 파일서술자;
    private Thulaganyo_kemo kemo_Boleng = Thulaganyo_kemo.Baakanya;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Thulaganyo_Boleng(int setlhaodi_Boleng, int 부모식별자, tsebe_motsamaisi.aterese_sebaka aterese_sebaka, 파일서술자표 파일서술자) {
        this.setlhaodi_Boleng = setlhaodi_Boleng;
        this.부모식별자 = 부모식별자;
        this.aterese_sebaka = aterese_sebaka;
        this.파일서술자 = 파일서술자;
    }

    public int setlhaodi_Boleng() {
        return setlhaodi_Boleng;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public tsebe_motsamaisi.aterese_sebaka aterese_sebaka() {
        return aterese_sebaka;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Thulaganyo_kemo kemo_Boleng() {
        return kemo_Boleng;
    }

    public void sete_kemo(Thulaganyo_kemo 새상태) {
        kemo_Boleng = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void tswaya_Tiriso(int Boleng) {
        종료값 = Boleng & 0xff;
        kemo_Boleng = Thulaganyo_kemo.tswaya_Tiriso;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("Tiriso_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int simolola_aterese, String[] 인자, String[] 환경) {
        실행시작주소 = simolola_aterese;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
