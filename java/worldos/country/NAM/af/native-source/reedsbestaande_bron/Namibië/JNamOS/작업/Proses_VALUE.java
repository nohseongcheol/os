// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibië.JNamOS.작업;

import Namibië.JNamOS.기억공간.bladsy_bestuurder;
import Namibië.JNamOS.lêerstelsel.파일서술자표;

public final class Proses_VALUE {
    private final int waarde_VALUE;
    private final int 부모식별자;
    private final bladsy_bestuurder.adres_ruimte adres_ruimte;
    private final 파일서술자표 파일서술자;
    private Proses_stand stand_VALUE = Proses_stand.Maak_gereed;
    private int Verlaat_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proses_VALUE(int waarde_VALUE, int 부모식별자, bladsy_bestuurder.adres_ruimte adres_ruimte, 파일서술자표 파일서술자) {
        this.waarde_VALUE = waarde_VALUE;
        this.부모식별자 = 부모식별자;
        this.adres_ruimte = adres_ruimte;
        this.파일서술자 = 파일서술자;
    }

    public int waarde_VALUE() {
        return waarde_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public bladsy_bestuurder.adres_ruimte adres_ruimte() {
        return adres_ruimte;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proses_stand stand_VALUE() {
        return stand_VALUE;
    }

    public void stel_stand(Proses_stand 새상태) {
        stand_VALUE = 새상태;
    }

    public int Verlaat_CODE() {
        return Verlaat_CODE;
    }

    public void Verlaat_program(int VALUE) {
        Verlaat_CODE = VALUE & 0xff;
        stand_VALUE = Proses_stand.Verlaat_program;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int BEGIN_adres, String[] 인자, String[] 환경) {
        실행시작주소 = BEGIN_adres;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
