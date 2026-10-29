// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.작업;

import COD.JCodOS.기억공간.paji_Umugenzuzi;
import COD.JCodOS.sisitemu_ya_dosiye.파일서술자표;

public final class Inzira_agaciro {
    private final int indanga_agaciro;
    private final int 부모식별자;
    private final paji_Umugenzuzi.aderesi_akanya aderesi_akanya;
    private final 파일서술자표 파일서술자;
    private Inzira_imimerere imimerere_agaciro = Inzira_imimerere.Gutegura;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Inzira_agaciro(int indanga_agaciro, int 부모식별자, paji_Umugenzuzi.aderesi_akanya aderesi_akanya, 파일서술자표 파일서술자) {
        this.indanga_agaciro = indanga_agaciro;
        this.부모식별자 = 부모식별자;
        this.aderesi_akanya = aderesi_akanya;
        this.파일서술자 = 파일서술자;
    }

    public int indanga_agaciro() {
        return indanga_agaciro;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public paji_Umugenzuzi.aderesi_akanya aderesi_akanya() {
        return aderesi_akanya;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Inzira_imimerere imimerere_agaciro() {
        return imimerere_agaciro;
    }

    public void itsinda_imimerere(Inzira_imimerere 새상태) {
        imimerere_agaciro = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void gusohoka_porogaramu(int agaciro) {
        종료값 = agaciro & 0xff;
        imimerere_agaciro = Inzira_imimerere.gusohoka_porogaramu;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("porogaramu_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Itangira_aderesi, String[] 인자, String[] 환경) {
        실행시작주소 = Itangira_aderesi;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
