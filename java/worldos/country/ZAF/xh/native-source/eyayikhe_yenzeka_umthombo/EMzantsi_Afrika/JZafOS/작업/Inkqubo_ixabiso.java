// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.작업;

import EMzantsi_Afrika.JZafOS.기억공간.ikhasi_umphathi;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.파일서술자표;

public final class Inkqubo_ixabiso {
    private final int isalathisi_ixabiso;
    private final int 부모식별자;
    private final ikhasi_umphathi.idilesi_isithuba idilesi_isithuba;
    private final 파일서술자표 파일서술자;
    private Inkqubo_imo_4346e67f imo_ixabiso = Inkqubo_imo_4346e67f.lungisa;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Inkqubo_ixabiso(int isalathisi_ixabiso, int 부모식별자, ikhasi_umphathi.idilesi_isithuba idilesi_isithuba, 파일서술자표 파일서술자) {
        this.isalathisi_ixabiso = isalathisi_ixabiso;
        this.부모식별자 = 부모식별자;
        this.idilesi_isithuba = idilesi_isithuba;
        this.파일서술자 = 파일서술자;
    }

    public int isalathisi_ixabiso() {
        return isalathisi_ixabiso;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ikhasi_umphathi.idilesi_isithuba idilesi_isithuba() {
        return idilesi_isithuba;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Inkqubo_imo_4346e67f imo_ixabiso() {
        return imo_ixabiso;
    }

    public void isethi_imo(Inkqubo_imo_4346e67f 새상태) {
        imo_ixabiso = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void phuma_inkqubo(int ixabiso) {
        종료값 = ixabiso & 0xff;
        imo_ixabiso = Inkqubo_imo_4346e67f.phuma_inkqubo;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("inkqubo_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int qala_idilesi, String[] 인자, String[] 환경) {
        실행시작주소 = qala_idilesi;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
