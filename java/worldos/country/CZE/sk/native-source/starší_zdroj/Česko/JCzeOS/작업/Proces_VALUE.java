// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.작업;

import Česko.JCzeOS.Pamäť_oblasť.쪽관리자;
import Česko.JCzeOS.systém_súborov.파일서술자표;

public final class Proces_VALUE {
    private final int identifikátor_VALUE;
    private final int nadradený_identifikátor;
    private final 쪽관리자.adresa_priestor adresa_priestor;
    private final 파일서술자표 파일서술자;
    private Proces_Stav Stav_VALUE = Proces_Stav.Pripraviť;
    private int kód_ukončenia;
    private int program_prerušiť = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proces_VALUE(int identifikátor_VALUE, int nadradený_identifikátor, 쪽관리자.adresa_priestor adresa_priestor, 파일서술자표 파일서술자) {
        this.identifikátor_VALUE = identifikátor_VALUE;
        this.nadradený_identifikátor = nadradený_identifikátor;
        this.adresa_priestor = adresa_priestor;
        this.파일서술자 = 파일서술자;
    }

    public int identifikátor_VALUE() {
        return identifikátor_VALUE;
    }

    public int nadradený_identifikátor() {
        return nadradený_identifikátor;
    }

    public 쪽관리자.adresa_priestor adresa_priestor() {
        return adresa_priestor;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_Stav Stav_VALUE() {
        return Stav_VALUE;
    }

    public void množina_Stav(Proces_Stav 새상태) {
        Stav_VALUE = 새상태;
    }

    public int kód_ukončenia() {
        return kód_ukončenia;
    }

    public void Skončiť_program(int VALUE) {
        kód_ukončenia = VALUE & 0xff;
        Stav_VALUE = Proces_Stav.Skončiť_program;
    }

    public int program_prerušiť() {
        return program_prerušiť;
    }

    public void množina_program_prerušiť(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_prerušiť = 새끝;
    }

    public void 실행문맥설정(int START_adresa, String[] parameter_argument, String[] 환경) {
        실행시작주소 = START_adresa;
        실행인자 = parameter_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
