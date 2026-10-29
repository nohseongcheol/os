// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.작업;

import Noreg.JNorOS.기억공간.side_leiar;
import Noreg.JNorOS.filsystem.파일서술자표;

public final class Prosess_VALUE {
    private final int identifikator_VALUE;
    private final int forelder_identifikator;
    private final side_leiar.ADDRESS_område ADDRESS_område;
    private final 파일서술자표 파일서술자;
    private Prosess_status status_VALUE = Prosess_status.Klargjer;
    private int Utgang_CODE;
    private int app_pause = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Prosess_VALUE(int identifikator_VALUE, int forelder_identifikator, side_leiar.ADDRESS_område ADDRESS_område, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.forelder_identifikator = forelder_identifikator;
        this.ADDRESS_område = ADDRESS_område;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int forelder_identifikator() {
        return forelder_identifikator;
    }

    public side_leiar.ADDRESS_område ADDRESS_område() {
        return ADDRESS_område;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Prosess_status status_VALUE() {
        return status_VALUE;
    }

    public void sett_status(Prosess_status 새상태) {
        status_VALUE = 새상태;
    }

    public int Utgang_CODE() {
        return Utgang_CODE;
    }

    public void Utgang_app(int VALUE) {
        Utgang_CODE = VALUE & 0xff;
        status_VALUE = Prosess_status.Utgang_app;
    }

    public int app_pause() {
        return app_pause;
    }

    public void sett_app_pause(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_pause = 새끝;
    }

    public void 실행문맥설정(int START_ADDRESS, String[] parameter_argument, String[] 환경) {
        실행시작주소 = START_ADDRESS;
        실행인자 = parameter_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
