// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.작업;

import Kanada.JCanOS.Memorija_regije.dojaviti_Upravitelj;
import Kanada.JCanOS.datotečni_sustav.파일서술자표;

public final class Proces_VALUE {
    private final int identifikator_VALUE;
    private final int roditeljski_identifikator;
    private final dojaviti_Upravitelj.adresa_Space adresa_Space;
    private final 파일서술자표 파일서술자;
    private Proces_Stanje Stanje_VALUE = Proces_Stanje.Pripremi;
    private int Izlaz_kod;
    private int program_pauza = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] okruženje_VALUE = new String[0];

    Proces_VALUE(int identifikator_VALUE, int roditeljski_identifikator, dojaviti_Upravitelj.adresa_Space adresa_Space, 파일서술자표 파일서술자) {
        this.identifikator_VALUE = identifikator_VALUE;
        this.roditeljski_identifikator = roditeljski_identifikator;
        this.adresa_Space = adresa_Space;
        this.파일서술자 = 파일서술자;
    }

    public int identifikator_VALUE() {
        return identifikator_VALUE;
    }

    public int roditeljski_identifikator() {
        return roditeljski_identifikator;
    }

    public dojaviti_Upravitelj.adresa_Space adresa_Space() {
        return adresa_Space;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_Stanje Stanje_VALUE() {
        return Stanje_VALUE;
    }

    public void skup_Stanje(Proces_Stanje 새상태) {
        Stanje_VALUE = 새상태;
    }

    public int Izlaz_kod() {
        return Izlaz_kod;
    }

    public void Izlaz_program(int VALUE) {
        Izlaz_kod = VALUE & 0xff;
        Stanje_VALUE = Proces_Stanje.Izlaz_program;
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

    public void 실행문맥설정(int START_adresa, String[] parametar_argument, String[] okruženje) {
        실행시작주소 = START_adresa;
        실행인자 = parametar_argument.clone();
        okruženje_VALUE = okruženje.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] okruženje_VALUE() { return okruženje_VALUE.clone(); }
}
