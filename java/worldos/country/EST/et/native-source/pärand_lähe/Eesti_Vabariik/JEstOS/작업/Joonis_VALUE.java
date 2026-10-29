// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.작업;

import Eesti_Vabariik.JEstOS.Mälu_regioon.쪽관리자;
import Eesti_Vabariik.JEstOS.failisüsteem.파일서술자표;

public final class Joonis_VALUE {
    private final int identifikaator_VALUE;
    private final int ema_identifikaator;
    private final 쪽관리자.ADDRESS_ruum ADDRESS_ruum;
    private final 파일서술자표 파일서술자;
    private Joonis_Olek Olek_VALUE = Joonis_Olek.Ettevalmistamine;
    private int Välju_CODE;
    private int programm_vaheaeg = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Joonis_VALUE(int identifikaator_VALUE, int ema_identifikaator, 쪽관리자.ADDRESS_ruum ADDRESS_ruum, 파일서술자표 파일서술자) {
        this.identifikaator_VALUE = identifikaator_VALUE;
        this.ema_identifikaator = ema_identifikaator;
        this.ADDRESS_ruum = ADDRESS_ruum;
        this.파일서술자 = 파일서술자;
    }

    public int identifikaator_VALUE() {
        return identifikaator_VALUE;
    }

    public int ema_identifikaator() {
        return ema_identifikaator;
    }

    public 쪽관리자.ADDRESS_ruum ADDRESS_ruum() {
        return ADDRESS_ruum;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Joonis_Olek Olek_VALUE() {
        return Olek_VALUE;
    }

    public void hulk_Olek(Joonis_Olek 새상태) {
        Olek_VALUE = 새상태;
    }

    public int Välju_CODE() {
        return Välju_CODE;
    }

    public void Välju_programm(int VALUE) {
        Välju_CODE = VALUE & 0xff;
        Olek_VALUE = Joonis_Olek.Välju_programm;
    }

    public int programm_vaheaeg() {
        return programm_vaheaeg;
    }

    public void hulk_programm_vaheaeg(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programm_f5044b9b 끝 범위를 벗어났습니다.");
        }
        programm_vaheaeg = 새끝;
    }

    public void 실행문맥설정(int START_ADDRESS, String[] parameeter_argument, String[] 환경) {
        실행시작주소 = START_ADDRESS;
        실행인자 = parameeter_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
