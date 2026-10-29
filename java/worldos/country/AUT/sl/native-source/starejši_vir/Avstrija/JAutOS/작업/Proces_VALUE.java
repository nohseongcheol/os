// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Avstrija.JAutOS.작업;

import Avstrija.JAutOS.pomnilnik_območje.stran_Upravitelj;
import Avstrija.JAutOS.datotečni_sistem.파일서술자표;

public final class Proces_VALUE {
    private final int identifikator_VALUE;
    private final int nadrejen_identifikator;
    private final stran_Upravitelj.naslov_Space naslov_Space;
    private final 파일서술자표 파일서술자;
    private Proces_stanje stanje_VALUE = Proces_stanje.Pripravi;
    private int izhodna_koda;
    private int aplikacija_odmor = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proces_VALUE(int identifikator_VALUE, int nadrejen_identifikator, stran_Upravitelj.naslov_Space naslov_Space, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.nadrejen_identifikator = nadrejen_identifikator;
        this.naslov_Space = naslov_Space;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int nadrejen_identifikator() {
        return nadrejen_identifikator;
    }

    public stran_Upravitelj.naslov_Space naslov_Space() {
        return naslov_Space;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_stanje stanje_VALUE() {
        return stanje_VALUE;
    }

    public void nabor_stanje(Proces_stanje 새상태) {
        stanje_VALUE = 새상태;
    }

    public int izhodna_koda() {
        return izhodna_koda;
    }

    public void Izhod_aplikacija(int VALUE) {
        izhodna_koda = VALUE & 0xff;
        stanje_VALUE = Proces_stanje.Izhod_aplikacija;
    }

    public int aplikacija_odmor() {
        return aplikacija_odmor;
    }

    public void nabor_aplikacija_odmor(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("aplikacija_f5044b9b 끝 범위를 벗어났습니다.");
        }
        aplikacija_odmor = 새끝;
    }

    public void 실행문맥설정(int Start_naslov, String[] parameter_argument, String[] 환경) {
        실행시작주소 = Start_naslov;
        실행인자 = parameter_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
