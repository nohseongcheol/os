// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.작업;

import Bosna_i_Hercegovina.JBihOS.기억공간.stranica_menadžer;
import Bosna_i_Hercegovina.JBihOS.fajl_sistem.파일서술자표;

public final class proces_VALUE {
    private final int identifikator_VALUE;
    private final int roditelj_identifikator;
    private final stranica_menadžer.adresa_prostor adresa_prostor;
    private final 파일서술자표 파일서술자;
    private proces_stanje stanje_VALUE = proces_stanje.Pripremiti;
    private int izaći_kod;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] operativno_okruženje_VALUE = new String[0];

    proces_VALUE(int identifikator_VALUE, int roditelj_identifikator, stranica_menadžer.adresa_prostor adresa_prostor, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.roditelj_identifikator = roditelj_identifikator;
        this.adresa_prostor = adresa_prostor;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int roditelj_identifikator() {
        return roditelj_identifikator;
    }

    public stranica_menadžer.adresa_prostor adresa_prostor() {
        return adresa_prostor;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public proces_stanje stanje_VALUE() {
        return stanje_VALUE;
    }

    public void skup_stanje(proces_stanje 새상태) {
        stanje_VALUE = 새상태;
    }

    public int izaći_kod() {
        return izaći_kod;
    }

    public void izaći_program(int VALUE) {
        izaći_kod = VALUE & 0xff;
        stanje_VALUE = proces_stanje.izaći_program;
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

    public void 실행문맥설정(int početna_adresa, String[] parametar_argument, String[] operativno_okruženje) {
        실행시작주소 = početna_adresa;
        실행인자 = parametar_argument.clone();
        operativno_okruženje_VALUE = operativno_okruženje.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] operativno_okruženje_VALUE() { return operativno_okruženje_VALUE.clone(); }
}
