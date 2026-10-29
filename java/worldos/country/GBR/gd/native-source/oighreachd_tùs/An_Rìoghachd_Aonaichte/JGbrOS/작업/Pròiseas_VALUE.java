// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.작업;

import An_Rìoghachd_Aonaichte.JGbrOS.기억공간.duilleag_manaidsear;
import An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean.파일서술자표;

public final class Pròiseas_VALUE {
    private final int aithnichear_VALUE;
    private final int 부모식별자;
    private final duilleag_manaidsear.ADDRESS_spàs ADDRESS_spàs;
    private final 파일서술자표 파일서술자;
    private Pròiseas_cor cor_VALUE = Pròiseas_cor.Ullaich;
    private int fàg_CODE;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    Pròiseas_VALUE(int aithnichear_VALUE, int 부모식별자, duilleag_manaidsear.ADDRESS_spàs ADDRESS_spàs, 파일서술자표 파일서술자) {
        this.aithnichear_VALUE = aithnichear_VALUE;
        this.부모식별자 = 부모식별자;
        this.ADDRESS_spàs = ADDRESS_spàs;
        this.파일서술자 = 파일서술자;
    }

    public int aithnichear_VALUE() {
        return aithnichear_VALUE;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public duilleag_manaidsear.ADDRESS_spàs ADDRESS_spàs() {
        return ADDRESS_spàs;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Pròiseas_cor cor_VALUE() {
        return cor_VALUE;
    }

    public void seata_cor(Pròiseas_cor 새상태) {
        cor_VALUE = 새상태;
    }

    public int fàg_CODE() {
        return fàg_CODE;
    }

    public void fàg_ap(int VALUE) {
        fàg_CODE = VALUE & 0xff;
        cor_VALUE = Pròiseas_cor.fàg_ap;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ap_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Start_ADDRESS, String[] 인자, String[] 환경) {
        실행시작주소 = Start_ADDRESS;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
