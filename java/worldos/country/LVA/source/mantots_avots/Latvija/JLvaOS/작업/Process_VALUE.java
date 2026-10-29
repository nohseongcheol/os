// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.작업;

import Latvija.JLvaOS.atmiņa_reģions.쪽관리자;
import Latvija.JLvaOS.failu_sistēma.파일서술자표;

public final class Process_VALUE {
    private final int identifikators_VALUE;
    private final int vecākobjekts_identifikators;
    private final 쪽관리자.adrese_telpa adrese_telpa;
    private final 파일서술자표 파일서술자;
    private Process_Statuss Statuss_VALUE = Process_Statuss.Sagatavot;
    private int Iziet_CODE;
    private int programma_pārtraukt = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Process_VALUE(int identifikators_VALUE, int vecākobjekts_identifikators, 쪽관리자.adrese_telpa adrese_telpa, 파일서술자표 파일서술자) {
        this.identifikators_VALUE = identifikators_VALUE;
        this.vecākobjekts_identifikators = vecākobjekts_identifikators;
        this.adrese_telpa = adrese_telpa;
        this.파일서술자 = 파일서술자;
    }

    public int identifikators_VALUE() {
        return identifikators_VALUE;
    }

    public int vecākobjekts_identifikators() {
        return vecākobjekts_identifikators;
    }

    public 쪽관리자.adrese_telpa adrese_telpa() {
        return adrese_telpa;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Process_Statuss Statuss_VALUE() {
        return Statuss_VALUE;
    }

    public void kopa_Statuss(Process_Statuss 새상태) {
        Statuss_VALUE = 새상태;
    }

    public int Iziet_CODE() {
        return Iziet_CODE;
    }

    public void Iziet_programma(int VALUE) {
        Iziet_CODE = VALUE & 0xff;
        Statuss_VALUE = Process_Statuss.Iziet_programma;
    }

    public int programma_pārtraukt() {
        return programma_pārtraukt;
    }

    public void kopa_programma_pārtraukt(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programma_f5044b9b 끝 범위를 벗어났습니다.");
        }
        programma_pārtraukt = 새끝;
    }

    public void 실행문맥설정(int Sākt_adrese, String[] parametrs_arg, String[] 환경) {
        실행시작주소 = Sākt_adrese;
        실행인자 = parametrs_arg.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
