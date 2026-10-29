// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuva.JLtuOS.작업;

import Lietuva.JLtuOS.atmintis_sritis.쪽관리자;
import Lietuva.JLtuOS.failų_sistema.파일서술자표;

public final class Procesas_VALUE {
    private final int identifikatorius_VALUE;
    private final int pirminis_identifikatorius;
    private final 쪽관리자.ADDRESS_erdvė ADDRESS_erdvė;
    private final 파일서술자표 파일서술자;
    private Procesas_Būsena Būsena_VALUE = Procesas_Būsena.Parengti;
    private int Baigti_CODE;
    private int programa_nutraukti = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Procesas_VALUE(int identifikatorius_VALUE, int pirminis_identifikatorius, 쪽관리자.ADDRESS_erdvė ADDRESS_erdvė, 파일서술자표 파일서술자) {
        this.identifikatorius_VALUE = identifikatorius_VALUE;
        this.pirminis_identifikatorius = pirminis_identifikatorius;
        this.ADDRESS_erdvė = ADDRESS_erdvė;
        this.파일서술자 = 파일서술자;
    }

    public int identifikatorius_VALUE() {
        return identifikatorius_VALUE;
    }

    public int pirminis_identifikatorius() {
        return pirminis_identifikatorius;
    }

    public 쪽관리자.ADDRESS_erdvė ADDRESS_erdvė() {
        return ADDRESS_erdvė;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Procesas_Būsena Būsena_VALUE() {
        return Būsena_VALUE;
    }

    public void rinkinys_Būsena(Procesas_Būsena 새상태) {
        Būsena_VALUE = 새상태;
    }

    public int Baigti_CODE() {
        return Baigti_CODE;
    }

    public void Baigti_programa_086bb533(int VALUE) {
        Baigti_CODE = VALUE & 0xff;
        Būsena_VALUE = Procesas_Būsena.Baigti_programa_086bb533;
    }

    public int programa_nutraukti() {
        return programa_nutraukti;
    }

    public void rinkinys_programa_nutraukti(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("programa_f5044b9b 끝 범위를 벗어났습니다.");
        }
        programa_nutraukti = 새끝;
    }

    public void 실행문맥설정(int Start_ADDRESS, String[] parametras_argumentas, String[] 환경) {
        실행시작주소 = Start_ADDRESS;
        실행인자 = parametras_argumentas.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
