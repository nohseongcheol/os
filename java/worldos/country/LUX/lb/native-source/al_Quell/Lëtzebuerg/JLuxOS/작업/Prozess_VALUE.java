// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.작업;

import Lëtzebuerg.JLuxOS.기억공간.Säit_Manager;
import Lëtzebuerg.JLuxOS.Fichierssystem.파일서술자표;

public final class Prozess_VALUE {
    private final int Identifikateur_VALUE;
    private final int 부모식별자;
    private final Säit_Manager.Adress_Plaz Adress_Plaz;
    private final 파일서술자표 파일서술자;
    private Prozess_Status Status_VALUE = Prozess_Status.Préparéieren;
    private int Schluss_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Prozess_VALUE(int Identifikateur_VALUE, int 부모식별자, Säit_Manager.Adress_Plaz Adress_Plaz, 파일서술자표 파일서술자) {
        this.Identifikateur_VALUE = Identifikateur_VALUE;
        this.부모식별자 = 부모식별자;
        this.Adress_Plaz = Adress_Plaz;
        this.파일서술자 = 파일서술자;
    }

    public int Identifikateur_VALUE() {
        return Identifikateur_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public Säit_Manager.Adress_Plaz Adress_Plaz() {
        return Adress_Plaz;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Prozess_Status Status_VALUE() {
        return Status_VALUE;
    }

    public void Saz_Status(Prozess_Status 새상태) {
        Status_VALUE = 새상태;
    }

    public int Schluss_CODE() {
        return Schluss_CODE;
    }

    public void Schluss_App(int VALUE) {
        Schluss_CODE = VALUE & 0xff;
        Status_VALUE = Prozess_Status.Schluss_App;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("App_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_Adress, String[] 인자, String[] 환경) {
        실행시작주소 = Start_Adress;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
