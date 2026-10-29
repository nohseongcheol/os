// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.작업;

import Espainia.JEspOS.기억공간.orri_kudeatzaile;
import Espainia.JEspOS.fitxategi_sistema.파일서술자표;

public final class prozesu_balio {
    private final int identifikatzaile_balio;
    private final int 부모식별자;
    private final orri_kudeatzaile.helbide_gune helbide_gune;
    private final 파일서술자표 파일서술자;
    private prozesu_Egoera Egoera_balio = prozesu_Egoera.준비;
    private int irten_KODE;
    private int aplik_atseden = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    prozesu_balio(int identifikatzaile_balio, int 부모식별자, orri_kudeatzaile.helbide_gune helbide_gune, 파일서술자표 파일서술자) {
        this.identifikatzaile_balio = identifikatzaile_balio;
        this.부모식별자 = 부모식별자;
        this.helbide_gune = helbide_gune;
        this.파일서술자 = 파일서술자;
    }

    public int identifikatzaile_balio() {
        return identifikatzaile_balio;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public orri_kudeatzaile.helbide_gune helbide_gune() {
        return helbide_gune;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public prozesu_Egoera Egoera_balio() {
        return Egoera_balio;
    }

    public void sorta_Egoera(prozesu_Egoera 새상태) {
        Egoera_balio = 새상태;
    }

    public int irten_KODE() {
        return irten_KODE;
    }

    public void irten_aplik(int balio) {
        irten_KODE = balio & 0xff;
        Egoera_balio = prozesu_Egoera.irten_aplik;
    }

    public int aplik_atseden() {
        return aplik_atseden;
    }

    public void sorta_aplik_atseden(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("aplik_f5044b9b 끝 범위를 벗어났습니다.");
        }
        aplik_atseden = 새끝;
    }

    public void 실행문맥설정(int HASI_helbide, String[] parametro_arg, String[] 환경) {
        실행시작주소 = HASI_helbide;
        실행인자 = parametro_arg.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
