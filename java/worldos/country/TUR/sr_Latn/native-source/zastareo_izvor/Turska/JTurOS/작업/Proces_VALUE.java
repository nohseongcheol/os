// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turska.JTurOS.작업;

import Turska.JTurOS.Memorija_oblast.stranica_menadžer;
import Turska.JTurOS.sistem_datoteka.파일서술자표;

public final class Proces_VALUE {
    private final int identifikator_VALUE;
    private final int nadređen_identifikator;
    private final stranica_menadžer.adresa_prostor adresa_prostor;
    private final 파일서술자표 파일서술자;
    private Proces_Status Status_VALUE = Proces_Status.Pripremi;
    private int Izađi_kôd;
    private int program_pauza = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Proces_VALUE(int identifikator_VALUE, int nadređen_identifikator, stranica_menadžer.adresa_prostor adresa_prostor, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.nadređen_identifikator = nadređen_identifikator;
        this.adresa_prostor = adresa_prostor;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int nadređen_identifikator() {
        return nadređen_identifikator;
    }

    public stranica_menadžer.adresa_prostor adresa_prostor() {
        return adresa_prostor;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_Status Status_VALUE() {
        return Status_VALUE;
    }

    public void skup_Status(Proces_Status 새상태) {
        Status_VALUE = 새상태;
    }

    public int Izađi_kôd() {
        return Izađi_kôd;
    }

    public void Izađi_program(int VALUE) {
        Izađi_kôd = VALUE & 0xff;
        Status_VALUE = Proces_Status.Izađi_program;
    }

    public int program_pauza() {
        return program_pauza;
    }

    public void skup_program_pauza(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_pauza = 새끝;
    }

    public void 실행문맥설정(int START_adresa, String[] parametar_argument, String[] 환경) {
        실행시작주소 = START_adresa;
        실행인자 = parametar_argument.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
